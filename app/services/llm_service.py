from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def build_prompt(resume_text: str, jd_text: str):
    prompt = """You're an expert ATS (Applicant Tracking System) assistant, where you analyse resume based upon applicant's Job Description. 
    Provide following in response:
    1. ATS Score out of 100.
    2. Missing Skills
    3. Candidate Strengths
    4. Resume Improvement Suggestions
    5. Recommended rewritten resume summary - helpful for user..

    RETURN THE RESPONSE IN JSON FORMAT

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


def analyse_resume_with_llm(resume_text: str, jd_text: str):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=build_prompt(resume_text, jd_text)
    )

    print(response.output_text)

