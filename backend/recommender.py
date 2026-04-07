from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def recommend_jobs(cv_text, jobs, top_k=5):

    job_texts = [job["description"] for job in jobs]

    job_embeddings = model.encode(job_texts)
    cv_embedding = model.encode([cv_text])

    scores = cosine_similarity(cv_embedding, job_embeddings)[0]

    results = []

    for i in range(len(jobs)):
        results.append({
            "title": jobs[i]["title"],
            "description": jobs[i]["description"],
            "score": round(float(scores[i]), 3)
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:top_k]