from pydantic import BaseModel
from typing import List, Optional


class Offer(BaseModel):
    name: str
    value_props: List[str]
    ideal_use_cases: List[str]


class Lead(BaseModel):
    name: str
    role: str
    company: str
    industry: str
    location: Optional[str] = None
    linkedin_bio: Optional[str] = None


class Result(BaseModel):
    name: str
    role: str
    company: str
    intent: str
    score: int
    reasoning: str
