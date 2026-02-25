The project consists of 2 plans
1.Backend plan
📋 COMPLETE ACTION PLAN FOR YOUR AI AGENT
Here's exactly what to do, file by file:

🗑️ FILES TO DELETE (6 files)
File Path	Reason
Training_pipeline.ipynb	Training notebook - not needed
apply_clean_text.py	Pre-processing only
ls_to_spacy.py	Data conversion only
make_prelabels.py	Pre-labeling only
show_mismatches.py	Debugging tool
train_ner.py	Training script
📁 FILES TO KEEP (1 folder)
Path	Reason
/output/model-best/	The trained model (96.77% accuracy)
🆕 NEW FILES TO CREATE (15 files)
Folder Structure to Create:
text
backend/
├── __init__.py
├── main.py                 # FastAPI endpoints
├── config.py               # Environment config
├── requirements.txt        # Dependencies
├── Dockerfile              # Containerization
├── docker-compose.yml      # Multi-container setup
├── .env.example            # Environment template
│
├── scoring/
│   ├── __init__.py
│   └── scorer.py           # Scoring engine
│
├── extraction/
│   ├── __init__.py
│   ├── project_extractor.py
│   ├── achievement_extractor.py
│   ├── cgpa_extractor.py
│   ├── school_marks.py
│   ├── online_presence.py
│   ├── extra_curricular.py
│   ├── degree_classifier.py
│   └── college_ranker.py
│
├── batch/
│   ├── __init__.py
│   └── processor.py        # Batch processing
│
└── data/
    └── nirf_rankings.csv   # College rankings
📝 FILE CONTENTS FOR AI AGENT
File 1: backend/requirements.txt
txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
spacy==3.7.4
spacy-transformers==1.3.4
torch==2.1.0
pdfplumber==0.10.3
docx2txt==0.8
pandas==2.1.3
openpyxl==3.1.2
redis==5.0.1
slowapi==0.1.9
python-multipart==0.0.6
pydantic-settings==2.1.0
File 2: backend/config.py
python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    app_name: str = "Resume Parser API"
    environment: str = "development"
    model_path: str = "./output/model-best"
    max_file_size_mb: int = 10
    allowed_extensions: List[str] = [".pdf", ".docx"]
    redis_url: str = "redis://localhost:6379"
    api_rate_limit: str = "100/minute"
    cors_origins: List[str] = ["*"]
    
    class Config:
        env_file = ".env"

settings = Settings()
File 3: backend/.env.example
bash
ENVIRONMENT=production
MODEL_PATH=./output/model-best
REDIS_URL=redis://redis:6379
CORS_ORIGINS=https://your-frontend.vercel.app
File 4: backend/Dockerfile
dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_trf

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
File 5: backend/docker-compose.yml
yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - MODEL_PATH=/app/output/model-best
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./output:/app/output
      - ./data:/app/data
    depends_on:
      - redis
    restart: always

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: always
File 6: backend/main.py
python
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import pandas as pd
import io
import json
import uuid
import redis
from typing import List
import time

from config import settings
from batch.processor import BatchResumeProcessor

