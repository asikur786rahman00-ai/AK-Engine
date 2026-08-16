import os
from groq import Groq


class GroqProvider:

    def __init__(self, model=None):

        self.client = Groq(
            api_key=os.environ["GROQ_API_KEY"]
        )

        self.model = model or os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile",
        )

    def chat(
        self,
        message,
        task="general",
        model=None,
    ):
        selected_model = model or self.model

        response = self.client.chat.completions.create(
            model=selected_model,
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
        )

        return response.choices[0].message.content
