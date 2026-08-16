import sqlite3


class MemoryAgent:
    """
    Persistent SQLite memory for AK Engine.

    Supports the current category/key/value schema while remaining
    compatible with older key/value databases.
    """

    def __init__(self, db="ak_memory.db"):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

        self._ensure_schema()

    def _ensure_schema(self):
        """
        Ensure the memory table has the expected schema.

        Existing databases are preserved.
        """

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS memory(
                category TEXT NOT NULL DEFAULT 'general',
                key TEXT NOT NULL,
                value TEXT,
                PRIMARY KEY(category, key)
            )
            """
        )

        self.conn.commit()

    def remember(self, key, value, category="general"):
        """
        Store a memory entry.

        Category defaults to 'general' for backwards compatibility.
        """

        self.cur.execute(
            """
            INSERT INTO memory(category, key, value)
            VALUES (?, ?, ?)
            ON CONFLICT(category, key)
            DO UPDATE SET value = excluded.value
            """,
            (category, key, str(value)),
        )

        self.conn.commit()

    def recall(self, key, category="general"):
        """
        Retrieve a memory entry.
        """

        self.cur.execute(
            """
            SELECT value
            FROM memory
            WHERE category = ?
              AND key = ?
            """,
            (category, key),
        )

        row = self.cur.fetchone()

        if row:
            return row[0]

        return None

    def show(self):
        """
        Return all stored memories.
        """

        self.cur.execute(
            """
            SELECT category, key, value
            FROM memory
            ORDER BY category, key
            """
        )

        return self.cur.fetchall()

    def close(self):
        self.conn.close()
