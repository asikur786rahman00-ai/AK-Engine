import re


class TestEngine:
    """
    Deterministic runtime contract engine.

    Converts generated test input into structured cases and
    verifies each case independently against program output.

    The LLM may propose tests.
    The deterministic engine decides whether observable evidence
    satisfies those tests.
    """

    NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)"

    def split_input(self, raw_input):
        if not raw_input:
            return []

        return [
            line.strip()
            for line in raw_input.splitlines()
            if line.strip()
        ]

    def _arithmetic(self, a, operator, b):
        if operator == "+":
            return a + b
        if operator == "-":
            return a - b
        if operator == "*":
            return a * b
        if operator == "/":
            if b == 0:
                raise ZeroDivisionError
            return a / b

        raise ValueError(f"Unsupported operator: {operator}")

    def _parse_expression(self, value):
        pattern = (
            rf"^\s*({self.NUMBER})\s*"
            rf"([+\-*/])\s*"
            rf"({self.NUMBER})\s*$"
        )

        match = re.match(pattern, value)

        if not match:
            return None

        a = float(match.group(1))
        operator = match.group(2)
        b = float(match.group(3))

        case = {
            "a": a,
            "b": b,
            "operator": operator,
        }

        if operator == "/" and b == 0:
            case["type"] = "division_by_zero"
            return case

        case["type"] = "arithmetic"
        case["expected"] = self._arithmetic(a, operator, b)

        return case

    def _parse_menu(self, values):
        """
        Detect menu calculator sequences:

        1
        10
        5
        2
        20
        8
        ...
        q
        """

        cases = []
        i = 0
        case_id = 1

        menu_map = {
            "1": "+",
            "2": "-",
            "3": "*",
            "4": "/",
        }

        while i < len(values):
            value = values[i].strip().lower()

            if value in {"q", "quit", "exit"}:
                cases.append({
                    "id": case_id,
                    "input": value,
                    "type": "exit",
                })
                break

            if value not in menu_map:
                return None

            if i + 2 >= len(values):
                return None

            operator = menu_map[value]

            try:
                a = float(values[i + 1])
                b = float(values[i + 2])
            except ValueError:
                return None

            case = {
                "id": case_id,
                "input": f"{value} {values[i + 1]} {values[i + 2]}",
                "operator": operator,
                "a": a,
                "b": b,
            }

            if operator == "/" and b == 0:
                case["type"] = "division_by_zero"
            else:
                case["type"] = "arithmetic"
                case["expected"] = self._arithmetic(
                    a,
                    operator,
                    b,
                )

            cases.append(case)

            case_id += 1
            i += 3

        return cases

    def build_cases(self, raw_input):
        values = self.split_input(raw_input)

        if not values:
            return []

        # Try menu format first.
        menu_cases = self._parse_menu(values)

        if menu_cases is not None:
            return menu_cases

        # Expression-style format.
        cases = []

        for index, value in enumerate(values, start=1):

            lowered = value.lower()

            if lowered in {"exit", "quit"}:
                cases.append({
                    "id": index,
                    "input": value,
                    "type": "exit",
                })
                continue

            parsed = self._parse_expression(value)

            if parsed:
                parsed = {
                    "id": index,
                    "input": value,
                    **parsed,
                }
                cases.append(parsed)
                continue

            if re.search(r"[a-zA-Z]", value):
                case_type = "invalid_input"
            else:
                case_type = "generic"

            cases.append({
                "id": index,
                "input": value,
                "type": case_type,
            })

        return cases

    def _extract_numbers(self, text):
        return [
            float(x)
            for x in re.findall(
                r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)",
                text,
            )
        ]

    def _verify_arithmetic_case(self, case, output):
        """
        Verify the expected result for ONE arithmetic case.

        We intentionally look for the expected number near the
        observable result text rather than trusting an LLM.
        """

        expected = case["expected"]

        result_matches = re.findall(
            r"result\s*:\s*([^\n\r]+)",
            output,
            flags=re.IGNORECASE,
        )

        if not result_matches:
            return {
                "passed": False,
                "reason": "No observable Result: output found.",
                "expected": expected,
            }

        expected_text = f"{expected:g}"

        for result_text in result_matches:
            numbers = self._extract_numbers(result_text)

            for number in numbers:
                if abs(number - expected) <= max(
                    1e-9,
                    abs(expected) * 1e-9,
                ):
                    return {
                        "passed": True,
                        "expected": expected,
                        "observed": number,
                    }

            if expected_text in result_text:
                return {
                    "passed": True,
                    "expected": expected,
                    "observed": expected_text,
                }

        return {
            "passed": False,
            "reason": "Expected arithmetic result was not observed.",
            "expected": expected,
            "observed_results": result_matches,
        }

    def _verify_division_case(self, output):
        lowered = output.lower()

        handled = any(
            phrase in lowered
            for phrase in (
                "cannot divide",
                "division by zero",
                "divide by zero",
                "division error",
                "calculation error",
            )
        )

        return {
            "passed": handled,
            "reason": (
                None
                if handled
                else "No division-by-zero error was observed."
            ),
        }

    def _verify_invalid_case(self, output):
        lowered = output.lower()

        handled = any(
            phrase in lowered
            for phrase in (
                "invalid",
                "error",
                "unsupported",
                "valid numeric",
            )
        )

        return {
            "passed": handled,
            "reason": (
                None
                if handled
                else "Invalid input was not visibly handled."
            ),
        }

    def inspect_output(
        self,
        raw_input,
        stdout,
        stderr,
        returncode,
    ):
        cases = self.build_cases(raw_input)

        output = stdout or ""
        error = stderr or ""

        evidence = {
            "returncode": returncode,
            "stdout": output,
            "stderr": error,
            "cases": cases,
            "case_results": [],
            "checks": [],
        }

        # ---------------------------------------------------------
        # Process-level check
        # ---------------------------------------------------------

        evidence["checks"].append({
            "name": "process_completed",
            "passed": returncode == 0,
        })

        # ---------------------------------------------------------
        # Case-level verification
        # ---------------------------------------------------------

        for case in cases:

            case_type = case["type"]

            if case_type == "arithmetic":
                result = self._verify_arithmetic_case(
                    case,
                    output,
                )

            elif case_type == "division_by_zero":
                result = self._verify_division_case(
                    output,
                )

            elif case_type == "invalid_input":
                result = self._verify_invalid_case(
                    output,
                )

            elif case_type == "exit":
                lowered = output.lower()

                passed = (
                    "exit" in lowered
                    or "goodbye" in lowered
                    or returncode == 0
                )

                result = {
                    "passed": passed,
                    "reason": (
                        None
                        if passed
                        else "Clean exit was not observed."
                    ),
                }

            else:
                result = {
                    "passed": True,
                    "reason": "No specialized verifier for this case.",
                }

            case_result = {
                "id": case["id"],
                "input": case["input"],
                "type": case_type,
                **result,
            }

            evidence["case_results"].append(case_result)

        # ---------------------------------------------------------
        # Summary checks
        # ---------------------------------------------------------

        failed_cases = [
            case
            for case in evidence["case_results"]
            if not case["passed"]
        ]

        evidence["checks"].append({
            "name": "all_cases_verified",
            "passed": len(failed_cases) == 0,
            "total_cases": len(evidence["case_results"]),
            "failed_cases": len(failed_cases),
        })

        evidence["passed"] = all(
            check["passed"]
            for check in evidence["checks"]
        )

        return evidence

    def summarize(self, evidence):
        checks = evidence.get("checks", [])

        passed_checks = sum(
            1
            for check in checks
            if check.get("passed")
        )

        failed_checks = len(checks) - passed_checks

        failed_cases = [
            case
            for case in evidence.get("case_results", [])
            if not case.get("passed")
        ]

        return {
            "passed": evidence.get("passed", False),
            "total_checks": len(checks),
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "total_cases": len(
                evidence.get("case_results", [])
            ),
            "failed_cases": [
                {
                    "id": case.get("id"),
                    "input": case.get("input"),
                    "type": case.get("type"),
                    "reason": case.get("reason"),
                    "expected": case.get("expected"),
                    "observed": case.get("observed"),
                }
                for case in failed_cases
            ],
            "failed_reasons": [
                check.get("name")
                for check in checks
                if not check.get("passed")
            ],
        }
