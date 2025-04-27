# import requests

# GROQ_API_KEY = "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"
# GROQ_API_URL = "https://api.groq.com/v1/chat/completions"

# def ask_groq(message):
#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     data = {
#         "model": "llama3-8b-8192",
#         "messages": [
#             {"role": "user", "content": message}
#         ]
#     }

#     response = requests.post(GROQ_API_URL, json=data, headers=headers)
#     if response.status_code == 200:
#         return response.json()['choices'][0]['message']['content']
#     else:
#         return "Sorry, something went wrong with Groq API."

import requests

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
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

    try:
        response = requests.post(GROQ_API_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return "Sorry, something went wrong with Groq API."