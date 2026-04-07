from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil

from utils.parser import extract_cv_text
from utils.preprocessing import clean_text
from backend.job_api import fetch_jobs
from backend.recommender import recommend_jobs

app = FastAPI()

#  CORS (IMPORTANT for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Home route
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1> AI Job Recommendation API</h1>
    <p>Use the frontend UI or go to <a href="/docs">/docs</a></p>
    """

@app.post("/recommend")
async def recommend(file: UploadFile):

    with open("cv.pdf", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_cv_text("cv.pdf")
    clean = clean_text(text)

    jobs = fetch_jobs()
    results = recommend_jobs(clean, jobs)

    return {"results": results}