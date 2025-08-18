import os
import tempfile
import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util
import nltk
import matplotlib.pyplot as plt
import seaborn as sns

# NLTK downloads
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')

# Load transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Extract text from PDF
def extract_text_from_pdf(path):
    text = ""
    try:
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error reading PDF with fitz: {e}")
    return text

# Regex-based fallback for resume info
def extract_resume_info(path):
    text = extract_text_from_pdf(path)

    # Name: First non-empty line
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    name = lines[0] if lines else "Unknown"

    # Email
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    email = emails[0] if emails else "Not available"

    # Phone
    phones = re.findall(r'\+?\d[\d\s\-\(\)]{8,}\d', text)
    mobile = phones[0] if phones else "Not available"

    # Skills: Match common tech skills
    skill_list = [
        "python", "java", "c++", "flask", "django", "react", "angular", "node", "sql",
        "html", "css", "javascript", "git", "github", "docker", "kubernetes", "aws", "azure"
    ]
    text_lower = text.lower()
    skills = [skill.title() for skill in skill_list if skill in text_lower]

    return {
        "name": name,
        "email": email,
        "mobile_number": mobile,
        "skills": skills
    }

# Semantic similarity
def calculate_similarity(resume_text, job_desc):
    if not resume_text.strip():
        return 0.0
    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    job_emb = model.encode(job_desc, convert_to_tensor=True)
    return util.pytorch_cos_sim(resume_emb, job_emb).item()

# Simple keyword matching
def keyword_match_score(resume_text, job_desc):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_desc.lower().split())
    return len(resume_words & job_words) / len(job_words) if job_words else 0

# ---------------- Streamlit UI ----------------

st.set_page_config(page_title="ATS with fitz", layout="wide")
st.title("📄 Applicant Tracking System (Using PyMuPDF + Semantic AI)")

job_desc = st.text_area("📝 Paste the Job Description", height=200)
uploaded_files = st.file_uploader("📤 Upload Resume PDFs", type=["pdf"], accept_multiple_files=True)
num_shortlist = st.number_input("🎯 Number of Candidates to Shortlist", min_value=1, step=1)

if st.button("🚀 Compare and Rank"):
    if not uploaded_files or not job_desc.strip():
        st.warning("Please upload resumes and enter a job description.")
    else:
        results = []

        for uploaded_file in uploaded_files:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    path = tmp.name

                resume_text = extract_text_from_pdf(path)
                resume_info = extract_resume_info(path)

                ai_score = calculate_similarity(resume_text, job_desc)
                keyword_score = keyword_match_score(resume_text, job_desc)
                final_score = 0.7 * ai_score + 0.3 * keyword_score

                jd_keywords = set(word.strip().lower() for word in job_desc.split())
                matched_skills = [
                    skill for skill in resume_info.get("skills", [])
                    if skill.lower() in jd_keywords
                ]

                results.append({
                    "filename": uploaded_file.name,
                    "name": resume_info.get("name") or uploaded_file.name.split(".")[0],
                    "email": resume_info.get("email") or "Not available",
                    "mobile": resume_info.get("mobile_number") or "Not available",
                    "skills": resume_info.get("skills") or [],
                    "matched_skills": matched_skills,
                    "score": round(final_score, 4),
                    "ai_score": round(ai_score, 4),
                    "keyword_score": round(keyword_score, 4),
                    "text": resume_text
                })

            except Exception as e:
                st.error(f"Error processing file {uploaded_file.name}: {e}")

        results = sorted(results, key=lambda x: x['score'], reverse=True)[:num_shortlist]

        if results:
            st.subheader("🏆 Top Candidates")

            for idx, r in enumerate(results, start=1):
                st.markdown(f"### {idx}. {r['name']} ({r['email']}, 📞 {r['mobile']})")
                st.write(f"📄 File: `{r['filename']}`")
                st.write(f"✅ Final Score: `{r['score']}` (AI: `{r['ai_score']}`, Keyword: `{r['keyword_score']}`)")
                st.write(f"🧠 Extracted Skills: `{', '.join(r['skills']) if r['skills'] else 'N/A'}`")
                st.write(f"🎯 Matched Skills (from JD): `{', '.join(r['matched_skills']) if r['matched_skills'] else 'None'}`")

                with st.expander("📄 View Resume Text"):
                    st.text(r['text'][:3000])

                st.markdown("---")

            # CSV export
            df_export = pd.DataFrame([{
                "Name": r['name'],
                "Email": r['email'],
                "Mobile": r['mobile'],
                "Filename": r['filename'],
                "Final Score": r['score'],
                "AI Score": r['ai_score'],
                "Keyword Score": r['keyword_score'],
                "Matched Skills": ", ".join(r['matched_skills']),
                "All Skills": ", ".join(r['skills']),
            } for r in results])

            st.download_button("⬇️ Download Results as CSV", df_export.to_csv(index=False), "top_candidates.csv")

            # 📊 Line Plot: ATS vs Traditional
            st.subheader("📊 ATS Efficiency Comparison")

            names = [r['name'] for r in results]
            ai_scores = [r['ai_score'] for r in results]
            keyword_scores = [r['keyword_score'] for r in results]

            fig, ax = plt.subplots(figsize=(10, 5))
            sns.set(style="whitegrid")

            ax.plot(names, keyword_scores, marker='o', linestyle='--', color='orange', label='Traditional (Keyword Score)')
            ax.plot(names, ai_scores, marker='s', linestyle='-', color='green', label='AI-based (Semantic Score)')

            ax.set_xlabel("Candidate Name")
            ax.set_ylabel("Score")
            ax.set_title("Semantic AI vs Traditional ATS Scoring")
            ax.legend()
            plt.xticks(rotation=20)
            st.pyplot(fig)

            st.markdown("""
            **🧠 AI-based ATS vs Traditional Keyword-Based ATS**

            | Criteria                    | Traditional ATS | AI-based ATS |
            |-----------------------------|------------------|---------------|
            | Understands context         | ❌                | ✅             |
            | Synonym & phrase matching   | ❌                | ✅             |
            | Fairness in ranking         | ⚠️                | ✅             |
            | Skill match accuracy        | Moderate         | High          |

            ➡️ **Conclusion**: AI-based scoring provides more accurate, context-aware rankings and highlights candidates with relevant skills, even if wording differs.
            """)

        else:
            st.info("No suitable candidates found or scoring failed.")
