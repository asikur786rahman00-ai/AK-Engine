class MemorySearch:
    def __init__(self, storage):
        self.storage = storage

    def search(self, keyword):
        cursor = self.storage.conn.execute(
            """
            SELECT category, key, value
            FROM memory
            WHERE category LIKE ?
               OR key LIKE ?
               OR value LIKE ?
            ORDER BY category, key
            """,
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
        )

        return cursor.fetchall()
