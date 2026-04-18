# backend/ai_engine.py
# Handles all AI generation using Groq's free API

import requests


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def build_system_prompt(mode: str, topic: str, file_context: str, length: str) -> str:
    """Build the system prompt based on selected mode and options."""

    ctx = f"\n\nContent from uploaded files:\n{file_context}" if file_context else ""
    base = topic if topic else "Generate from the uploaded content."

    length_guide = {
        "concise":  "Keep it concise, bullet-style, max 400 words.",
        "medium":   "Medium length, well-structured, around 600-800 words.",
        "detailed": "Be very thorough and detailed. Cover all key points."
    }.get(length, "Medium length, well-structured.")

    if mode == "detailed":
        return f"""You are an expert academic tutor creating last-minute exam revision notes.

Topic: {base}{ctx}

Instructions:
- {length_guide}
- Start with a clear # Title
- Use ## for major sections, ### for subtopics
- Bold **key terms** throughout
- Use these markers: 📌 key point, ⚠️ important warning, ✅ conclusion
- End with a ## Quick Recall section (5-8 must-know bullet points)
- Make it easy to scan quickly before an exam
- Use clear, simple language"""

    elif mode == "mcq":
        return f"""You are an expert exam coach generating MCQ practice questions.

Topic: {base}{ctx}

Instructions:
- Generate exactly 10 MCQs
- Vary difficulty: 3 easy, 4 medium, 3 hard
- Format EXACTLY as shown for each question:

Q1. [Question text here]
A) [option]
B) [option]
C) [option]
D) [option]
✅ Correct: A) — [One sentence explanation]

---

- End with a ## Study Tips section (3-5 tips)"""

    elif mode == "exam":
        return f"""You are an expert exam strategist generating predicted exam questions with model answers.

Topic: {base}{ctx}

Instructions:
- {length_guide}
- Generate 5-7 predicted exam questions
- Mix: short answer (2-4 marks) and essay questions (8-12 marks)
- For each question use this exact format:

### 🎯 Q[n]: [Question text]
**Marks:** [x marks]
**Model Answer:**
[Detailed answer with bullet points for key arguments]
**💡 Examiner Tip:** [What earns top marks]

---

- End with a ## Common Mistakes to Avoid section"""

    return f"Generate helpful revision notes about: {base}"


def generate_notes(
    api_key: str,
    topic: str,
    mode: str,
    model: str,
    length: str,
    file_context: str = ""
) -> dict:
    """
    Call Groq API and return generated notes.

    Returns:
        dict with keys:
            success (bool)
            content (str) — the generated text
            error   (str) — error message if failed
    """

    system_prompt = build_system_prompt(mode, topic, file_context, length)
    user_message  = topic if topic else "Generate revision notes from the uploaded content."

    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model":       model,
        "max_tokens":  2048,
        "temperature": 0.7,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message}
        ]
    }

    try:
        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            data    = response.json()
            content = data["choices"][0]["message"]["content"].strip()
            return {"success": True, "content": content}

        elif response.status_code == 401:
            return {"success": False, "error": "Invalid API key. Please check your Groq API key."}

        elif response.status_code == 429:
            return {"success": False, "error": "Rate limit hit. Please wait a moment and try again."}

        else:
            err_data = response.json()
            err_msg  = err_data.get("error", {}).get("message", f"API error {response.status_code}")
            return {"success": False, "error": err_msg}

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Please try again."}

    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "No internet connection. Please check your network."}

    except Exception as e:
        return {"success": False, "error": str(e)}
