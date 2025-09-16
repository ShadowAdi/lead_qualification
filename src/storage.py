from typing import List
import json
from pathlib import Path
from src.schemas import Lead, Offer, Result

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

OFFER_FILE = DATA_DIR / "offer.json"
LEADS_FILE = DATA_DIR / "leads.json"
RESULTS_FILE = DATA_DIR / "results.json"

_offer = None
_leads: List[Lead] = []
_results: List[dict] = []

def set_offer(offer: Offer):
    global _offer
    _offer = offer
    with open(OFFER_FILE, "w", encoding="utf-8") as f:
        json.dump(offer.model_dump(), f)

def get_offer() -> Offer | None:
    global _offer
    if _offer:
        return _offer
    if OFFER_FILE.exists():
        data = json.loads(OFFER_FILE.read_text(encoding="utf-8"))
        from src.schemas import Offer as _Offer
        _offer = _Offer(**data)
        return _offer
    return None

def save_leads(leads: List[Lead]):
    global _leads
    _leads = leads
    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump([l.model_dump() for l in leads], f)

def get_leads() -> List[Lead]:
    global _leads
    if _leads:
        return _leads
    if LEADS_FILE.exists():
        data = json.loads(LEADS_FILE.read_text(encoding="utf-8"))
        from src.schemas import Lead as _Lead
        _leads = [_Lead(**d) for d in data]
    return _leads

def save_results(results: List[dict]):
    global _results
    _results = results
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f)

def get_results():
    global _results
    if _results:
        return _results
    if RESULTS_FILE.exists():
        _results = json.loads(RESULTS_FILE.read_text(encoding="utf-8"))
    return _results
