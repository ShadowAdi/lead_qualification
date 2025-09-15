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

def get_offer() -> schemas.Offer:
    return _offer


def get_leads()->List[schemas.Lead]:
    return _leads

def save_results(results):
    global _results
    _results = results

def get_results():
    return _results

def save_leads(leads:List[schemas.Lead]):
    logger.info("Storing Leads")
    global _leads
    _leads=leads