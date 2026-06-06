from pydantic import BaseModel

class ResumeAnalyseResponse(BaseModel):
    ats_score: int
    missing_skills: list[str]
    candidate_strengths: list[str]
    resume_improvement_suggestions: list[str]
    rewritten_resume_summary: str
