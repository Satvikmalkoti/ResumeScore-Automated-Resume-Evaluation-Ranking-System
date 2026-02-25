import re

class SchoolMarksExtractor:
    def extract_school_marks(self, text):
        # Match patterns like 95%, 9.8 CGPA (10th/12th)
        patterns = [
            r'(?:10th|12th|ssc|hsc).*?(\d{2}(?:\.\d+)?)\s*%',
            r'(\d{2}(?:\.\d+)?)\s*%\s*(?:in|for)\s*(?:10th|12th)',
            r'(?:10th|12th).*?(\d\.\d+)\s*cgpa'
        ]
        
        marks = []
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    val = float(match.group(1))
                    if val <= 10: # Probably CGPA
                        marks.append(val * 10)
                    else:
                        marks.append(val)
                except ValueError:
                    continue
                    
        if marks:
            return sum(marks) / len(marks)
        return 0.0
