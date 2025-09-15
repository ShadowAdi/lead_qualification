from typing import List
from src.schema import schemas
import logging

logger = logging.getLogger(__name__)


_offer: schemas.Offer = None
_leads: List[schemas.Lead] = []
_results = List[schemas.Result] = []


def set_offer(offer: schemas.Offer):
    logger.info("Offer Has been stored")
    global _offer
    _offer = offer
