import os
from google import genai


class GeminiProvider:

    def __init__(self, model=None):

        self.client = genai.Client(
            api_key=os.environ["GEMINI_API_KEY"]
        )

        self.model = model or os.getenv(
            "GEMINI_MODEL",
            "gemini-3.5-flash",
        )

    def chat(
        self,
        message,
        task="general",
        model=None,
    ):
        selected_model = model or self.model

        response = self.client.models.generate_content(
            model=selected_model,
            contents=message,
        )

        return response.text
