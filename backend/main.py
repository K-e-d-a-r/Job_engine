from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil

from utils.parser import extract_cv_text
from utils.preprocessing import clean_text
from backend.job_api import fetch_jobs
from backend.recommender import recommend_jobs

app = FastAPI()

# CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home route
@app.get("/", response_class=HTMLResponse)
def home():
    return "<h2> AI Job Recommendation API Running</h2>"

# Main endpoint with filters
@app.post("/recommend")
async def recommend(
    file: UploadFile,
    title: str = Form(None),
    location: str = Form(None),
    job_type: str = Form(None)
):

    # Save CV
    with open("cv.pdf", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    text = extract_cv_text("cv.pdf")
    clean = clean_text(text)

    # Fetch jobs
    jobs = fetch_jobs()

    #  APPLY FILTERS
    filtered_jobs = []

    for job in jobs:
        desc = job["description"].lower()
        title_text = job["title"].lower()

        combined = title_text + " " + desc

        if title and title.lower() not in title_text:
            continue

        if location:
            if location.lower() not in combined:
                continue

        if job_type:
            jt = job_type.lower()
            if jt == "part time" and "part" not in combined:
                continue
            elif jt == "full time" and "full" not in combined:
                continue
            elif jt == "remote" and "remote" not in combined:
                continue

        filtered_jobs.append(job)

    # fallback if nothing matched
    if len(filtered_jobs) == 0:
        return {"results": []}

    # Recommend
    results = recommend_jobs(clean, filtered_jobs)

    return {"results": results}