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
```bash
git clone https://github.com/<your-username>/ai-ats.git
cd ai-ats
```
**2. Create Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```
**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**requirements.txt**

streamlit
pymupdf
pandas
sentence-transformers
nltk
matplotlib
seaborn

**4. Download NLTK Resources**

The script automatically downloads:

punkt

averaged_perceptron_tagger

stopwords

wordnet

But you can also run:
```bash
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('wordnet')
```
**5. Run the App**
```bash
streamlit run app.py
```

The app will open at http://localhost:8501/

**🎮 Usage**

Paste the Job Description in the text area.

Upload one or multiple Resume PDFs.

Select the number of candidates to shortlist.

Click on "🚀 Compare and Rank".

View ranked candidates with:

Extracted info (name, email, mobile, skills).

AI vs keyword-based score.

Matched skills from JD.

Option to preview resume text.

Export results to CSV.

View ATS efficiency comparison plots.

**📊 Example Output**
Candidate Ranking
1. John Doe (john@example.com, 📞 +91-9876543210)
   ✅ Final Score: 0.85 (AI: 0.88, Keyword: 0.76)
   🧠 Extracted Skills: Python, Flask, SQL
   🎯 Matched Skills: Python, SQL

Visualization
<img width="1918" height="865" alt="image" src="https://github.com/user-attachments/assets/97bb0404-f7bb-4d3e-bd8c-6a2e9c8c433c" />
<img width="1915" height="858" alt="image" src="https://github.com/user-attachments/assets/08e77f17-9d96-40b3-85c0-6d89acb91770" />

AI vs Keyword-based Scoring Plot
<img width="1285" height="795" alt="image" src="https://github.com/user-attachments/assets/33433ad2-f7e2-4679-b353-d83ecd4430a5" />



**🔍 How it Works**

Resume Parsing
Extracts raw text and applies regex-based patterns to detect name, email, phone, and skills.

Scoring System

AI Score → Sentence-BERT semantic similarity between resume and JD.

Keyword Score → Overlap ratio of words between resume and JD.

Final Score → Weighted combination: 0.7 * AI Score + 0.3 * Keyword Score.

Ranking & Shortlisting
Sorts candidates by score and selects the top-N as per user input.

Visualization
Plots AI vs Keyword-based scores for fairness and accuracy analysis.

**📌 Roadmap**

 Add support for DOCX resumes.

 Enhance Named Entity Recognition (NER) for skill extraction.

 Multi-language support.

 Deploy on Streamlit Cloud / Hugging Face Spaces.

**🤝 Contributing**

Contributions are welcome! Please follow these steps:

Fork the repo

Create a feature branch (git checkout -b feature-xyz)

Commit your changes (git commit -m "Added xyz feature")

Push to branch (git push origin feature-xyz)

Open a Pull Request 🎉

**👨‍💻 Author**

Jannela Sai Venkat Suraj
B.Tech CSE | AI & ML Enthusiast | Full-stack & ML Developer
🔗 LinkedIn | GitHub

**⭐ Acknowledgements**

Streamlit

Sentence-BERT

PyMuPDF

NLTK
