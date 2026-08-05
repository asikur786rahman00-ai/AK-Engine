import sqlite3

class MemoryAgent:

    def __init__(self, db="ak_memory.db"):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS memory(
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        self.conn.commit()

    def remember(self, key, value):
        self.cur.execute(
            "REPLACE INTO memory VALUES (?,?)",
            (key, value)
        )
        self.conn.commit()

    def recall(self, key):
        self.cur.execute(
            "SELECT value FROM memory WHERE key=?",
            (key,)
        )

        row = self.cur.fetchone()

        if row:
            return row[0]

        return None

    def show(self):
        self.cur.execute("SELECT * FROM memory")
        return self.cur.fetchall()
