from fastapi import APIRouter
from fastapi import Request, HTTPException
from src.schema import schemas
from src.storage import storage
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
