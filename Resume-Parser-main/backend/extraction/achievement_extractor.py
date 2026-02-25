import re

class AchievementExtractor:
    def __init__(self):
        self.keywords = ['award', 'honor', 'distinction', 'achievement', 'scholarship', 'placed', 'won']
        
    def extract(self, text):
        achievements = []
        lines = text.split('\n')
        in_section = False
        
        for line in lines:
            line_clean = line.strip().lower()
            if any(kw in line_clean for kw in ['achievements', 'honors', 'awards']):
                in_section = True
                continue
            
            if in_section:
                if any(kw in line_clean for kw in ['experience', 'education', 'skills', 'projects']):
                    in_section = False
                    continue
                
                if len(line.strip()) > 5:
                    achievements.append(line.strip())
            else:
                # Catch individual achievement lines even if not in section
                if any(kw in line_clean for kw in self.keywords) and len(line_clean) < 100:
                    achievements.append(line.strip())
                    
        return list(set(achievements))[:10]
