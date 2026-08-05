import ast

class ValidatorAgent:

    def is_python(self, code):

        try:
            ast.parse(code)
            return True

        except Exception:
            return False

    def looks_like_explanation(self, code):

        bad_words = [
            "here is",
            "this code",
            "the problem",
            "an elegant way",
            "explanation",
            "markdown",
            "```"
        ]

        text = code.lower()

        return any(word in text for word in bad_words)
