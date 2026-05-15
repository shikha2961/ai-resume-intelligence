from fastapi import APIRouter, UploadFile, File, Form
from ....services.pdf_parser import extract_text_from_pdf
from ....services.llm_service import analyse_resume_with_llm

router = APIRouter(prefix="/api/v1/resumes")

# @router.post("/upload")
# async def uploadResume():
#     print(file.filename)
#     print(file.content_type)

#     content = await file.read()
#     extract_text_from_pdf(content)
#     return {
#         "filename": file.filename,
#         "content_type": file.content_type,
#         "size": len(content)
#     }

# @router.post("/jdtext")
# def jobDescription(jd_text: str):
#     return "text received"

@router.post("/analyze_resume")
async def analyzeResume(resume: UploadFile = File(...), jd_text: str = Form(...)):
    content = await resume.read()
    resume_text = extract_text_from_pdf(content)
    analyse_resume_with_llm(resume_text, jd_text)
    return "analysed successfully"