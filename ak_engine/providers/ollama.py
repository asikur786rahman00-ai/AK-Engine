import os
import requests


class OllamaProvider:

    def __init__(self):
        self.base_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://127.0.0.1:11434",
        ).rstrip("/")

        self.model = os.getenv(
            "OLLAMA_MODEL",
            "gemma4:31b-cloud",
        )

        self._check_connection()

    def _check_connection(self):
        response = requests.get(
            f"{self.base_url}/api/tags",
            timeout=5,
        )
        response.raise_for_status()

    def list_models(self):
        response = requests.get(
            f"{self.base_url}/api/tags",
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        return {
            item.get("name")
            for item in data.get("models", [])
            if item.get("name")
        }

    def has_model(self, model):
        return model in self.list_models()

    def chat(
        self,
        prompt,
        task="general",
        model=None,
    ):
        selected_model = model or self.model

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": selected_model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "")
