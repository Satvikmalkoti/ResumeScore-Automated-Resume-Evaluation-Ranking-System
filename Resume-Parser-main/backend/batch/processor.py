import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
from pathlib import Path
import json
import spacy
import pdfplumber
import docx2txt
import io

from scoring.scorer import ResumeScorer
from extraction.project_extractor import ProjectExtractor
from extraction.achievement_extractor import AchievementExtractor
from extraction.cgpa_extractor import CGPAExtractor
from extraction.school_marks import SchoolMarksExtractor
from extraction.online_presence import OnlinePresenceExtractor
from extraction.extra_curricular import ExtraCurricularExtractor
from extraction.degree_classifier import DegreeClassifier
from extraction.college_ranker import CollegeRanker

class BatchResumeProcessor:
    def __init__(self, model_path="./model"):
        self.scorer = ResumeScorer()
        try:
            self.nlp = spacy.load(model_path)
        except Exception:
            # Fallback if specific model is not found, though should be there
            self.nlp = None
        
        # Initialize extractors
        self.project_extractor = ProjectExtractor()
        self.achievement_extractor = AchievementExtractor()
        self.cgpa_extractor = CGPAExtractor()
        self.school_extractor = SchoolMarksExtractor()
        self.online_extractor = OnlinePresenceExtractor()
        self.ec_extractor = ExtraCurricularExtractor()
        self.degree_classifier = DegreeClassifier()
        self.college_ranker = CollegeRanker('./data/nirf_rankings.csv')
        
        self.executor = ThreadPoolExecutor(max_workers=10)
    
    def is_model_loaded(self):
        return self.nlp is not None
    
    async def process_batch(self, files):
        start = time.time()
        
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(self.executor, self._process_single_sync, file_name, file_content)
            for file_name, file_content in files
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Filter out errors
        results = [r for r in results if r is not None]
        
        # Rank results
        ranked = self._rank_candidates(results)
        
        elapsed = time.time() - start
        
        return {
            'results': ranked,
            'stats': {
                'count': len(ranked),
                'time_seconds': round(elapsed, 2),
                'avg_per_resume': round(elapsed / max(len(ranked), 1), 3),
                'max_score': max([r['score']['total'] for r in ranked]) if ranked else 0,
                'min_score': min([r['score']['total'] for r in ranked]) if ranked else 0,
                'avg_score': round(sum([r['score']['total'] for r in ranked]) / max(len(ranked), 1), 2) if ranked else 0
            }
        }
    
    def _process_single_sync(self, filename, content):
        try:
            # Extract text
            if filename.lower().endswith('.pdf'):
                text = self._extract_pdf(content)
            elif filename.lower().endswith('.docx'):
                text = self._extract_docx(content)
            else:
                text = content.decode('utf-8', errors='ignore')
            
            # Run NLP
            doc = self.nlp(text) if self.nlp else None
            
            # Extract basic entities from spaCy
            skills = [ent.text for ent in doc.ents if ent.label_ == 'Skill'] if doc else []
            education = [ent.text for ent in doc.ents if ent.label_ == 'Education'] if doc else []
            experience_text = [ent.text for ent in doc.ents if ent.label_ == 'Work_Experience'] if doc else []
            languages = [ent.text for ent in doc.ents if ent.label_ == 'Language'] if doc else []
            
            # Heuristic for experience years
            exp_years = 0
            exp_match = re.search(r'(\d+(?:\.\d+)?)\+?\s*years?\s*(?:of\s*)?experience', text, re.IGNORECASE)
            if exp_match:
                exp_years = float(exp_match.group(1))
            
            # Heuristic for internships
            internships = []
            # Look for lines containing 'intern' and keep them as entries
            for line in text.split('\n'):
                if 'intern' in line.lower() and len(line.strip()) > 10:
                    internships.append(line.strip())

            # Run specialized extractors
            extracted = {
                'skills': skills,
                'education': education,
                'experience': experience_text,
                'languages': languages,
                'projects': self.project_extractor.extract(text),
                'achievements': self.achievement_extractor.extract(text),
                'cgpa': self.cgpa_extractor.extract(text),
                'school_marks_avg': self.school_extractor.extract_school_marks(text),
                'online_presence': self.online_extractor.extract(text),
                'extra_curricular': self.ec_extractor.extract(text),
                'degree_type': self.degree_classifier.get_highest_degree(text),
                'college_tier': self.college_ranker.get_tier(''.join(education)),
                'experience_years': exp_years,
                'internships': internships
            }
            
            # Calculate score
            score = self.scorer.calculate_score(extracted)
            
            return {
                'filename': filename,
                'score': score,
                **extracted
            }
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            return None
    
    def _extract_pdf(self, content):
        with io.BytesIO(content) as f:
            with pdfplumber.open(f) as pdf:
                text = []
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
                return '\n'.join(text)
    
    def _extract_docx(self, content):
        with io.BytesIO(content) as f:
            return docx2txt.process(f)
    
    def _rank_candidates(self, candidates):
        """Sort by score with tie-breaking"""
        sorted_cands = sorted(
            candidates,
            key=lambda x: x['score']['total'],
            reverse=True
        )
        
        for i, cand in enumerate(sorted_cands, 1):
            cand['rank'] = i
        
        return sorted_cands

    async def match_with_jd(self, files, job_description):
        """Match resumes against job description"""
        # Extract skills from JD if nlp is available
        jd_skills = []
        if self.nlp:
            jd_doc = self.nlp(job_description)
            jd_skills = [ent.text for ent in jd_doc.ents if ent.label_ == 'Skill']
        
        # Process resumes
        results = await self.process_batch(files)
        
        # Add match scores
        for res in results['results']:
            resume_skills = set([s.lower() for s in res.get('skills', [])])
            jd_skills_set = set([s.lower() for s in jd_skills])
            matches = resume_skills & jd_skills_set
            
            res['job_match'] = {
                'score': round(len(matches) / max(len(jd_skills_set), 1) * 100, 2) if jd_skills_set else 0,
                'matching_skills': list(matches),
                'missing_skills': list(jd_skills_set - resume_skills)
            }
        
        # Re-rank by match score if desired, or keep original ranking
        # Let's re-rank by job match score
        results['results'] = sorted(
            results['results'],
            key=lambda x: x['job_match']['score'],
            reverse=True
        )
        
        return results
