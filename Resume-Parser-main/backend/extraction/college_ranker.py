import pandas as pd
import os

class CollegeRanker:
    def __init__(self, rankings_path):
        self.rankings = {}
        if os.path.exists(rankings_path):
            try:
                df = pd.read_csv(rankings_path)
                # Assume columns 'College' and 'Rank'
                for _, row in df.iterrows():
                    self.rankings[str(row['College']).lower()] = int(row['Rank'])
            except Exception:
                pass
                
    def get_tier(self, college_name):
        if not college_name:
            return 3
            
        name_lower = college_name.lower()
        # Search for college name in rankings
        for college, rank in self.rankings.items():
            if college in name_lower or name_lower in college:
                if rank <= 50:
                    return 1
                if rank <= 200:
                    return 2
        return 3
