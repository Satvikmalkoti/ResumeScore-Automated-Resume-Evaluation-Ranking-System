import re

class CGPAExtractor:
    def extract(self, text):
        # Match patterns like 8.5/10, 3.8/4.0, CGPA: 9.2, GPA 3.5/4
        patterns = [
            r'(?:cgpa|gpa)[:\s]+(\d\.\d+)',
            r'(\d\.\d+)\s*/\s*(?:10|10\.0|4|4\.0)',
            r'(\d\.\d+)\s*(?:cgpa|gpa)',
            r'(?:cgpa|gpa)\s+of\s+(\d\.\d+)',
            r'grade[:\s]+(\d\.\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    val = float(match.group(1))
                    # Basic heuristic: if > 4.0 and < 10.0, it's likely a 10-point scale
                    # If <= 4.0 it could be either, but we'll return as is.
                    return val
                except ValueError:
                    continue
        return 0.0
