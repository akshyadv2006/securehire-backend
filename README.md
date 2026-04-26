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