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
            'manipal', 'kiit', 'lpu', 'chandigarh university'
        ]
        
        # Words that indicate it's actually a skill
        self.skill_indicators = [
            'programming', 'language', 'framework', 'library',
            'developer', 'engineer', 'coding', 'software'
        ]
    
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
            skill_lower = skill.lower()
            
            # Skip if skill matches any college name
            if any(college in skill_lower for college in college_names):
                continue
            
            # Skip if it looks like a college
            if self.is_actually_college(skill):
                continue
            
            filtered_skills.append(skill)
        
        return filtered_skills
