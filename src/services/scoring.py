from typing import Tuple
import re
from src.schema import schemas


DECISION_KEYWORDS = [
    "ceo",
    "founder",
    "co-founder",
    "cto",
    "cpo",
    "head",
    "director",
    "vp",
    "vice president",
    "owner",
    "president",
    "chief",
]
INFLUENCER_KEYWORDS = [
    "manager",
    "lead",
    "principal",
    "senior",
    "marketing",
    "growth",
    "product",
    "analyst",
]


def role_score(role: str) -> Tuple[int, str]:
    if not role:
        return 0, "Role Missing"
    r = role.lower()
    for kw in DECISION_KEYWORDS:
        if kw in r:
            return 20, "Role match decision maker."
    for kw in INFLUENCER_KEYWORDS:
        if kw in r:
            return 10, "Role matches influencer"
    return 0, "Role not a decision maker or influencer."


def industry_score(
    lead_industry: str, offer_ideal_use_cases: list[str]
) -> Tuple[int, str]:
    if not lead_industry:
        return 0, "Industry Missing"
    li = lead_industry.lower()
    for target in offer_ideal_use_cases:
        t = target.lower()
        if all(word in li for word in t.split()):
            return 20, f"Exact industry match to '{target}'"
    lead_tokens = set(re.findall(r"\w+", li))
    for target in offer_ideal_use_cases:
        target_tokens = set(re.findall(r"\w+", target.lower()))
        if lead_tokens & target_tokens:
            return 10, f"Adjacent industry match to '{target}'"
    return 0, "Industry not matched"


def completeness_score(lead: schemas.Lead) -> Tuple[int, str]:
    required = [lead.name, lead.role, lead.company, lead.industry, lead.linkedin_bio]
    if all(field and field.strip() for field in required):
        return 10, "All required fields present"
    else:
        missing = [
            name
            for name, val in zip(
                ["name", "role", "company", "industry", "linkedin_bio"], required
            )
            if not val or not val.strip()
        ]
        return 0, f"Missing fields: {', '.join(missing)}"


def compute_rule_score(lead: schemas.Lead, offer: schemas.Offer) -> Tuple[int, str]:
    rscore, rreason = role_score(lead.role)
    iscore, ireason = industry_score(
        lead_industry=lead.industry, offer_ideal_use_cases=offer.ideal_use_cases
    )
    csscore, csreason = completeness_score(lead=lead)
    total=csscore+iscore+rscore
    reason=f"{rreason} ; {ireason} ; {csreason};"
    return total, reason
