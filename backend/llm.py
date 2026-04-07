from openai import OpenAI

client = OpenAI()

def explain_job(cv_text, job_desc):
    
    prompt = f"""
    Candidate CV:
    {cv_text}

    Job Description:
    {job_desc}

    Explain:
    1. Why this job matches
    2. Missing skills
    3. Suitability score (out of 10)
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content