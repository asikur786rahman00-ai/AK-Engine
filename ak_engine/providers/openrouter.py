import requests

class OpenRouterProvider:
    def __init__(self, api_key):
        self.api_key = api_key

    def chat(self, model, message):
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/asikur786rahman00-ai/AK-Engine",
            "X-Title": "AK-Engine"
        }

        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        if not response.ok:
            print("Status:", response.status_code)
            print(response.text)
            return None

        return response.json()["choices"][0]["message"]["content"]
