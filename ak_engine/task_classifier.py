CODING_WORDS = {
    "code","coding","program","programming","python","java",
    "javascript","typescript","react","vue","angular",
    "html","css","node","express","flask","django",
    "fastapi","api","backend","frontend","database",
    "sql","mysql","postgres","mongodb","docker",
    "kubernetes","linux","bash","shell","git",
    "github","bot","telegram","discord","web",
    "website","app","android","ios","bug","debug",
    "fix","error","exception","function","class",
    "script","automation","algorithm"
}

REASONING_WORDS = {
    "explain",
    "reason",
    "analyze",
    "analysis",
    "compare",
    "proof",
    "quantum",
    "physics",
    "chemistry",
    "biology",
    "mathematics",
    "math",
    "logic",
    "algorithm",
    "architecture",
    "strategy",
    "theorem"
}

WRITING_WORDS = {
    "write","story","article","essay",
    "email","blog","caption","post",
    "thread","rewrite","grammar"
}

class TaskClassifier:
    def classify(self, text: str) -> str:
        text = text.lower()

        if any(word in text for word in CODING_WORDS):
            return "coding"

        if any(word in text for word in REASONING_WORDS):
            return "reasoning"

        if any(word in text for word in WRITING_WORDS):
            return "writing"

        return "general"
