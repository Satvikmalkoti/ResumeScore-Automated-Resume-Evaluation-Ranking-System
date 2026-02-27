import re

class SkillFilter:
    """
    Filters out colleges/universities from extracted skills
    """
    
    def __init__(self):
        # Common college/university keywords
        self.college_keywords = [
            'iit', 'nit', 'iiit', 'bits', 'iisc', 'dtu', 'nsut',
            'university', 'college', 'institute', 'school',
            'engineering college', 'medical college', 'law school',
            'academy', 'campus', 'faculty', 'department',
            # Specific names
            'delhi technological university',
            'jawaharlal nehru university',
            'banaras hindu university',
            'jadavpur', 'amrita', 'vit', 'srm', 'thapar',
            'manipal', 'kiit', 'lpu', 'chandigarh university',
            'aktu', 'dr apj abdul kalam technical university',
        ]
        self.college_keywords = [k.lower() for k in self.college_keywords]
        
        # Words that indicate it's actually a skill
        self.skill_indicators = [
            'programming', 'language', 'framework', 'library',
            'developer', 'engineer', 'coding', 'software'
        ]
        self.skill_indicators = [k.lower() for k in self.skill_indicators]

        # Common "education artifacts" that spaCy may mislabel as skills
        self.academic_noise_patterns = [
            r'\bclass\s*(?:x|xii|10|12)\b',
            r'\b(?:10th|12th)\b',
            r'\b(?:ssc|hsc)\b',
            r'\b(?:cbse|icse)\b',
            r'\b(?:high\s*school|secondary\s*school|senior\s*secondary)\b',
        ]
    
    def is_academic_noise(self, text: str) -> bool:
        text_lower = text.lower().strip()
        if not text_lower:
            return True

        # Avoid filtering if it clearly looks like an actual skill phrase
        for skill_word in self.skill_indicators:
            if skill_word in text_lower:
                return False

        for pat in self.academic_noise_patterns:
            if re.search(pat, text_lower, flags=re.IGNORECASE):
                return True

        # Common false positives: pure grade tokens
        if re.fullmatch(r'(?:x|xii|10|12)', text_lower):
            return True

        return False
    
    def is_actually_college(self, text):
        """
        Check if extracted text is actually a college name
        """
        text_lower = text.lower()
        
        # Check for college keywords
        for keyword in self.college_keywords:
            if keyword in text_lower:
                # But if it has skill indicators, maybe keep it
                for skill_word in self.skill_indicators:
                    if skill_word in text_lower:
                        return False  # It's probably a skill (e.g., "IIT JEE coaching")
                return True  # It's a college
        
        return False
    
    def filter_skills(self, extracted_skills, education_entries=None):
        """
        Remove colleges from skills list
        """
        # Get all college names from education if provided
        college_names = []
        if education_entries:
            for edu in education_entries:
                # Handle both string and dict education entries
                if isinstance(edu, dict) and edu.get('institution'):
                    college_names.append(edu['institution'].lower())
                elif isinstance(edu, str):
                    college_names.append(edu.lower())
        
        filtered_skills = []
        for skill in extracted_skills:
            if self.is_academic_noise(skill):
                continue

            skill_lower = skill.lower()
            
            # Skip if skill matches any college name
            if any(college in skill_lower for college in college_names):
                continue
            
            # Skip if it looks like a college
            if self.is_actually_college(skill):
                continue
            
            filtered_skills.append(skill)
        
        return filtered_skills
