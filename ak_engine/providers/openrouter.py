import os
from openai import OpenAI


class OpenRouterProvider:

    def __init__(self, model=None):

        self.client = OpenAI(
            api_key=os.environ["OPENROUTER_API_KEY"],
            base_url="https://openrouter.ai/api/v1",
        )

        self.model = model or os.getenv(
            "OPENROUTER_MODEL",
            "openai/gpt-oss-120b",
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
