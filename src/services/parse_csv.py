from typing import List
from src.schema import schemas
import csv
from io import StringIO


def parse_leads_csv(content: bytes) -> List[schemas.Lead]:
    text = content.decode("utf-8")
    reader = csv.DictReader(StringIO(text))
    leads = []
    for row in reader:
        leads.append(
            schemas.Lead(
                name=row.get("name", "").strip(),
                company=row.get("company", "").strip(),
                role=row.get("role", "").strip(),
                industry=row.get("industry", "").strip(),
                location=row.get("location", "").strip(),
                linkedin_bio=row.get("linkedin_bio", "").strip(),
            )
        )
    return leads
