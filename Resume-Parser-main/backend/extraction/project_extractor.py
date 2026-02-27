import re

class ProjectExtractor:
    def __init__(self):
        self.project_keywords = [
            'project', 'personal project', 'academic project', 'side project',
            'developed', 'built', 'created', 'implemented'
        ]
        
    def extract(self, text):
        """
        Extract project-like sections from text.
        Returns a list of project descriptions.
        """
        # Search for project headers or bullet points under project sections
        projects = []
        
        # Simple heuristic: Look for lines starting with bullet points or keywords in a project section
        lines = text.split('\n')
        in_project_section = False
        for line in lines:
            line_clean = line.strip().lower()
            if any(kw in line_clean for kw in ['projects', 'key projects', 'notable projects']):
                in_project_section = True
                continue
            
            if in_project_section:
                # If we hit another major section, stop
                if any(kw in line_clean for kw in ['experience', 'education', 'skills', 'achievements']):
                    in_project_section = False
                    continue
                
                # If it's a non-empty line and looks like a project title or description
                if len(line.strip()) > 10:
                    projects.append(line.strip())
        
        # Limit to reasonable number
        return projects[:10]
