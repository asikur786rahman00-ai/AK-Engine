import importlib.util
import re

from ak_engine.platform.package_manager import PackageManager


class DependencyAgent:

    STDLIB = {
        "abc", "argparse", "asyncio", "base64", "collections",
        "concurrent", "contextlib", "copy", "csv", "dataclasses",
        "datetime", "decimal", "enum", "functools", "hashlib",
        "http", "importlib", "inspect", "itertools", "json",
        "logging", "math", "os", "pathlib", "pickle", "platform",
        "random", "re", "shutil", "socket", "sqlite3", "statistics",
        "string", "subprocess", "sys", "tempfile", "textwrap",
        "threading", "time", "traceback", "typing", "unittest",
        "urllib", "uuid", "warnings", "xml", "zipfile"
    }

    def __init__(self):
        self.package_manager = PackageManager()

    def extract_imports(self, code):
        packages = set()

        for match in re.finditer(
            r"^\s*(?:import|from)\s+([A-Za-z_][A-Za-z0-9_]*)",
            code,
            re.MULTILINE
        ):
            packages.add(match.group(1))

        return sorted(packages)

    def classify(self, code):
        imports = self.extract_imports(code)

        result = {
            "stdlib": [],
            "installed": [],
            "missing": [],
        }

        for package in imports:

            if package in self.STDLIB:
                result["stdlib"].append(package)
                continue

            if importlib.util.find_spec(package) is not None:
                result["installed"].append(package)
            else:
                result["missing"].append(package)

        return result

    def analyze(self, code):
        result = self.classify(code)

        print("[DependencyAgent]")
        print("Standard library:", result["stdlib"])
        print("Already installed:", result["installed"])
        print("Missing:", result["missing"])

        if not result["missing"]:
            print("✅ No installation required.")
            return result

        manager = self.package_manager.detect()

        if manager:
            print(
                f"⚠️ Missing dependencies detected. "
                f"System manager available: {manager}"
            )
        else:
            print("⚠️ Missing dependencies detected.")

        return result
