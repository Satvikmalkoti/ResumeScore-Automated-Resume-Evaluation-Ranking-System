"""
Semantic Job Matcher using Sentence-Transformers
Understands synonyms: "Web Dev" ~ "Frontend Developer"
Runs locally - FREE and FAST
"""

from __future__ import annotations

from typing import List, Dict
import re

try:
    from sentence_transformers import SentenceTransformer, util  # type: ignore
except Exception:
    SentenceTransformer = None
    util = None

try:
    import torch  # type: ignore
except Exception:
    torch = None

class SemanticJobMatcher:
    """
    Uses all-MiniLM-L6-v2 (lightweight, 80MB) for semantic understanding
    No API calls - runs entirely locally
    """
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.available = False
        self.model = None
        self.device = 'cpu'
        self.embedding_cache = {}

        if SentenceTransformer is None or util is None or torch is None:
            print("[WARNING] sentence-transformers/torch not available - semantic matching disabled")
            return

        try:
            print(f"[PROCESS] Loading semantic model: {model_name}...")
            self.model = SentenceTransformer(model_name)
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
            self.model.to(self.device)
            self.available = True
            print(f"[SUCCESS] Semantic model loaded on {self.device}")
        except Exception as e:
            print(f"[WARNING] Semantic model init failed - semantic matching disabled: {e}")
            self.available = False
        
    def _normalize_skill(self, s: str) -> str:
        s = (s or "").lower().strip()
        s = re.sub(r"[^a-z0-9\.\+\#\s]", " ", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s
    
    def get_embedding(self, text: str):
        """Get or compute embedding with caching"""
        if not self.available:
            return None

        if text in self.embedding_cache:
            return self.embedding_cache[text]
        
        embedding = self.model.encode(text, convert_to_tensor=True)
        self.embedding_cache[text] = embedding
        return embedding
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """Compute semantic similarity between two texts"""
        if not self.available:
            return 0.0

        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)
        
        # Cosine similarity
        similarity = util.pytorch_cos_sim(emb1, emb2).item()
        return float(similarity)
    
    def _basic_skill_overlap(self, resume_skills: List[str], jd_skills: List[str]) -> Dict:
        jd_norm = [self._normalize_skill(s) for s in jd_skills if s]
        res_norm = [self._normalize_skill(s) for s in resume_skills if s]

        jd_set = set(jd_norm)
        res_set = set(res_norm)
        if not jd_set:
            return {
                'score': 0,
                'matched_skills': [],
                'unmatched_skills': [],
                'semantic_threshold': None,
                'semantic_disabled': True
            }

        matched = []
        for raw in resume_skills:
            r = self._normalize_skill(raw)
            if r and r in jd_set:
                matched.append({
                    'resume_skill': raw,
                    'matches': raw,
                    'confidence': 100.0
                })

        matched_count = len(set(self._normalize_skill(m['matches']) for m in matched))
        match_score = (matched_count / len(jd_set)) * 100 if jd_set else 0

        unmatched = [s for s in resume_skills if self._normalize_skill(s) and self._normalize_skill(s) not in jd_set]

        return {
            'score': round(match_score, 2),
            'matched_skills': matched,
            'unmatched_skills': unmatched[:10],
            'semantic_threshold': None,
            'semantic_disabled': True
        }

    def compare_skill_sets(self, 
                          resume_skills: List[str], 
                          jd_skills: List[str],
                          threshold: float = 0.7) -> Dict:
        """
        Semantic skill matching - understands synonyms
        e.g., "React.js" ~ "React" ~ "ReactJS"
        """
        if not self.available:
            return self._basic_skill_overlap(resume_skills, jd_skills)

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
        if not self.available:
            skill_match = self._basic_skill_overlap(resume_skills, jd_skills)
            # Conservative fallback: combine TF-IDF + exact skill overlap
            overlap = (skill_match.get('score', 0) / 100.0)
            hybrid = (tfidf_score * 0.7 + overlap * 0.3) * 100
            return {
                'hybrid_score': round(hybrid, 2),
                'semantic_similarity': 0.0,
                'skill_match': skill_match,
                'tfidf_contribution': round(tfidf_score * 100, 2),
                'semantic_disabled': True
            }

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
