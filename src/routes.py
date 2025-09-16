from fastapi import APIRouter, UploadFile, File
from fastapi import Request, HTTPException
from src.schemas import Lead, Offer, Result
from src.storage import (
    set_offer,
    save_leads,
    get_leads,
    get_offer,
    get_results,
    save_results,
)
from src import parse_csv
import logging
from src import ai_client
from src import scoring

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/offer")
async def CreateOffer(offer: Offer):
    try:
        set_offer(offer=offer)
        return {"success": True, "offer": offer}
    except Exception as e:
        logger.error(f"Error in offer: {e}", exc_info=True)
        raise HTTPException(500, detail="Internal Server Error")


@router.post("/leads/upload")
async def UploadLeads(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=400, detail="Invalid File Upload. Only Upload CSV Files"
            )
        content = await file.read()
        leads = parse_csv.parse_leads_csv(content)
        save_leads(leads=leads)
        return {"success": True, "count": len(leads)}
    except Exception as e:
        logger.error(f"Error in Upload Leads: {e}", exc_info=True)
        raise HTTPException(500, detail="Internal Server Error")


@router.post("/score")
async def run_score():
    try:
        offer = get_offer()
        if not offer:
            raise HTTPException(status_code=400, detail="No offer found. POST /offer first.")
        leads = get_leads()
        if not leads:
            raise HTTPException(status_code=400, detail="No leads found. POST /leads/upload first.")
        results = []
        for lead in leads:
            rule_score, rule_reason = scoring.compute_rule_score(lead, offer)

            lead_dict = lead.model_dump()
            offer_dict = offer.model_dump()
            try:
                ai_out = ai_client.classify_intent(lead_dict, offer_dict)
                intent = ai_out.get("intent", "Low").capitalize()
                explanation = ai_out.get("explanation", "")
            except Exception as e:
                intent = "Low"
                explanation = f"AI call failed: {str(e)}"

            ai_map = {"High": 50, "Medium": 30, "Low": 10}
            ai_points = ai_map.get(intent, 10)
            final = rule_score + ai_points

            out = lead_dict.copy()
            out.update({
                "intent": intent,
                "score": int(final),
                "reasoning": f"{rule_reason} AI: {explanation}"
            })
            results.append(out)

        save_results(results=results)
        return {"status": "ok", "count": len(results)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in Calculating Score: {e}", exc_info=True)
        raise HTTPException(500, detail="Internal Server Error")



@router.get("/results")
async def get_scored_results():
    return get_results()
