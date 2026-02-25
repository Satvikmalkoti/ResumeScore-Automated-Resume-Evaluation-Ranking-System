import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
from pathlib import Path
import json
import spacy
import pdfplumber
import docx2txt
import io
import re

from scoring.scorer import ResumeScorer
from extraction.project_extractor import ProjectExtractor
from extraction.achievement_extractor import AchievementExtractor
from extraction.cgpa_extractor import CGPAExtractor
from extraction.school_marks import SchoolMarksExtractor
from extraction.online_presence import OnlinePresenceExtractor
from extraction.extra_curricular import ExtraCurricularExtractor
from extraction.degree_classifier import DegreeClassifier
from extraction.college_ranker import CollegeRanker
from extraction.skill_filter import SkillFilter
from matcher.jd_parser import JDParser
from matcher.tfidf_matcher import TFIDFJobMatcher

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
        # Initialize with the directory containing all NIRF CSVs
        self.college_ranker = CollegeRanker('./data')
        self.skill_filter = SkillFilter()
        self.jd_parser = JDParser()
        self.job_matcher = TFIDFJobMatcher()
        
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
            
            # Filter skills to remove college names
            skills = self.skill_filter.filter_skills(skills, education)
            
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
                'college_tier': self.college_ranker.get_tier(' '.join(education) if education else text),
                'experience_years': exp_years,
                'internships': internships
            }
            
            # Calculate score
            score = self.scorer.calculate_score(extracted)
            
            return {
                'filename': filename,
                'full_text': text,
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
        """Match resumes against job description using TF-IDF and skill matching"""
        # Parse job description
        jd_data = self.jd_parser.parse_job_description(job_description)
        jd_skills = set(jd_data['required_skills'])
        jd_exp = jd_data['years_experience']
        
        # Process resumes to get basic features
        results = await self.process_batch(files)
        
        # Add matches using comprehensive_match
        for res in results['results']:
            # Re-extracting full text or using stored text if available
            # Since process_batch doesn't return full text currently, let's assume we need it
            # We might want to modify _process_single_sync to include full_text if needed
            # But for now, we'll recreate the match based on extracted data
            
            # Note: For better accuracy, we should really pass the full text here.
            # I'll update match_with_jd to store full text during processing or use a workaround.
            
            # Using extracted skills and experience
            resume_skills = set([s.lower() for s in res.get('skills', [])])
            resume_exp = res.get('experience_years', 0)
            
            # For TF-IDF, we need 'text'. Since it's not in 'res', let's fix that in _process_single_sync.
            resume_text = res.get('full_text', "") 
            
            match_res = self.job_matcher.comprehensive_match(
                resume_text=resume_text,
                jd_text=job_description,
                resume_skills=resume_skills,
                jd_skills=jd_skills,
                resume_exp=resume_exp,
                jd_exp=jd_exp
            )
            
            res['job_match'] = {
                'score': match_res['total_score'],
                'tfidf_similarity': match_res['tfidf_similarity'],
                'matching_skills': match_res['skill_match']['matched'],
                'missing_skills': match_res['skill_match']['missing'],
                'experience_match': match_res['experience_match'],
                'top_terms': match_res['top_terms']
            }
        
        # Re-rank by match score
        results['results'] = sorted(
            results['results'],
            key=lambda x: x['job_match']['score'],
            reverse=True
        )
        
        return results
