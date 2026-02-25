import re

class ExtraCurricularExtractor:
    def __init__(self):
        self.keywords = [
            'volunteer', 'club', 'society', 'sports', 'captain', 'leader',
            'coordinated', 'organized', 'event', 'non-profit', 'ngo'
        ]
        
    def extract(self, text):
        activities = []
        lines = text.split('\n')
        in_section = False
        
        for line in lines:
            line_clean = line.strip().lower()
            if any(kw in line_clean for kw in ['extra-curricular', 'volunteering', 'co-curricular']):
                in_section = True
                continue
            
            if in_section:
                if any(kw in line_clean for kw in ['experience', 'education', 'skills', 'projects', 'achievements']):
                    in_section = False
                    continue
                
                if len(line.strip()) > 5:
                    activities.append(line.strip())
            else:
                if any(kw in line_clean for kw in self.keywords) and len(line_clean) < 100:
                    activities.append(line.strip())
                    
        return list(set(activities))[:5]
