# 📌 Lead Qualification Backend

This project is a FastAPI backend service that scores leads (prospects) based on product/offer context. It integrates rule-based logic + AI (Google Gemini) to classify buying intent into High, Medium, or Low.

## 🚀 Features

- Upload a CSV of leads and product/offer description

- AI-powered lead scoring (High / Medium / Low)

- Rule-based fallback scoring logic

- Retrieve results as JSON

- (Bonus ✅) Export results as CSV

- Well-documented, clean API design

## 🛠️ Setup Steps

- Clone the Repository

```bash
git clone https://github.com/ShadowAdi/lead_qualification.git
cd lead-qualification
```

- Create Virtual Environment & Install Dependencies

```bash
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

- Add Environment Variables

```bash
API_KEY=YOUR_API_KEY
```

- RUN the Service
  uvicorn app.main:app --reload

The API will be live at:
👉 http://127.0.0.1:8000

🌐 Deployed Backend

Live API base URL:
👉 https://lead-qualification.onrender.com/

## 📖 API Usage Examples

1️⃣ Health Check

```bash
curl -X GET https://127.0.0.1:8000/
```

2️⃣ Submit Offer

Endpoint: POST /api/offer
Description: Save the product/offer description for scoring.

Request:

```bash
    name: str
    value_props: List[str]
    ideal_use_cases: List[str]
```

Response:

```bash
{ "message": "Offer saved successfully" ,"success":boolean
}
```

2️⃣ Upload Leads & Score

Endpoint: POST /api/upload-leads/
Description: Upload a CSV file of leads.

Request:

file: CSV file (with columns like name, company, role, etc.)

Example cURL:

```bash
curl -X POST https://127.0.0.1:8000/api/upload-leads/ \
-F "file=@Leads.csv" \
```

Response

```bash
{
  "results": [
    {
        "success": True, "count": len(leads)
    }
  ]
}
```

3️⃣ Score Leads

Endpoint: POST /api/score

Description: Score all uploaded leads against the submitted offer using rules + Gemini AI.

Response:

```bash
{"status": "ok", "count": len(results)
}
```

4️⃣ Get Results
Endpoint: GET /api/results
Description: Retrieve the latest scored results in JSON format.

"results":
[{"name": "Larry Page", "role": "Founder", "company": "Goggle", "industry": "Tech", "location": "California", "linkedin_bio": "https://www.linkedin.com/in/larrypage", "intent": "Low", "score": 40, "reasoning": "Role match decision maker. ; Industry not matched ; All required fields present; AI: Larry Page is the founder of Google, a massive tech company. SalesBoost CRM's value proposition is targeted towards smaller businesses, not established tech giants like Google."}, ]

5️⃣ Export Results (CSV, Bonus)
Endpoint: GET /api/results/csv
Description: Export scored results as a downloadable CSV file.
Example cURL:

```bash
curl -X GET "https://<your-url>/api/export-csv" -o results.csv
```

## 🧠 Rule Logic & Prompts

### Rule Logic

- High Intent → Keywords like decision maker, budget approved, scaling team

- Medium Intent → Some interest but unclear budget or timeline

- Low Intent → Freelancers, students, or irrelevant industries

## AI Prompt (Gemini)

```bash
PROMPT_TEMPLATE = """
You are an assistant that reads a short prospect profile and an offer description.
Based on the information, classify the prospect's buying intent into one of: High, Medium, Low.
Return exactly a JSON object with keys: "intent" and "explanation".

Prospect: {prospect}
Offer: {offer}

Rules:
- Keep explanation 1-2 sentences, crisp.
- Use business judgement on fit and role.

IMPORTANT: Respond ONLY with valid JSON. No extra text.
"""
```