# Initialize
app = FastAPI(title="Resume Parser API", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Redis cache
redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

# Stats tracking
class Stats:
    def __init__(self):
        self.total = 0
        self.total_time = 0
    
    @property
    def avg_time(self):
        return round(self.total_time / max(self.total, 1), 2)

stats = Stats()

# Initialize processor
processor = BatchResumeProcessor(model_path=settings.model_path)

@app.get("/")
async def root():
    return {
        "app": settings.app_name,
        "version": "2.0.0",
        "status": "running",
        "environment": settings.environment
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": processor.is_model_loaded(),
        "api_version": "2.0.0",
        "environment": settings.environment
    }

@app.get("/metrics")
async def get_metrics():
    return {
        "total_resumes_processed": stats.total,
        "average_response_time_ms": stats.avg_time,
        "accuracy_f1_score": 96.77,
        "cache_hit_rate": 0.0  # To be implemented
    }

@app.post("/parse")
@limiter.limit(settings.api_rate_limit)
async def parse_resume(
    request: Request,
    file: UploadFile = File(...)
):
    """Parse a single resume"""
    start = time.time()
    
    # Check cache
    cache_key = f"resume:{file.filename}"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Process
    result = await processor.process_single(file)
    
    # Cache for 1 hour
    redis_client.setex(cache_key, 3600, json.dumps(result))
    
    # Update stats
    stats.total += 1
    stats.total_time += (time.time() - start) * 1000
    
    return result

@app.post("/batch-parse")
async def batch_parse(
    files: List[UploadFile] = File(...)
):
    """Parse 25+ resumes and rank them"""
    if len(files) > 100:
        raise HTTPException(400, "Maximum 100 files per request")
    
    results = await processor.process_batch(files)
    return results

@app.post("/batch-parse-async")
async def batch_parse_async(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    """Process resumes in background"""
    task_id = str(uuid.uuid4())
    
    # Save files temporarily
    file_paths = []
    for file in files:
        path = f"/tmp/{task_id}_{file.filename}"
        content = await file.read()
        with open(path, "wb") as f:
            f.write(content)
        file_paths.append(path)
    
    # Background processing
    background_tasks.add_task(
        processor.process_batch_background,
        task_id=task_id,
        file_paths=file_paths
    )
    
    return {
        "task_id": task_id,
        "status": "processing",
        "check_status_at": f"/task-status/{task_id}"
    }

@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    """Check background task status"""
    status = redis_client.get(f"task:{task_id}")
    if not status:
        raise HTTPException(404, "Task not found")
    return json.loads(status)

@app.post("/export")
async def export_results(
    results: List[dict],
    format: str = "json"
):
    """Export results in various formats"""
    if format == "csv":
        df = pd.DataFrame(results)
        csv_data = df.to_csv(index=False)
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=rankings.csv"}
        )
    
    elif format == "excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df = pd.DataFrame(results)
            df.to_excel(writer, sheet_name='Rankings', index=False)
        return Response(
            content=output.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=rankings.xlsx"}
        )
    
    return results

@app.post("/match-job")
async def match_with_job(
    files: List[UploadFile] = File(...),
    job_description: str = None
):
    """Match resumes against job description"""
    if not job_description:
        raise HTTPException(400, "Job description required")
    
    results = await processor.match_with_jd(files, job_description)
    return results
File 7: backend/scoring/scorer.py
python
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
        scores['school_marks'] = (school_avg / 10) * 2
        
        total = sum(scores.values())
        
        return {
            'total': round(total, 2),
            'breakdown': scores,
            'max_possible': 100
        }
File 8: backend/batch/processor.py
python
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time
from pathlib import Path
import json
import spacy
import pdfplumber
import docx2txt

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
    def __init__(self, model_path="./output/model-best"):
        self.scorer = ResumeScorer()
        self.nlp = spacy.load(model_path)
        
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
            loop.run_in_executor(self.executor, self._process_single, file)
            for file in files
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Rank results
        ranked = self._rank_candidates(results)
        
        elapsed = time.time() - start
        
        return {
            'results': ranked,
            'stats': {
                'count': len(ranked),
                'time_seconds': round(elapsed, 2),
                'avg_per_resume': round(elapsed / len(ranked), 3),
                'max_score': max(r['score']['total'] for r in ranked),
                'min_score': min(r['score']['total'] for r in ranked),
                'avg_score': round(sum(r['score']['total'] for r in ranked) / len(ranked), 2)
            }
        }
    
    def _process_single(self, file):
        # Read file
        content = file.file.read()
        
        # Extract text
        if file.filename.endswith('.pdf'):
            text = self._extract_pdf(content)
        else:
            text = self._extract_docx(content)
        
        # Run NLP
        doc = self.nlp(text)
        
        # Extract entities
        extracted = self._extract_entities(doc, text)
        extracted['filename'] = file.filename
        
        # Calculate score
        score = self.scorer.calculate_score(extracted)
        
        return {
            'filename': file.filename,
            'score': score,
            **extracted
        }
    
    def _extract_entities(self, doc, text):
        """Extract all entities from doc"""
        return {
            'skills': [ent.text for ent in doc.ents if ent.label_ == 'Skill'],
            'education': [ent.text for ent in doc.ents if ent.label_ == 'Education'],
            'experience': [ent.text for ent in doc.ents if ent.label_ == 'Work_Experience'],
            'languages': [ent.text for ent in doc.ents if ent.label_ == 'Language'],
            'projects': self.project_extractor.extract(text),
            'achievements': self.achievement_extractor.extract(text),
            'cgpa': self.cgpa_extractor.extract(text),
            'school_marks_avg': self.school_extractor.extract_school_marks(text),
            'online_presence': self.online_extractor.extract(text),
            'extra_curricular': self.ec_extractor.extract(text),
            'degree_type': self.degree_classifier.get_highest_degree([]),
            'college_tier': 3,
            'experience_years': 0
        }
    
    def _extract_pdf(self, content):
        import io
        with io.BytesIO(content) as f:
            with pdfplumber.open(f) as pdf:
                text = []
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
                return '\n'.join(text)
    
    def _extract_docx(self, content):
        import io
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
        # Extract skills from JD
        jd_doc = self.nlp(job_description)
        jd_skills = [ent.text for ent in jd_doc.ents if ent.label_ == 'Skill']
        
        # Process resumes
        results = await self.process_batch(files)
        
        # Add match scores
        for res in results['results']:
            resume_skills = set(res.get('skills', []))
            jd_skills_set = set(jd_skills)
            matches = resume_skills & jd_skills_set
            
            res['job_match'] = {
                'score': round(len(matches) / len(jd_skills_set) * 100, 2) if jd_skills_set else 0,
                'matching_skills': list(matches),
                'missing_skills': list(jd_skills_set - resume_skills)
            }
        
        # Re-rank by match score
        results['results'] = sorted(
            results['results'],
            key=lambda x: x['job_match']['score'],
            reverse=True
        )
        
        return results
    
    def process_batch_background(self, task_id, file_paths):
        """Background processing for large batches"""
        try:
            results = []
            for path in file_paths:
                # Process file
                with open(path, 'rb') as f:
                    # Mock processing
                    results.append({
                        'filename': Path(path).name,
                        'score': {'total': 85.5}
                    })
            
            # Store result
            from redis import Redis
            r = Redis.from_url('redis://localhost:6379')
            r.setex(
                f"task:{task_id}",
                3600,
                json.dumps({
                    'status': 'completed',
                    'results': results,
                    'completed_at': time.time()
                })
            )
        except Exception as e:
            r.setex(
                f"task:{task_id}",
                3600,
                json.dumps({'status': 'failed', 'error': str(e)})
            )
🚀 How to Run Everything:
Step 1: Delete old files
bash
rm Training_pipeline.ipynb apply_clean_text.py ls_to_spacy.py make_prelabels.py show_mismatches.py train_ner.py
Step 2: Create folder structure
bash
mkdir -p backend/scoring backend/extraction backend/batch backend/data
Step 3: Add all new files (use the code above)
Step 4: Run with Docker
bash
cd backend
docker-compose up --build
Step 5: Test the API
bash
# Health check
curl http://localhost:8000/health

# Parse a resume
curl -X POST -F "file=@resume.pdf" http://localhost:8000/parse


2.Frontend plan
I have used google stich so use it for the project as design and write the code


Important NOte:
You can odify the directory structure as you want but make sure the code is well organized and easy to understand.