import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_fake_job():
    res = client.post("/predict", json={
        "title": "Earn money fast",
        "description": "No experience needed, contact via WhatsApp",
        "requirements": ""
    })
    assert res.status_code == 200

def test_real_job():
    res = client.post("/predict", json={
        "title": "Software Engineer",
        "description": "Python developer role",
        "requirements": ""
    })
    assert res.status_code == 200

def test_health():
    res = client.get("/health")
    assert res.status_code == 200