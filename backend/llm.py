import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

def explain_job(cv_text, job_desc):
    try:
        prompt = f"""
        Candidate CV:
        {cv_text[:400]}

        Job Description:
        {job_desc[:400]}

        Explain:
        - Why this job matches
        - Matching skills
        - Missing skills
        - Suitability score out of 10

        Keep it short (max 5 bullet points).
        """

        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300   
        )

        return response.choices[0].message.content

    except Exception as e:
        print("HF ROUTER ERROR:", e)
        return f"LLM error: {str(e)}"