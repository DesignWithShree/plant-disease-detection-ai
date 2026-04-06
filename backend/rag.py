import json
import os
import requests

# ---------------------------
# LOAD DATABASE (SAFE PATH)
# ---------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file_path = os.path.join(BASE_DIR, "data", "disease_database.json")

print("Loading disease data from:", file_path)

try:
    with open(file_path, "r") as f:
        disease_db = json.load(f)
except FileNotFoundError:
    print("❌ disease_database.json NOT FOUND")
    disease_db = {}

# ---------------------------
# SAFE OLLAMA CALL
# ---------------------------
def call_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code != 200:
            return "⚠️ Ollama API error"

        try:
            data = response.json()
        except:
            return "⚠️ Invalid response from AI"

        return data.get("response", "⚠️ No AI response")

    except Exception as e:
        print("🔥 Ollama Error:", e)
        return "⚠️ Ollama failed"


# ---------------------------
# RAG AGENT (NO CRASH VERSION)
# ---------------------------
def rag_agent(disease_name, confidence):

    # 🔥 Always safe (no crash)
    data = disease_db.get(disease_name, {})

    if not data:
        print("⚠️ Disease not found:", disease_name)

    # STRUCTURED PROMPT
    prompt = f"""
You are an agricultural expert.

Explain the disease in a clear structured way.

Use this format:

Title: {disease_name}

1. What is it?
- point
- point

2. Severity
- point
- point

3. Treatment Steps
- Step 1
- Step 2

4. Prevention
- point
- point

Keep it simple and readable.
"""

    ai_response = call_ollama(prompt)

    return {
        "plant": data.get("plant", "Unknown"),
        "disease": data.get("disease", disease_name),
        "description": data.get("description", "No description available"),
        "severity": "High" if confidence > 0.8 else "Moderate",
        "fertilizer": data.get("fertilizer", []),
        "pesticide": data.get("pesticide", []),
        "organic_solution": data.get("organic_solution", []),
        "prevention": data.get("prevention", []),
        "ai_explanation": ai_response
    }