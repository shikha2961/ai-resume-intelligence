from fastapi import APIRouter, UploadFile, File
from ....services.pdf_parser import extract_text_from_pdf

router = APIRouter(prefix="/api/v1/resumes")

@router.post("/upload")
async def uploadResume(file: UploadFile = File(...)):
    print(file.filename)
    print(file.content_type)

    content = await file.read()
    extract_text_from_pdf(content)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content)
    }

@router.post("/jdtext")
def jobDescription():
    return "text received"

@router.post("/analyze")
def analyzeResume():
    return "analysed successfully"