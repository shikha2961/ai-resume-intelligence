from fastapi import APIRouter, UploadFile, File, Form
from ....services.pdf_extraction import extract_text_from_pdf
from ....services.llm_parser_agent import parse_resume_with_gemini
from ....services.llm_analysis_agent import analyse_resume_with_gemini
from ....schemas.resume_analyse_response import ResumeAnalyseResponse

router = APIRouter(prefix="/api/v1/resumes")

@router.post("/analyze_resume", response_model=ResumeAnalyseResponse)
async def analyzeResume(resume: UploadFile = File(...), jd_text: str = Form(...)):
    content = await resume.read()
    resume_text = extract_text_from_pdf(content)
    parsed_resume = parse_resume_with_gemini(resume_text)
    return analyse_resume_with_gemini(parsed_resume, jd_text)
    