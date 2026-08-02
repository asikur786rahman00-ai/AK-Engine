import sqlite3


class MemoryStorage:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            key TEXT,
            value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(category, key)
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
        cur = self.conn.execute(
            """
            SELECT value
            FROM memory
            WHERE category=? AND key=?
            """,
            (category, key),
        )

        row = cur.fetchone()
        return row[0] if row else None

    def delete(self, category, key):
        self.conn.execute(
            """
            DELETE FROM memory
            WHERE category=? AND key=?
            """,
            (category, key),
        )
        self.conn.commit()
