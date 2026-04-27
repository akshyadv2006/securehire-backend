
# 🚀 SecureHire — AI Job Fraud Detection

![CI](https://github.com/akshyadv2006/securehire-backend/actions/workflows/ci.yml/badge.svg)

SecureHire is an AI-powered system that detects fraudulent job postings using Machine Learning and NLP. It provides real-time risk analysis through a FastAPI backend and integrates with a Chrome extension for in-browser job scanning.

---

## 🌐 Live API

- 🔗 https://securehire-api.onrender.com  
- ❤️ Health Check: https://securehire-api.onrender.com/health  

---

## 🧠 Features

- Detect fake job postings in real-time  
- Risk scoring (Real vs Risk %)  
- Explanation with reasons for predictions  
- Chrome extension integration for job scanning  
- Highlight suspicious content directly on job pages  

---

## ⚙️ Tech Stack

- **Backend:** FastAPI  
- **ML/NLP:** Scikit-learn (TF-IDF + Logistic Regression)  
- **Deployment:** Render, Docker  
- **Testing:** pytest  
- **CI/CD:** GitHub Actions  

---

## 📦 Project Structure
- backend → FastAPI + ML model
- extension → Chrome extension
- tests → API tests
- data → sample dataset


## 🧪 Testing
python -m pytest -v

## 🐳 Docker
docker build -t securehire .
docker run -p 8000:8000 securehire


👤 Author
Akshat Yadav