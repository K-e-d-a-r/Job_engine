import requests

def fetch_jobs():
    url = "https://www.arbeitnow.com/api/job-board-api"
    response = requests.get(url)
    data = response.json()

    jobs = []
    for job in data["data"]:
        jobs.append({
            "title": job["title"],
            "description": job["description"]
        })

    return jobs