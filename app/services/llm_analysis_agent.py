from openai import OpenAI
import os, json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from app.models.resume_analyse_response import ResumeAnalyseResponse

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

geminiClient = genai.Client()

def build_prompt(resume_text: str, jd_text: str):
    prompt = """
    user_input:
    =====================
    RESUME:
    =====================
    {resume_text}

    =====================
    JOB DESCRIPTION:
    =====================
    {jd_text}
    """
    return prompt


def analyse_resume_with_gpt(resume_text: str, jd_text: str):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=build_prompt(resume_text, jd_text)
    )

    print(response.output_text)


def analyse_resume_with_gemini(resume_text: str, jd_text: str) -> ResumeAnalyseResponse:
    response = geminiClient.models.generate_content(
        model="gemini-2.5-flash",
        contents=build_prompt(resume_text, jd_text),
        config=types.GenerateContentConfig(
            system_instruction="""You're an expert ATS (Applicant Tracking System) assistant, where you analyse resume based upon applicant's Job Description. 
            Provide following in response:
            1. ATS Score out of 100.
            2. Missing Skills
            3. Candidate Strengths
            4. Resume Improvement Suggestions
            5. Recommended rewritten resume summary - helpful for user..

            RETURN THE RESPONSE IN JSON FORMAT""",
            temperature=0.2,
            response_mime_type="application/json",
            response_schema=ResumeAnalyseResponse,
        )
    )

    if response.parsed is None:
        raise ValueError(f"Gemini parsing failed: {response.text}")

    return response.parsed


    

