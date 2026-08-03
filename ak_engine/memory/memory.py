import json
from pathlib import Path

class Memory:

    def __init__(self):
        self.file = Path("memory.json")

        if not self.file.exists():
            self.file.write_text("[]", encoding="utf-8")

    def save(self, role, content):

        data = json.loads(self.file.read_text())

        data.append({
            "role": role,
            "content": content
        })

        self.file.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8"
        )

    def load(self):

        return json.loads(
            self.file.read_text()
        )

    def clear(self):

        self.file.write_text(
            "[]",
            encoding="utf-8"
        )
