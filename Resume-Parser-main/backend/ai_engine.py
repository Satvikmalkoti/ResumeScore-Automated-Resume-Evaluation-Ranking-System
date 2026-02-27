"""
AI Insights Engine using Google Gemini 2.0 Flash
Generates SWOT analysis and interview questions
FREE tier - perfect for hackathon
"""

import os
from typing import Dict, List
import json

try:
    import google.generativeai as genai  # type: ignore
except Exception:
    genai = None

class AIInsightsEngine:
    """
    Uses Gemini 2.0 Flash for:
    - SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)
    - Tailored Interview Questions
    """
    
    def __init__(self, api_key: str = None):
        # Get API key from environment
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            print("[WARNING] No Gemini API key found - AI insights disabled")
            self.available = False
            return

        if genai is None:
            print("[WARNING] google-generativeai is not installed - AI insights disabled")
            self.available = False
            self.model = None
            return
        
        # Configure Gemini (keep app running even if config/model init fails)
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            self.available = True
            print("[SUCCESS] Gemini AI Insights Engine ready")
        except Exception as e:
            print(f"[WARNING] Gemini init failed - AI insights disabled: {e}")
            self.available = False
            self.model = None
    
    def generate_swot(self, resume_text: str, jd_text: str) -> Dict:
        """
        Generate SWOT analysis for candidate vs job
        """
        if not self.available:
            return self._mock_swot()
        
        prompt = f"""
        You are an expert HR analyst. Analyze this candidate's resume against the job description.
        
        JOB DESCRIPTION:
        {jd_text[:1000]}
        
        RESUME:
        {resume_text[:1500]}
        
        Generate a SWOT analysis:
        
        STRENGTHS: What makes this candidate EXCELLENT for this role? (3-5 points)
        WEAKNESSES: What skills/experience are they MISSING? (2-4 points)
        OPPORTUNITIES: How could they grow in this role? (2-3 points)
        THREATS: What could hurt their success? (1-2 points)
        
        Format as JSON:
        {{
            "strengths": ["point1", "point2", ...],
            "weaknesses": ["point1", "point2", ...],
            "opportunities": ["point1", "point2", ...],
            "threats": ["point1", "point2", ...]
        }}
        
        Be specific, concise, and professional.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Extract JSON from response
            text = response.text
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1].split('```')[0]
            
            return json.loads(text.strip())
        except Exception as e:
            print(f"Error generating SWOT: {e}")
            return self._mock_swot()
    
    def generate_interview_questions(self, 
                                   resume_text: str, 
                                   jd_text: str,
                                   num_questions: int = 5) -> List[Dict]:
        """
        Generate tailored interview questions
        """
        if not self.available:
            return self._mock_questions()
        
        prompt = f"""
        You are a technical interviewer. Generate {num_questions} interview questions for this candidate.
        
        JOB DESCRIPTION:
        {jd_text[:1000]}
        
        CANDIDATE RESUME:
        {resume_text[:1500]}
        
        Create questions that:
        1. Test their claimed skills
        2. Address potential gaps
        3. Assess fit for the role
        
        Format as JSON array:
        [
            {{
                "question": "Question text here?",
                "type": "technical|behavioral|problem-solving",
                "skill_tested": "skill name",
                "difficulty": "easy|medium|hard"
            }},
            ...
        ]
        
        Make questions specific to their resume and the job.
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1].split('```')[0]
            
            return json.loads(text.strip())
        except Exception as e:
            print(f"Error generating questions: {e}")
            return self._mock_questions()
    
    def _mock_swot(self) -> Dict:
        """Fallback SWOT when AI unavailable"""
        return {
            "strengths": [
                "Strong Python skills matching job requirements",
                "Previous experience with web frameworks",
                "Good academic background"
            ],
            "weaknesses": [
                "Limited cloud/AWS experience mentioned",
                "No senior-level project leadership shown"
            ],
            "opportunities": [
                "Could grow into technical lead role",
                "Opportunity to learn modern stack"
            ],
            "threats": [
                "May need ramp-up time with specific tech stack"
            ]
        }
    
    def _mock_questions(self) -> List[Dict]:
        """Fallback questions when AI unavailable"""
        return [
            {
                "question": "Describe a challenging Python project you worked on. How did you overcome obstacles?",
                "type": "behavioral",
                "skill_tested": "Python",
                "difficulty": "medium"
            },
            {
                "question": "How would you design a REST API for a high-traffic application?",
                "type": "technical",
                "skill_tested": "API Design",
                "difficulty": "hard"
            },
            {
                "question": "Explain your experience with databases and query optimization.",
                "type": "technical",
                "skill_tested": "Databases",
                "difficulty": "medium"
            }
        ]
    
    def analyze_candidate(self, resume_text: str, jd_text: str) -> Dict:
        """
        Complete candidate analysis
        """
        swot = self.generate_swot(resume_text, jd_text)
        questions = self.generate_interview_questions(resume_text, jd_text)
        
        return {
            'swot_analysis': swot,
            'interview_questions': questions,
            'ai_powered': self.available
        }
