import streamlit as st
import requests

st.set_page_config(page_title="AI Job Recommender", layout="wide")

# Title
st.title(" AI Job Recommendation System")
st.markdown("Upload your CV and get the best matching jobs")

# Sidebar
st.sidebar.title("⚙️ Settings")
top_k = st.sidebar.slider("Number of jobs", 1, 10, 5)

# Upload
uploaded_file = st.file_uploader("📄 Upload your CV (PDF)", type=["pdf"])

if uploaded_file:
    
    with st.spinner("Analyzing your CV... 🔍"):
        response = requests.post(
            "http://127.0.0.1:8000/recommend",
            files={"file": uploaded_file}
        )
    
    data = response.json()
    
    st.success("Top Job Matches Found ✅")

    for job in data["results"][:top_k]:
        
        st.subheader(job["title"])
        
        # Score visualization
        st.progress(job["score"])
        st.write(f"Match Score: {job['score']:.2f}")
        
        # Score label
        if job["score"] > 0.5:
            st.success("High Match")
        elif job["score"] > 0.3:
            st.warning("Medium Match")
        else:
            st.error("Low Match")
        
        # Expand description
        with st.expander("📄 Job Description"):
            st.write(job["description"])
        
        st.markdown("---")