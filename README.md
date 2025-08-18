# 📄 AI-Powered Applicant Tracking System (ATS)

An **AI-based Applicant Tracking System (ATS)** built with **Streamlit**, **PyMuPDF**, and **Sentence-BERT** that helps recruiters **automatically extract resume information, rank candidates, and compare AI-based scoring with traditional keyword matching**.

---

## 🚀 Features

- **Resume Parsing**: Extracts text, email, phone, and skills from PDF resumes using `PyMuPDF`.
- **Semantic Similarity Scoring**: Uses **Sentence-BERT** (`all-MiniLM-L6-v2`) to compute AI-based similarity between resume and job description.
- **Keyword Matching**: Implements traditional keyword-based scoring for benchmarking.
- **Candidate Ranking**: Scores resumes using a weighted combination of AI-based and keyword-based similarity.
- **Skill Matching**: Highlights skills from resumes that match the job description.
- **Visualization**: Compare **AI-based ATS vs Traditional ATS** performance with plots.
- **CSV Export**: Download top-ranked candidate results in CSV format.
- **Interactive UI**: Simple and clean interface built with **Streamlit**.

---

## 🛠️ Tech Stack

- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **Resume Parsing**: [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- **Semantic Search**: [Sentence-BERT](https://www.sbert.net/)
- **NLP Tools**: [NLTK](https://www.nltk.org/)
- **Visualization**: [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/)
- **Data Handling**: [Pandas](https://pandas.pydata.org/)

---

## 📂 Project Structure

.
├── app.py # Main Streamlit app
├── requirements.txt # Python dependencies
├── README.md # Documentation
└── sample_resumes/ # (Optional) Example resumes for testing

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

git clone https://github.com/<your-username>/ai-ats.git
cd ai-ats
###2. Create Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
3. Install Dependencies
pip install -r requirements.txt
