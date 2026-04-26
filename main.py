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
# Request schema
# -------------------------
class JobPost(BaseModel):
    title: str
    description: str
    requirements: str = ""

# -------------------------
# Health check
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------------
# Feature extraction (IMPROVED)
# -------------------------
def extract_features(text):
    return {
        # better salary detection
        "has_salary": int(bool(re.search(r"(₹|\$|salary|lpa|per annum)", text, re.I))),

        # urgency / scam signals
        "urgency_words": len(re.findall(
            r'\b(urgent|immediately|asap|earn|quick money)\b', text, re.I
        )),

        # suspicious emails
        "generic_email": int(bool(re.search(
            r'@gmail|@yahoo|@hotmail', text, re.I
        ))),

        # extra scam patterns
        "suspicious_phrases": int(bool(re.search(
            r'no experience|work from home|easy money|earn fast',
            text, re.I
        )))
    }

# -------------------------
# Reason generator (FIXED)
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

    # 🔥 IMPORTANT: fallback
    if len(reasons) == 0:
        reasons.append("No strong risk signals detected")

    return reasons

# -------------------------
# Predict endpoint
# -------------------------
@app.post("/predict")
def predict(job: JobPost):

    if pipeline is None:
        return {"error": "Pipeline not loaded properly"}

    text = job.title + " " + job.description + " " + job.requirements

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