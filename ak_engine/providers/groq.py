import os
from groq import Groq

class GroqProvider:

    def __init__(self, model=None):

        self.client = Groq(
            api_key=os.environ["GROQ_API_KEY"]
        )

        self.model = model or os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile"
        )

    def chat(self, message):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return response.choices[0].message.content
