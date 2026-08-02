from .storage import MemoryStorage


class MemoryManager:
    def __init__(self, db_path="ak_memory.db"):
        self.storage = MemoryStorage(db_path)

    def remember(self, category, key, value):
        self.storage.save(category, key, value)

    def recall(self, category, key):
        return self.storage.load(category, key)

    def forget(self, category, key):
        self.storage.delete(category, key)
