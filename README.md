# 📚 RevisionAI — Last-Minute Exam Prep Tool

A beautiful AI-powered revision notes generator built with Python + Streamlit.
Powered by Groq AI (100% Free, no credit card needed).

---

## 🚀 Setup & Run (Do This Once)

### Step 1 — Make sure Python is installed
Open Command Prompt and type:
```
python --version
```
If you see Python 3.x.x you're good. If not, download from https://python.org

---

### Step 2 — Open this project folder in terminal
```
cd "D:\Jit all\Revise Ai"
```

---

### Step 3 — Create virtual environment
```
python -m venv venv
```

---

### Step 4 — Activate virtual environment

**Windows:**
```
venv\Scripts\activate
```

**Mac/Linux:**
```
source venv/bin/activate
```

You'll see `(venv)` appear in your terminal — that means it's active.

---

### Step 5 — Install all dependencies
```
pip install -r requirements.txt
```
This installs everything. Wait for it to finish.

---

### Step 6 — Run the app
```
streamlit run app.py
```

Your browser will open automatically at http://localhost:8501 🎉

---

## 🔑 Get Free Groq API Key

1. Go to https://console.groq.com
2. Sign up free (no credit card)
3. Click API Keys → Create API Key
4. Copy the key (starts with gsk_...)
5. Paste it in the sidebar of the app

---

## 📁 Project Structure

```
Revise Ai/
├── app.py                  ← Main Streamlit app
├── requirements.txt        ← All dependencies
├── README.md               ← This file
└── backend/
    ├── __init__.py         ← Makes backend a Python package
    ├── ai_engine.py        ← Groq AI calls & prompt building
    └── file_reader.py      ← PDF, DOCX, PPTX, TXT reader
```

---

## ✨ Features

- Upload PDF, DOCX, PPTX, TXT files
- Type any topic or paste your notes
- 3 modes: Detailed Notes / MCQ Quiz / Exam Mode
- Choose AI model and output length
- Download generated notes as .txt
- Beautiful dark UI

---

## 🔁 Every Time You Want to Run the App

```
cd "D:\Jit all\Revise Ai"
venv\Scripts\activate
streamlit run app.py
```

That's it!
