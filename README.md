![CI](https://github.com/YOUR_USERNAME/securehire-backend/actions/workflows/ci.yml/badge.svg)

# SecureHire 🔍

Detect fake job postings using Machine Learning.

## 🚀 Live API
https://your-render-url.onrender.com

## 🧠 Features
- Fake job detection
- Risk scoring
- Explanation (reasons)
- Chrome extension integration
- Highlight suspicious content

## 📦 Project Structure
- backend → FastAPI + ML model
- extension → Chrome extension
- tests → API tests
- data → sample dataset

## ⚙️ Tech Stack
- FastAPI
- Scikit-learn
- Docker
- GitHub Actions

## 🧪 Run locally

pip install -r requirements.txt  
uvicorn main:app --reload

## 📊 Model
TF-IDF + Logistic Regression + heuristic features

## 🚀 Live API
https://your-render-url.onrender.com

## 🎥 Demo
(Add GIF or video later)

## 🧠 Features
- Detect fake job postings
- Risk scoring (Real vs Risk %)
- Reason explanation
- Chrome extension integration

## 🧪 Testing
pytest-based API testing

## 🐳 Docker
docker build -t securehire .
docker run -p 8000:8000 securehire