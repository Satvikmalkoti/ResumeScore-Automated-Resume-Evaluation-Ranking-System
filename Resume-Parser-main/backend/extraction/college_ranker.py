"""
College Ranker - 2% of total score
Handles multiple NIRF ranking files across different categories
"""

import pandas as pd
import os
import glob
import re
from pathlib import Path

class CollegeRanker:
    """
    Assigns tier based on college rankings from multiple NIRF files
    Supports: Engineering, Medical, Innovation, Architecture, etc.
    """
    
    def __init__(self, rankings_dir=None):
        """
        Initialize with multiple NIRF ranking files
        
        Args:
            rankings_dir: Path to folder containing all NIRF CSV files
                         If None, uses default hardcoded rankings
        """
        self.rankings = {}  # college_name -> (rank, category)
        self.category_files = []
        
        if rankings_dir and os.path.exists(rankings_dir):
            self._load_all_rankings(rankings_dir)
        else:
            self._load_default_rankings()
        
        # Cache for faster lookups
        self.tier_cache = {}
        
        print(f"✅ Loaded {len(self.rankings)} college rankings from {len(self.category_files)} categories")
    
    def _load_all_rankings(self, rankings_dir):
        """
        Load all CSV files from the rankings directory
        """
        csv_files = glob.glob(os.path.join(rankings_dir, "*.csv"))
        
        for csv_file in csv_files:
            category = self._get_category_from_filename(csv_file)
            self.category_files.append(category)
            self._load_rankings_file(csv_file, category)
    
    def _get_category_from_filename(self, filename):
        """
        Extract category from filename
        Example: NIRF_Engineering_2024.csv -> Engineering
                NIRF_Innovation_2024.csv -> Innovation
        """
        base = os.path.basename(filename)
        # Remove extension and split
        parts = base.replace('.csv', '').split('_')
        if len(parts) >= 2:
            return parts[1]  # Returns: Engineering, Innovation, Medical, etc.
        return "General"
    
    def _load_rankings_file(self, csv_path, category):
        """
        Load a single NIRF CSV file
        Handles different column name variations
        """
        try:
            df = pd.read_csv(csv_path)
            
            # Try to identify college name and rank columns
            college_col = self._find_college_column(df)
            rank_col = self._find_rank_column(df)
            
            if college_col and rank_col:
                for _, row in df.iterrows():
                    college_name = self._clean_college_name(str(row[college_col]))
                    try:
                        rank_val = row[rank_col]
                        # Handle potential non-numeric rank strings
                        if isinstance(rank_val, str):
                            rank_match = re.search(r'(\d+)', rank_val)
                            rank = int(rank_match.group(1)) if rank_match else 0
                        else:
                            rank = int(rank_val)
                            
                        if rank == 0: continue

                        # Store with category context
                        self.rankings[college_name] = {
                            'rank': rank,
                            'category': category,
                            'original_name': str(row[college_col])
                        }
                    except (ValueError, TypeError, AttributeError):
                        continue
                        
                print(f"  ✓ Loaded {len(df)} colleges from {category} rankings")
            else:
                print(f"  ✗ Could not identify columns in {os.path.basename(csv_path)}")
                
        except Exception as e:
            print(f"  ✗ Error loading {csv_path}: {e}")
    
    def _find_college_column(self, df):
        """
        Find the college name column (handles variations)
        """
        possible_names = [
            'college', 'institute', 'university', 'name',
            'College', 'Institute', 'University', 'Name',
            'institution', 'Institution'
        ]
        
        for col in df.columns:
            col_str = str(col).lower()
            if any(name.lower() in col_str for name in possible_names):
                return col
        
        # If no match, use first string column
        for col in df.columns:
            if df[col].dtype == 'object':
                return col
        
        return None
    
    def _find_rank_column(self, df):
        """
        Find the rank column (handles variations)
        """
        possible_names = ['rank', 'Rank', 'RANK', 'score', 'Score', 'position']
        
        for col in df.columns:
            col_str = str(col).lower()
            if any(name.lower() in col_str for name in possible_names):
                return col
        
        # If no match, use first numeric column
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                return col
        
        return None
    
    def _clean_college_name(self, name):
        """
        Clean college name for matching
        """
        # Remove quotes
        name = name.replace('"', '').replace("'", "")
        # Remove extra spaces
        name = ' '.join(name.split())
        # Convert to lowercase for matching
        return name.lower().strip()
    
    def _load_default_rankings(self):
        """
        Fallback: Hardcoded rankings if no CSV files found
        """
        print("⚠️ Using default hardcoded rankings (no CSV files found)")
        
        # Tier 1 Colleges (Rank ≤ 50)
        tier1_colleges = [
            "indian institute of technology madras",
            "indian institute of technology delhi",
            "indian institute of technology bombay",
            "indian institute of technology kanpur",
            "indian institute of technology kharagpur",
            "indian institute of technology roorkee",
            "indian institute of technology guwahati",
            "indian institute of technology hyderabad",
            "indian institute of technology indore",
            "national institute of technology tiruchirappalli",
            "jadavpur university",
            "birla institute of technology and science pilani",
            "indian institute of science",
            "university of delhi",
            "jawaharlal nehru university",
            "banaras hindu university",
            "amrita vishwa vidyapeetham",
            "anna university",
        ]
        
        # Tier 2 Colleges (Rank 51-200)
        tier2_colleges = [
            "vellore institute of technology",
            "srm institute",
            "thapar institute",
            "kiit university",
            "lovely professional university",
            "chandigarh university",
            "amity university",
            "symbiosis international",
            "manipal university",
            "sathyabama institute",
            "delhi technological university",
        ]
        
        # Add to rankings
        for idx, college in enumerate(tier1_colleges, 1):
            self.rankings[college] = {'rank': idx, 'category': 'default', 'original_name': college}
        
        for idx, college in enumerate(tier2_colleges, 51):
            self.rankings[college] = {'rank': idx, 'category': 'default', 'original_name': college}
    
    def get_college_info(self, college_name):
        """
        Get ranking info for a college
        """
        if not college_name:
            return None
            
        cleaned = self._clean_college_name(college_name)
        
        # Check cache first
        if cleaned in self.tier_cache:
            return self.tier_cache[cleaned]
        
        # Direct match
        if cleaned in self.rankings:
            info = self.rankings[cleaned]
            self.tier_cache[cleaned] = info
            return info
        
        # Partial match (search in all stored colleges)
        for stored_name, info in self.rankings.items():
            if (stored_name in cleaned or cleaned in stored_name) and len(cleaned) > 5:
                self.tier_cache[cleaned] = info
                return info
        
        return None
    
    def get_tier(self, college_name):
        """
        Get tier for college (1=best, 2=good, 3=other)
        """
        info = self.get_college_info(college_name)
        
        if not info:
            return 3  # Unknown college -> Tier 3
        
        rank = info['rank']
        
        if rank <= 50:
            return 1  # Top tier (2 points)
        elif rank <= 200:
            return 2  # Good tier (1 point)
        else:
            return 3  # Other (0.5 points)
    
    def score_tier(self, tier):
        """
        Convert tier to score (max 2 points)
        """
        return {
            1: 2.0,   # Top tier (Rank 1-50)
            2: 1.0,   # Good tier (Rank 51-200)
            3: 0.5    # Other colleges
        }.get(tier, 0)
    
    def get_rank_details(self, college_name):
        """
        Get detailed ranking information for a college
        """
        info = self.get_college_info(college_name)
        
        if not info:
            return {
                'found': False,
                'tier': 3,
                'score': 0.5,
                'message': 'College not found in NIRF rankings'
            }
        
        tier = self.get_tier(college_name)
        
        return {
            'found': True,
            'college': info.get('original_name', college_name),
            'rank': info['rank'],
            'category': info.get('category', 'unknown'),
            'tier': tier,
            'score': self.score_tier(tier),
            'message': f"Ranked #{info['rank']} in {info.get('category', 'NIRF')} category"
        }

    def get_statistics(self):
        """
        Get statistics about loaded rankings
        """
        if not self.rankings:
            return {'total': 0}
        
        return {
            'total_colleges': len(self.rankings),
            'categories': list(set([info.get('category', 'unknown') for info in self.rankings.values()]))
        }
