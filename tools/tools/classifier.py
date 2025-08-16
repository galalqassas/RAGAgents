import requests
import re

OLLAMA_MODEL_ID = "llama3.1:8b-instruct-q8_0"

def classify_query_intent(query: str):
    query = query.strip().replace("\n", " ").replace("\r", " ")

    system_prompt = (
        "You are a classification expert. Classify the user's query into one or more of the following categories "
        "depending on relevance:\n"
        "- activity\n"
        "- accommodation\n"
        "- visa\n"
        "- scam\n"
        "- dish\n"
        "- transport\n"
        "- seasonal\n"
        "- restaurant\n\n"
        "Rules:\n"
        "- Reply with a comma-separated list of relevant categories (e.g., visa, restaurant)\n"
        "- Do NOT explain. Do NOT add anything else. ONLY output categories.\n"
        "- If only one category applies, return just that one word.\n"
        "- Only use the category names listed above. No synonyms or other text.\n\n"
        f"Query: {query}\nLabels:"
    )

    payload = {
        "model": OLLAMA_MODEL_ID,
        "prompt": system_prompt,
        "stream": False
    }

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()

        raw = response.json()["response"].strip().lower()
        # print(f"[Classifier Raw Output]: {raw}")

        valid_labels = ["activity", "accommodation", "visa", "restaurant","scam","transport","dish","seasonal"]
        found_labels = [label.strip() for label in raw.split(",") if label.strip() in valid_labels]


        if len(found_labels) == 1:
            return found_labels[0]  
        elif found_labels:
            return found_labels     
        else:
            return "unknown"

    except Exception as e:
        print(f"[Intent Classifier Error]: {e}")
        return "unknown"
