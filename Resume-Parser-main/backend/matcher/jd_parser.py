"""
Job Description Parser - Extracts requirements from JD
Uses regex patterns (no AI model needed)
"""

import re
from typing import List, Dict, Set

class JDParser:
    def __init__(self):
        # Skill section patterns
        self.skill_patterns = [
            r'(?i)required skills?:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'(?i)preferred skills?:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'(?i)qualifications?:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'(?i)requirements?:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'(?i)what you.*?ll need:?\s*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'(?i)about you:?\s*(.*?)(?=\n\n|\n[A-Z]|$)'
        ]
        
        # Experience pattern
        self.exp_pattern = r'(?i)(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience'
        
        # Education pattern
        self.edu_pattern = r'(?i)(bachelor|master|phd|b\.tech|m\.tech|degree).*?(required|preferred)'
    
    def extract_required_skills(self, jd_text: str) -> Set[str]:
        """Extract skills explicitly mentioned as required"""
        skills = set()
        
        for pattern in self.skill_patterns:
            matches = re.finditer(pattern, jd_text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                section = match.group(1)
                # Split by common delimiters
                items = re.split(r'[,•\n;]', section)
                for item in items:
                    item = item.strip()
                    # Filter out short items and numbers
                    if item and len(item) > 2 and not re.match(r'^\d+$', item):
                        skills.add(item.lower())
        
        # If no skills found via patterns, fallback to some basic cleanup of the whole text
        if not skills:
            # This is a very basic fallback
            pass
            
        return skills
    
    def extract_experience(self, jd_text: str) -> float:
        """Extract required years of experience"""
        matches = re.findall(self.exp_pattern, jd_text, re.IGNORECASE)
        if matches:
            try:
                return float(matches[0])
            except:
                return 0.0
        return 0.0
    
    def parse_job_description(self, jd_text: str) -> Dict:
        """Complete JD parsing"""
        return {
            'required_skills': list(self.extract_required_skills(jd_text)),
            'years_experience': self.extract_experience(jd_text),
            'title': self._extract_title(jd_text),
            'full_text': jd_text
        }
    
    def _extract_title(self, jd_text: str) -> str:
        """Extract job title from first line"""
        lines = jd_text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) < 100 and not line.startswith('http'):
                return line
        return "Job Position"
