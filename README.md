# AI Resume Analyzer & Job Matcher

An end-to-end full-stack intelligent recruitment and career optimization application. It extracts skills, qualifications, contact info, and metrics from uploaded PDF resumes using Natural Language Processing (NLP), evaluates alignment against target job descriptions, computes ATS compatibility scores, and delivers actionable recommendations with missing skill breakdowns.

---

## 🌟 Key Features

1. **Resume Ingestion & Parsing (PDF & Plain Text)**:
   - High-fidelity PDF text extraction using `pypdf`.
   - Contact info extraction: Candidate Name, Email, Phone, LinkedIn, GitHub.
   - Section detection: Summary, Experience, Education, Skills, Projects, Certifications.
   - Quantified achievements & KPI detection (percentages, revenue, multipliers, latency reductions).
   - Power action verbs detection (e.g. *Architected*, *Spearheaded*, *Optimized*).

2. **NLP Skills Extraction Engine**:
   - Broad taxonomy of 400+ technical and soft skills spanning Programming Languages, Frontend, Backend, Databases, Cloud/DevOps, AI/ML/Data Science, System Design, and Methodologies.
   - Boundary-aware n-gram matching preventing false positives (e.g. handles `C`, `R`, `Go`, `C++`, `Node.js`, `.NET Core`, `CI/CD`).
   - Synonym normalization mapping (e.g. `k8s` → `Kubernetes`, `reactjs` → `React`, `aws` → `AWS`, `sklearn` → `Scikit-learn`).

3. **Intelligent Job Matching Algorithm**:
   - **Skill Match Score**: Ratio of required skills present in candidate resume.
   - **Semantic / Contextual Relevance**: Cosine Similarity via TF-IDF vectorization across resume content and job specifications.
   - **Composite Match Score**: Weighted balance (65% skill coverage + 35% semantic context).

4. **ATS Compatibility & Readiness Scoring**:
   - Section completeness audit against ATS guidelines.
   - Contact information integrity check.
   - Measurable metrics & business impact scoring.
   - Action verbs density scoring.

5. **Actionable Improvement Recommendations**:
   - Prioritized missing skills (High vs Medium priority).
   - ATS formatting suggestions.
   - Google XYZ formula recommendations for bullet points (`Accomplished [X] as measured by [Y] by doing [Z]`).
   - Suggested projects and courses to bridge detected gaps.

6. **SQLite Storage & Scan History**:
   - Complete persistence of resumes, parsed entities, job targets, and match history.
   - History viewer modal with search and 1-click restore.

7. **Modern React Frontend**:
   - Sleek responsive UI with Tailwind CSS and Lucide icons.
   - Animated SVG circular match gauges.
   - Filterable skills comparison chips (Matched, Missing, Bonus Skills).
   - 1-Click "Load Demo Sample" for instant testing.
   - PDF print/export support.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn, SQLite3, Pydantic, Scikit-learn, PyPDF.
- **Frontend**: React 18, Vite, Tailwind CSS, Lucide React.
- **Storage**: SQLite (`backend/resumes.db`).

---

## 📁 Project Architecture

```
AI project/
├── backend/
│   ├── database.py             # SQLite connection, schemas, and queries
│   ├── models.py               # Pydantic request/response validation
│   ├── parser.py               # PDF parser, regex extractors, section auditor
│   ├── nlp_engine.py           # NLP skills taxonomy, TF-IDF cosine similarity, matching engine
│   ├── sample_data.py          # Pre-loaded sample jobs and candidate profiles
│   ├── main.py                 # FastAPI application and REST endpoints
│   ├── create_sample_pdf.py    # Generates sample PDF resumes
│   ├── test_backend.py         # Backend automated tests
│   ├── test_api.py             # API endpoints integration tests
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── ResumeUploader.jsx
│   │   │   ├── JobDescriptionInput.jsx
│   │   │   ├── MatchScoreCard.jsx
│   │   │   ├── SkillsComparison.jsx
│   │   │   ├── ImprovementSuggestions.jsx
│   │   │   ├── ResumeOverview.jsx
│   │   │   └── HistoryModal.jsx
│   │   ├── api.js              # REST client wrapper
│   │   ├── App.jsx             # Main dashboard
│   │   ├── index.css           # Tailwind base & utilities
│   │   └── main.jsx
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── package.json
├── sample_resumes/             # Ready-to-use sample PDF resumes
│   ├── Alex_Morgan_Resume.pdf
│   └── Priya_Sharma_Resume.pdf
├── run_app.py                  # One-command dual server launcher
└── README.md
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 2. Backend Setup
From the root folder:
```bash
cd backend
pip install -r requirements.txt
```

### 3. Frontend Setup
From the root folder:
```bash
cd frontend
npm install
```

### 4. Run the Full Application (Single Command)
Run from the root directory:
```bash
python run_app.py
```

This starts:
- **Frontend UI**: [http://localhost:5173](http://localhost:5173)
- **FastAPI Backend**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Running Automated Tests

Run the backend unit and integration tests:
```bash
python backend/test_backend.py
python backend/test_api.py
```

---

## 📡 API Endpoints Summary

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Health check endpoint |
| `POST` | `/api/upload-resume` | Upload PDF file, extract text, sections, and candidate skills |
| `POST` | `/api/analyze` | Match resume text against job description, return score and suggestions |
| `GET` | `/api/history` | Retrieve past analysis scans |
| `GET` | `/api/history/{id}` | Retrieve full details of an analysis |
| `DELETE` | `/api/history/{id}` | Delete a scan from database |
| `GET` | `/api/sample-jobs` | List pre-configured job roles (Full Stack, ML, DevOps, Data Science) |
| `GET` | `/api/sample-resumes` | List pre-configured sample resumes |

