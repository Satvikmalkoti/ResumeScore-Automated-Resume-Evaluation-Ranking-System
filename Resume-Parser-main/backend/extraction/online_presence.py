import re

class OnlinePresenceExtractor:
    def extract(self, text):
        presence = {
            'github': None,
            'linkedin': None,
            'portfolio': None
        }
        
        # GitHub
        github_match = re.search(r'github\.com/([\w-]+)', text, re.IGNORECASE)
        if github_match:
            presence['github'] = f"https://github.com/{github_match.group(1)}"
            
        # LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/([\w-]+)', text, re.IGNORECASE)
        if linkedin_match:
            presence['linkedin'] = f"https://linkedin.com/in/{linkedin_match.group(1)}"
            
        # Portfolio / Personal Website (generic)
        # Avoid matching common domains
        portfolio_match = re.search(r'(?:portfolio|website)[:\s]+(https?://[^\s,]+)', text, re.IGNORECASE)
        if portfolio_match:
            presence['portfolio'] = portfolio_match.group(1)
            
        return presence
