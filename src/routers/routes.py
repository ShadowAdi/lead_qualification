from fastapi import APIRouter, UploadFile, File
from fastapi import Request, HTTPException
from src.schema import schemas
from src.storage import storage
from src.services import parse_csv
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/offer")
async def CreateOffer(request: Request, offer: schemas.Offer):
    try:
        storage.set_offer(offer=offer)
        return {"success": True, "offer": offer}
    except Exception as e:
        logger.error(f"Error in offer: {e}", exc_info=True)
        raise HTTPException(500, detail="Internal Server Error")


@router.post("/leads/upload")
async def UploadLeads(request: Request, file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="Invalid File Upload. Only Upload CSV Files"
        )
    content = await file.read()
    leads = parse_csv(content)
    storage.save_leads(leads=leads)
    return {"success": True, "count": len(leads)}
