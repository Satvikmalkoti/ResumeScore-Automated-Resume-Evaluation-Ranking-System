import re

class CGPAExtractor:
    def extract(self, text):
        # Supports: "CGPA: 8.2", "CGPA - 8", "8.5/10", "3.6/4.0", "GPA 3.8"
        num = r"(\d+(?:\.\d+)?)"
        denom = r"(10(?:\.0)?|4(?:\.0)?)"

        # Prefer explicit ratio forms first so we can normalize /4.0 → /10
        ratio_patterns = [
            rf"(?:cgpa|gpa)\s*[:\-]?\s*{num}\s*/\s*{denom}",
            rf"{num}\s*/\s*{denom}\s*(?:cgpa|gpa)?",
        ]

        for pattern in ratio_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if not match:
                continue
            try:
                val = float(match.group(1))
                den = float(match.group(2))
            except ValueError:
                continue

            # Normalize only when the scale is explicitly /4 or /4.0
            if abs(den - 4.0) < 1e-6:
                val = val * 2.5

            # Clamp to plausible ranges; keep within [0, 10]
            if 0 < val <= 10.0:
                return round(val, 2)

        # Non-ratio forms
        patterns = [
            rf"(?:cgpa|gpa)\s*(?:of\s*)?[:\-]?\s*{num}",
            rf"{num}\s*(?:cgpa|gpa)\b",
            rf"(?:grade|grade\s*point\s*average)\s*[:\-]?\s*{num}",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if not match:
                continue
            try:
                val = float(match.group(1))
            except ValueError:
                continue

            # Heuristic: values <= 4.0 might be a /4 GPA, but without explicit scale
            # we avoid converting to prevent incorrect inflation.
            if 0 < val <= 10.0:
                return round(val, 2)

        return 0.0
