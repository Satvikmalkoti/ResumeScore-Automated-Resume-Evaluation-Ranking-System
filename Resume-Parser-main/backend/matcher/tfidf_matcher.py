"""
TF-IDF Matcher - Compares resume vs job description using cosine similarity
NO new AI models - uses sklearn TF-IDF
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List, Set, Union

class TFIDFJobMatcher:
    """
    Job matching using TF-IDF and cosine similarity
    Industry standard approach - no LLMs needed
    """
    
    def __init__(self):
        # TF-IDF vectorizer with smart parameters
        self.vectorizer = TfidfVectorizer(
            max_features=1000,           # Limit features
            stop_words='english',         # Remove common words
            ngram_range=(1, 2),           # Use unigrams and bigrams
            min_df=1,                      # Minimum document frequency
            max_df=0.8                     # Ignore too common terms
        )
        
        # Scoring weights (based on research)
        self.weights = {
            'required_skills': 0.50,  # 50%
            'preferred_skills': 0.25,  # 25%
            'experience': 0.15,         # 15%
            'education': 0.10           # 10%
        }
        
        print("✅ TF-IDF Matcher initialized")
    
    def calculate_similarity(self, resume_text: str, jd_text: str) -> float:
        """
        Calculate cosine similarity between resume and JD
        Returns score between 0-1
        """
        try:
            # Create document pair
            documents = [resume_text, jd_text]
            
            # Fit and transform
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception as e:
            print(f"Error in similarity calculation: {e}")
            return 0.0
    
    def get_key_terms(self, text: str, top_n: int = 10) -> List[str]:
        """
        Extract top TF-IDF terms from text
        Useful for debugging and explainability
        """
        try:
            # Transform single document
            tfidf_matrix = self.vectorizer.fit_transform([text])
            
            # Get feature names
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Get scores for first document
            scores = tfidf_matrix.toarray()[0]
            
            # Sort and get top terms
            top_indices = scores.argsort()[-top_n:][::-1]
            top_terms = [feature_names[i] for i in top_indices if scores[i] > 0]
            
            return top_terms
        except:
            return []
    
    def calculate_skill_match(self, resume_skills: Union[Set[str], List[str]], jd_skills: Union[Set[str], List[str]]) -> Dict:
        """
        Calculate skill-based match (more accurate than TF-IDF alone)
        """
        resume_skills_set = set([s.lower() for s in resume_skills])
        jd_skills_set = set([s.lower() for s in jd_skills])
        
        if not jd_skills_set:
            return {'score': 0, 'matched': [], 'missing': []}
        
        # Find matches
        matched = resume_skills_set & jd_skills_set
        missing = jd_skills_set - resume_skills_set
        
        # Calculate score
        score = len(matched) / len(jd_skills_set) if jd_skills_set else 0
        
        return {
            'score': round(score * 100, 2),
            'matched': list(matched),
            'missing': list(missing)
        }
    
    def calculate_experience_match(self, resume_exp: float, jd_exp: float) -> float:
        """
        Calculate experience match percentage
        """
        if jd_exp <= 0:
            return 50.0  # Default if not specified
        
        ratio = resume_exp / jd_exp if jd_exp > 0 else 0
        return min(ratio * 100, 100)  # Cap at 100%
    
    def comprehensive_match(self, 
                           resume_text: str,
                           jd_text: str,
                           resume_skills: Union[Set[str], List[str]],
                           jd_skills: Union[Set[str], List[str]],
                           resume_exp: float,
                           jd_exp: float) -> Dict:
        """
        Complete matching with all components
        """
        # 1. TF-IDF similarity (overall content match)
        tfidf_score = self.calculate_similarity(resume_text, jd_text)
        
        # 2. Skill match (keyword based)
        skill_match = self.calculate_skill_match(resume_skills, jd_skills)
        
        # 3. Experience match
        exp_match = self.calculate_experience_match(resume_exp, jd_exp)
        
        # 4. Weighted total score (combines both methods)
        weighted_score = (
            (skill_match['score'] / 100 * 0.7) +  # Skills matter more
            (tfidf_score * 0.3)                    # Content similarity
        ) * 100
        
        return {
            'total_score': round(weighted_score, 2),
            'tfidf_similarity': round(tfidf_score * 100, 2),
            'skill_match': skill_match,
            'experience_match': round(exp_match, 2),
            'top_terms': {
                'resume': self.get_key_terms(resume_text, 5),
                'job': self.get_key_terms(jd_text, 5)
            }
        }
