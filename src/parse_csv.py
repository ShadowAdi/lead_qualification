from src.schemas import Lead
import csv
from io import StringIO

def safe_strip(value):
    return value.strip() if isinstance(value, str) else ""

def parse_leads_csv(content: bytes):
    leads = []
    decoded = content.decode("utf-8")
    reader = csv.DictReader(StringIO(decoded))
    print("reader ",reader)
    for row in reader:
        print("Row: ",row)
        leads.append(
            Lead(  
                name=safe_strip(row.get("name")),
                company=safe_strip(row.get("company")),
                role=safe_strip(row.get("role")),
                industry=safe_strip(row.get("industry")),
                location=safe_strip(row.get("location")),
                linkedin_bio=safe_strip(row.get("linkedin_bio")),
            )
        )
    return leads
