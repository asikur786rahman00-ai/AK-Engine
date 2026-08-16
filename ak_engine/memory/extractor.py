import re


class MemoryExtractor:
    def extract(self, text):
        memories = []

        patterns = [
            (r"my name is (.+)", "user", "name"),
            (r"i am (.+)", "user", "name"),
            (r"my favorite language is (.+)", "user", "favorite_language"),
            (r"i like (.+)", "user", "likes"),
            (r"i'm building (.+)", "project", "name"),
            (r"i am building (.+)", "project", "name"),
        ]

        text_lower = text.lower()

        for pattern, category, key in patterns:
            match = re.search(pattern, text_lower)
            if match:
                value = match.group(1).strip()
                memories.append((category, key, value))

        return memories
