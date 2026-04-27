from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pickle
import re
import os
import time

# -------------------------
# Debug: check files
# -------------------------
print("Files inside container:", os.listdir())

if os.path.exists("pipeline.pkl"):
    print("Pipeline last modified:",
          time.ctime(os.path.getmtime("pipeline.pkl")))

# -------------------------
# Load pipeline
# -------------------------
try:
    with open("pipeline.pkl", "rb") as f:
        pipeline = pickle.load(f)

    print(
        "Vectorizer fitted inside Docker:",
        hasattr(pipeline.named_steps["tfidf"], "idf_")
    )

except Exception as e:
    print("Error loading pipeline:", e)
    pipeline = None

# -------------------------
# Create app
# -------------------------
app = FastAPI()

# -------------------------
# Enable CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Request schema (UPDATED)
# -------------------------
class JobPost(BaseModel):
    title: str
    description: str
    requirements: str = ""
    salary: str = ""   # ✅ NEW FIELD

# -------------------------
# Health check
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------
# Feature extraction (FIXED)
# -------------------------
def extract_features(text):
    text_lower = text.lower()

    return {
        # ✅ IMPROVED salary detection
        "has_salary": int(bool(re.search(
            r"(₹|\$|lpa|ctc|per annum|lakhs|salary)",
            text_lower
        ))),

        "urgency_words": len(re.findall(
            r'\b(urgent|immediately|asap|earn|quick money)\b',
            text_lower
        )),

        "generic_email": int(bool(re.search(
            r'@gmail|@yahoo|@hotmail',
            text_lower
        ))),

        "suspicious_phrases": int(bool(re.search(
            r'no experience|work from home|easy money|earn fast|no interview',
            text_lower
        ))),

        "has_contact": int(bool(re.search(
            r'whatsapp|telegram|call now|contact us',
            text_lower
        ))),

        "too_good_salary": int(bool(re.search(
            r'earn \d{5,}|salary \d{5,}',
            text_lower
        )))
    }

# -------------------------
# Reason generator (IMPROVED)
# -------------------------
def get_reasons(features):
    reasons = []

    if features["urgency_words"] > 0:
        reasons.append("Uses urgent or pressure language")

    if features["generic_email"] == 1:
        reasons.append("Uses free email provider")

    if features["has_salary"] == 0:
        reasons.append("No clear salary mentioned")

    if features["suspicious_phrases"] == 1:
        reasons.append("Contains suspicious phrases")

    if features["has_contact"] == 1:
        reasons.append("Asks to contact directly (WhatsApp/Telegram)")

    if features["too_good_salary"] == 1:
        reasons.append("Unrealistically high salary mentioned")

    if len(reasons) == 0:
        reasons.append("No strong risk signals detected")

    return reasons

# -------------------------
# Predict endpoint (FIXED)
# -------------------------
@app.post("/predict")
def predict(job: JobPost):

    if pipeline is None:
        return {"error": "Pipeline not loaded properly"}

    # ✅ INCLUDE salary in model input
    text = f"{job.title} {job.description} {job.requirements} {job.salary}"

    print("🔍 INPUT TEXT:", text[:200])  # debug

    prob = pipeline.predict_proba([text])[0][1]

    features = extract_features(text)
    reasons = get_reasons(features)

    if prob > 0.7:
        verdict = "HIGH RISK"
    elif prob > 0.3:
        verdict = "SUSPICIOUS"
    else:
        verdict = "REAL"

    return {
        "verdict": verdict,
        "confidence": round(float(prob), 3),
        "reasons": reasons,
        "features": features
    }