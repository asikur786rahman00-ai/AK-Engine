import ast


BUILTIN = {
    "os",
    "sys",
    "json",
    "math",
    "time",
    "random",
    "sqlite3",
    "typing",
    "pathlib",
    "collections",
    "itertools",
    "threading",
    "asyncio",
    "logging",
    "csv",
    "datetime",
    "subprocess",
    "re"
}


PACKAGE_MAP = {
    "bs4": "beautifulsoup4",
    "cv2": "opencv-python",
    "PIL": "pillow",
    "sklearn": "scikit-learn",
    "yaml": "pyyaml"
}


class ImportScanner:

    def scan(self, code):

        tree = ast.parse(code)

        packages = set()

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:

                    name = alias.name.split(".")[0]

                    if name not in BUILTIN:

                        packages.add(
                            PACKAGE_MAP.get(name, name.lower())
                        )

            elif isinstance(node, ast.ImportFrom):

                if node.module:

                    name = node.module.split(".")[0]

                    if name not in BUILTIN:

                        packages.add(
                            PACKAGE_MAP.get(name, name.lower())
                        )

        return sorted(packages)
