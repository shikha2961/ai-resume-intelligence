from google import genai
from dotenv import load_dotenv
from google.genai import types
import os, json

load_dotenv()

geminiClient = genai.Client()

def parse_resume_with_gemini(resume_text: str):
    response = geminiClient.models.generate_content(
        model="gemini-2.5-flash",
        contents=resume_text,
        config=types.GenerateContentConfig(
            system_instruction="""You're an expert agent in parsing the resume and
            Extract the user's skill, experience, education, certification, projects
            After parsing the response,
            RETURN THE RESPONSE IN JSON FORMAT""",
            temperature=0.2,
            response_mime_type="application/json"
        )
    )

    if response.parsed is not None:
        return response.parsed

    try:
        return json.loads(response.text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Gemini parsing failed: {response.text}") from exc
