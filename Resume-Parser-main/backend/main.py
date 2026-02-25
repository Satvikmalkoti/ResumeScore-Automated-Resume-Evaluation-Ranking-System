import os
import time
import io
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
import pandas as pd

from batch.processor import BatchResumeProcessor
from matcher.jd_parser import JDParser
from matcher.tfidf_matcher import TFIDFJobMatcher

# Initialize FastAPI
app = FastAPI(title="Resume Parser API", version="2.0.0")

# CORS Configuration
# frontend_url = os.getenv("FRONTEND_URL", "*") # User didn't specify, so wildcard or local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Processor
# Using relative path to model as defined in implementation plan
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model")
processor = BatchResumeProcessor(model_path=MODEL_PATH)

@app.get("/")
async def root():
    return {
        "app": "Resume Parser API",
        "version": "2.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": processor.is_model_loaded(),
        "api_version": "2.0.0"
    }

@app.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    """Parse a single resume with detailed scoring"""
    try:
        content = await file.read()
        result = processor._process_single_sync(file.filename, content)
        
        if not result:
            raise HTTPException(status_code=400, detail="Failed to parse resume")
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch-parse")
async def batch_parse(files: List[UploadFile] = File(...)):
    """Parse multiple resumes and rank them"""
    try:
        file_data = []
        for file in files:
            content = await file.read()
            file_data.append((file.filename, content))
            
        results = await processor.process_batch(file_data)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/match-job")
async def match_with_job(
    files: List[UploadFile] = File(...),
    job_description: str = Form(...)
):
    """Match resumes against job description"""
    if not job_description:
        # Try to get from form body if not in query
        raise HTTPException(status_code=400, detail="Job description required")
    
    try:
        file_data = []
        for file in files:
            content = await file.read()
            file_data.append((file.filename, content))
            
        results = await processor.match_with_jd(file_data, job_description)
        
        # Add metadata for the UI if needed
        return {
            "status": "success",
            "job_description_parsed": True,
            **results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/export")
async def export_results(results: List[dict]):
    """Export results as CSV"""
    try:
        df = pd.DataFrame(results)
        # Flatten score dict for CSV
        if 'score' in df.columns:
            scores = pd.json_normalize(df['score'])
            df = pd.concat([df.drop('score', axis=1), scores], axis=1)
            
        csv_data = df.to_csv(index=False)
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=rankings.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
