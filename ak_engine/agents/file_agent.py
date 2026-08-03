from pathlib import Path

class FileAgent:

    def create_file(self, filename, content=""):
        Path(filename).write_text(content, encoding="utf-8")
        return filename

    def read_file(self, filename):
        return Path(filename).read_text(encoding="utf-8")

    def write_file(self, filename, content):
        Path(filename).write_text(content, encoding="utf-8")
        return filename

    def exists(self, filename):
        return Path(filename).exists()
