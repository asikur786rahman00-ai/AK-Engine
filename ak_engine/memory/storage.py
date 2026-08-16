import sqlite3


class MemoryStorage:
    def __init__(self, db_path="ak_memory.db"):
        self.conn = sqlite3.connect(db_path)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            category TEXT,
            key TEXT,
            value TEXT,
            PRIMARY KEY(category, key)
        )
        """)

        self.conn.commit()

    def save(self, category, key, value):
        self.conn.execute(
            """
            INSERT OR REPLACE INTO memory(category, key, value)
            VALUES (?, ?, ?)
            """,
            (category, key, value),
        )
        self.conn.commit()

    def load(self, category, key):
        cursor = self.conn.execute(
            """
            SELECT value FROM memory
            WHERE category=? AND key=?
            """,
            (category, key),
        )

        row = cursor.fetchone()
        return row[0] if row else None

    def list_category(self, category):
        cursor = self.conn.execute(
            """
            SELECT key, value
            FROM memory
            WHERE category=?
            ORDER BY key
            """,
            (category,),
        )

        return cursor.fetchall()
