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
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            self.available = True
            print("[SUCCESS] Gemini AI Insights Engine ready")
        except Exception as e:
            print(f"[WARNING] Gemini init failed - AI insights disabled: {e}")
            self.available = False
            self.model = None
    
    def generate_swot(self, resume_text: str, jd_text: str, skills: List[str] = None) -> Dict:
        """
        Generate SWOT analysis for candidate vs job
        """
        if not self.available:
            return self._mock_swot(skills)
        
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
            return self._mock_swot(skills)
    
    def generate_interview_questions(self, 
                                   resume_text: str, 
                                   jd_text: str,
                                   num_questions: int = 5,
                                   skills: List[str] = None) -> List[Dict]:
        """
        Generate tailored interview questions
        """
        if not self.available:
            return self._mock_questions(skills)
        
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
            return self._mock_questions(skills)
    
    async def extract_skills(self, text: str) -> List[str]:
        """
        Extract professional skills from text using Gemini
        """
        if not self.available:
            return []

        prompt = f"""
        Extract a comprehensive list of professional skills, technical tools, and soft skills from the following text.
        Text:
        {text[:2000]}

        Return only a JSON array of skill names.
        Example: ["Python", "Machine Learning", "FastAPI", "Project Management"]
        """

        try:
            # Use a slightly larger limit for skill extraction but keep it efficient
            response = await self.model.generate_content_async(prompt)
            output = response.text
            if '```json' in output:
                output = output.split('```json')[1].split('```')[0]
            elif '```' in output:
                output = output.split('```')[1].split('```')[0]
            
            skills = json.loads(output.strip())
            return [str(s).strip() for s in skills if s]
        except Exception as e:
            print(f"Error extracting skills via Gemini: {e}")
            return []

    def _mock_swot(self, skills: List[str] = None) -> Dict:
        """Fallback SWOT when AI unavailable"""
        top_skills = skills[:3] if skills else ["Python", "Web Development", "General Software Engineering"]
        skill_str = ", ".join(top_skills)
        
        return {
            "strengths": [
                f"Demonstrated proficiency in {skill_str}",
                "Relevant project experience shown in resume",
                "Strong academic background and credentials"
            ],
            "weaknesses": [
                "Limited cloud/deployment experience mentioned",
                "Candidate could provide more specific quantifiable results",
                "Some specialized industry tools not explicitly listed"
            ],
            "opportunities": [
                "Excellent potential for rapid upskilling in project's tech stack",
                "Could transition into a specialized role within 6-12 months",
                "Opportunity to learn modern CI/CD and DevOps workflows"
            ],
            "threats": [
                "Competitive candidate pool for this specific role",
                "Potential ramp-up time for project-specific business logic"
            ]
        }
    
    def _mock_questions(self, skills: List[str] = None) -> List[Dict]:
        """Fallback questions when AI unavailable"""
        q_skills = skills[:3] if skills else ["Software Development", "Problem Solving", "Collaboration"]
        
        return [
            {
                "question": f"Based on your background in {q_skills[0] if len(q_skills) > 0 else 'Software'}, can you describe a challenging project obstacle you overcame?",
                "type": "behavioral",
                "skill_tested": q_skills[0] if len(q_skills) > 0 else "Execution",
                "difficulty": "medium"
            },
            {
                "question": f"How have you applied {q_skills[1] if len(q_skills) > 1 else 'Modern Tools'} to optimize a workflow or improve code quality?",
                "type": "technical",
                "skill_tested": q_skills[1] if len(q_skills) > 1 else "Optimisation",
                "difficulty": "medium"
            },
            {
                "question": f"Explain a complex scenario where you used {q_skills[2] if len(q_skills) > 2 else 'Teamwork'} to achieve a common goal.",
                "type": "behavioral",
                "skill_tested": q_skills[2] if len(q_skills) > 2 else "Leadership",
                "difficulty": "medium"
            }
        ]
    
    def analyze_candidate(self, resume_text: str, jd_text: str, skills: List[str] = None) -> Dict:
        """
        Complete candidate analysis
        """
        swot = self.generate_swot(resume_text, jd_text, skills=skills)
        questions = self.generate_interview_questions(resume_text, jd_text, skills=skills)
        
        return {
            'swot_analysis': swot,
            'interview_questions': questions,
            'ai_powered': self.available
        }
