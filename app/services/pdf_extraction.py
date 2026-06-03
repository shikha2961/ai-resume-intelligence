import fitz
import re
import unicodedata
from fastapi import UploadFile
from presidio_analyzer import AnalyzerEngine

def clean_extracted_text(text: str) -> str:
    """Normalize and clean text extracted from a PDF."""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = "\n".join(line.strip() for line in text.splitlines())
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = "".join(page.get_text() for page in doc)
    cleaned_text = clean_extracted_text(text)
    return redact_personal_information(cleaned_text)

def redact_personal_information(resume_text: str):
    analyzer = AnalyzerEngine()
    results = analyzer.analyze(
        text = resume_text,
        entities=["PHONE_NUMBER", "EMAIL_ADDRESS"],
        language="en"

    )
    redacted_text = resume_text
    for result in sorted(results, key=lambda r: r.start, reverse=True):
        replacement = "[REDACTED_EMAIL]" if result.entity_type=="EMAIL_ADDRESS" else "[REDACTED_PHONE]"
        redacted_text = (
            redacted_text[: result.start]
            + replacement
            + redacted_text[result.end :]
        )
    return redacted_text
