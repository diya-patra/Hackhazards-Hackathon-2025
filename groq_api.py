import requests

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/v1/chat/completions"

def ask_groq(message):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(GROQ_API_URL, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Sorry, something went wrong with Groq API."
