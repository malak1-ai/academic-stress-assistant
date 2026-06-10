import requests
import json

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    },
    data=json.dumps({
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": "say hello"}],
        "max_tokens": 100
    }),
    timeout=30
)

print("Status:", response.status_code)
print("Full response:", json.dumps(response.json(), indent=2))