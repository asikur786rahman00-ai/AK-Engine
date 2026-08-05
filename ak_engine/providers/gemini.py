import os
from google import genai

class GeminiProvider:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.environ["GEMINI_API_KEY"]
        )

    def chat(self, message):
        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=message
        )
        return response.text
