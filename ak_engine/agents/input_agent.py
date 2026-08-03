class InputAgent:
    def answer(self, prompt):
        prompt = prompt.lower()

        if "choice" in prompt:
            return "5\n"

        if "yes/no" in prompt:
            return "yes\n"

        if "name" in prompt:
            return "AK\n"

        return "\n"
