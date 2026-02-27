import re

class DegreeClassifier:
    def __init__(self):
        self.degree_map = {
            'phd': ['ph.d', 'doctorate', 'phd'],
            'masters': ['m.tech', 'm.e.', 'msc', 'master', 'mba', 'm.s.'],
            'bachelors': ['b.tech', 'b.e.', 'bsc', 'bachelor', 'b.s.'],
            'diploma': ['diploma']
        }
        
    def get_highest_degree(self, text):
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in self.degree_map['phd']):
            return 'phd'
        if any(kw in text_lower for kw in self.degree_map['masters']):
            return 'masters'
        if any(kw in text_lower for kw in self.degree_map['bachelors']):
            return 'bachelors'
        if any(kw in text_lower for kw in self.degree_map['diploma']):
            return 'diploma'
            
        return 'unknown'
