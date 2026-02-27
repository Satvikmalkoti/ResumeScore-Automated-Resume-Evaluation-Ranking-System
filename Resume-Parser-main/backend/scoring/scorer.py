class ResumeScorer:
    """
    Scores resume based on extracted entities
    Implements exact 100-point weights from problem statement
    """
    
    def __init__(self):
        self.weights = {
            'internships': 0.20,        # 20 points
            'skills': 0.20,              # 20 points
            'projects': 0.15,             # 15 points
            'cgpa': 0.10,                  # 10 points
            'achievements': 0.10,          # 10 points
            'experience': 0.05,            # 5 points
            'extra_curricular': 0.05,      # 5 points
            'language': 0.03,               # 3 points
            'online_presence': 0.03,        # 3 points
            'degree_type': 0.03,            # 3 points
            'college_ranking': 0.02,        # 2 points
            'school_marks': 0.02            # 2 points
        }
        
        self.caps = {
            'internships': 3,        # Max 3 internships
            'skills': 20,             # Max 20 skills
            'projects': 5,             # Max 5 projects
            'experience_years': 5,     # Max 5 years
            'languages': 3,             # Max 3 languages
            'achievements': 10,         # Max 10 achievements
            'extra_curricular': 5       # Max 5 activities
        }
    
    def calculate_score(self, extracted_data):
        """
        Calculate final score out of 100
        Returns dict with total and breakdown
        """
        scores = {}
        
        # Internships (20 points)
        intern_count = len(extracted_data.get('internships', []))
        capped = min(intern_count, self.caps['internships'])
        scores['internships'] = (capped / self.caps['internships']) * 20
        
        # Skills (20 points)
        skill_count = len(extracted_data.get('skills', []))
        capped = min(skill_count, self.caps['skills'])
        scores['skills'] = (capped / self.caps['skills']) * 20
        
        # Projects (15 points)
        proj_count = len(extracted_data.get('projects', []))
        capped = min(proj_count, self.caps['projects'])
        scores['projects'] = (capped / self.caps['projects']) * 15
        
        # CGPA (10 points)
        cgpa = extracted_data.get('cgpa', 0)
        scores['cgpa'] = min(cgpa, 10)
        
        # Achievements (10 points)
        ach_count = len(extracted_data.get('achievements', []))
        capped = min(ach_count, self.caps['achievements'])
        scores['achievements'] = (capped / self.caps['achievements']) * 10
        
        # Experience (5 points)
        exp_years = extracted_data.get('experience_years', 0)
        capped = min(exp_years, self.caps['experience_years'])
        scores['experience'] = (capped / self.caps['experience_years']) * 5
        
        # Extra-curricular (5 points)
        ec_count = len(extracted_data.get('extra_curricular', []))
        capped = min(ec_count, self.caps['extra_curricular'])
        scores['extra_curricular'] = (capped / self.caps['extra_curricular']) * 5
        
        # Languages (3 points)
        lang_count = len(extracted_data.get('languages', []))
        capped = min(lang_count, self.caps['languages'])
        scores['language'] = (capped / self.caps['languages']) * 3
        
        # Online Presence (3 points)
        online = extracted_data.get('online_presence', {})
        online_score = 0
        if online.get('github'): online_score += 1
        if online.get('linkedin'): online_score += 1
        if online.get('portfolio'): online_score += 1
        scores['online_presence'] = online_score
        
        # Degree Type (3 points)
        degree = extracted_data.get('degree_type', 'unknown')
        degree_scores = {
            'phd': 3.0,
            'masters': 2.5,
            'bachelors': 2.0,
            'diploma': 1.0,
            'unknown': 0
        }
        scores['degree_type'] = degree_scores.get(degree, 0)
        
        # College Ranking (2 points)
        tier = extracted_data.get('college_tier', 3)
        tier_scores = {1: 2.0, 2: 1.0, 3: 0.5}
        scores['college_ranking'] = tier_scores.get(tier, 0)
        
        # School Marks (2 points)
        school_avg = extracted_data.get('school_marks_avg', 0)
        scores['school_marks'] = (school_avg / 100) * 2 # Fixed from / 10 to / 100 for percentage
        
        total = sum(scores.values())
        
        return {
            'total': round(total, 2),
            'breakdown': scores,
            'max_possible': 100
        }
