from ak_engine.memory.storage import MemoryStorage
from ak_engine.memory.search import MemorySearch
from ak_engine.memory.extractor import MemoryExtractor
from ak_engine.memory.history import ConversationHistory


class MemoryManager:
    def __init__(self):
        self.storage = MemoryStorage()
        self.search_engine = MemorySearch(self.storage)
        self.extractor = MemoryExtractor()
        self.history = ConversationHistory()

    def remember(self, category, key, value):
        self.storage.save(category, key, value)

    def auto_remember(self, text):
        memories = self.extractor.extract(text)

        for category, key, value in memories:
            self.remember(category, key, value)

        return memories

    def add_message(self, role, content):
        self.history.add(role, content)

    def conversation(self):
        return self.history.get()

    def clear_conversation(self):
        self.history.clear()

    def recall(self, category, key):
        return self.storage.load(category, key)

    def list_category(self, category):
        return self.storage.list_category(category)

    def search(self, keyword):
        return self.search_engine.search(keyword)
