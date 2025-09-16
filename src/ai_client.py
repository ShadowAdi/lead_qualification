import os
from dotenv import load_dotenv
import logging
import json, re
import google.genai as genai

logger = logging.getLogger(__name__)

load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("Missing API_KEY. Please set it in .env file.")

client = genai.Client(api_key=API_KEY)

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


def classify_intent(lead_dict: dict, offer_dict: dict) -> dict:
    prompt = PROMPT_TEMPLATE.format(prospect=lead_dict, offer=offer_dict)

    try:
        resp = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
        )

        text = resp.text.strip()
        logger.info(f"Gemini raw response: {text}")

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception as e:
                logger.warning("Regex JSON parse failed: %s", e)

        first = text.splitlines()[0]
        tokens = first.split()
        label = tokens[0].capitalize() if tokens else "Low"
        explanation = text
        return {
            "intent": label if label in ["High", "Medium", "Low"] else "Low",
            "explanation": explanation,
        }

    except Exception as e:
        logger.error("Gemini call failed: %s", e, exc_info=True)
        return {"intent": "Low", "explanation": "Error during classification"}
