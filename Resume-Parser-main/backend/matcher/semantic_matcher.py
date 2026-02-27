"""
Semantic Job Matcher using Sentence-Transformers
Understands synonyms: "Web Dev" ~ "Frontend Developer"
Runs locally - FREE and FAST
"""

from sentence_transformers import SentenceTransformer, util
import numpy as np
from typing import List, Dict, Tuple
import torch

class SemanticJobMatcher:
    """
    Uses all-MiniLM-L6-v2 (lightweight, 80MB) for semantic understanding
    No API calls - runs entirely locally
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        print(f"[PROCESS] Loading semantic model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
        print(f"[SUCCESS] Semantic model loaded on {self.device}")
        
        # Cache for embeddings
        self.embedding_cache = {}
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Get or compute embedding with caching"""
        if text in self.embedding_cache:
            return self.embedding_cache[text]
        
        embedding = self.model.encode(text, convert_to_tensor=True)
        self.embedding_cache[text] = embedding
        return embedding
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """Compute semantic similarity between two texts"""
        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)
        
        # Cosine similarity
        similarity = util.pytorch_cos_sim(emb1, emb2).item()
        return float(similarity)
    
    def compare_skill_sets(self, 
                          resume_skills: List[str], 
                          jd_skills: List[str],
                          threshold: float = 0.7) -> Dict:
        """
        Semantic skill matching - understands synonyms
        e.g., "React.js" ~ "React" ~ "ReactJS"
        """
        if not jd_skills:
            return {
                'score': 0,
                'matched_skills': [],
                'unmatched_skills': [],
                'semantic_threshold': threshold
            }
        
        matched = []
        missing = []
        skill_scores = {}
        
        # Get embeddings for JD skills
        jd_embeddings = [self.get_embedding(skill) for skill in jd_skills]
        
        for resume_skill in resume_skills:
            res_emb = self.get_embedding(resume_skill)
            best_match = None
            best_score = 0
            
            for jd_skill, jd_emb in zip(jd_skills, jd_embeddings):
                score = util.pytorch_cos_sim(res_emb, jd_emb).item()
                if score > best_score:
                    best_score = score
                    best_match = jd_skill
            
            if best_score >= threshold:
                matched.append({
                    'resume_skill': resume_skill,
                    'matches': best_match,
                    'confidence': round(best_score * 100, 2)
                })
                skill_scores[best_match] = max(skill_scores.get(best_match, 0), best_score)
            else:
                missing.append(resume_skill)
        
        # Calculate match score
        matched_count = len(set(m['matches'] for m in matched))
        match_score = (matched_count / len(jd_skills)) * 100 if jd_skills else 0
        
        return {
            'score': round(match_score, 2),
            'matched_skills': matched,
            'unmatched_skills': missing[:10],  # Limit for display
            'semantic_threshold': threshold
        }
    
    def hybrid_match(self,
                    resume_text: str,
                    jd_text: str,
                    resume_skills: List[str],
                    jd_skills: List[str],
                    tfidf_score: float) -> Dict:
        """
        Combine semantic + TF-IDF for best results
        """
        # Semantic similarity between full texts
        semantic_sim = self.compute_similarity(resume_text, jd_text)
        
        # Semantic skill matching
        skill_match = self.compare_skill_sets(resume_skills, jd_skills)
        
        # Hybrid score (70% semantic, 30% TF-IDF)
        hybrid = (semantic_sim * 0.4 + 
                 (skill_match['score'] / 100) * 0.3 + 
                 tfidf_score * 0.3) * 100
        
        return {
            'hybrid_score': round(hybrid, 2),
            'semantic_similarity': round(semantic_sim * 100, 2),
            'skill_match': skill_match,
            'tfidf_contribution': round(tfidf_score * 100, 2)
        }
