# 🤖 End-to-End Resume AI Parser

An end-to-end AI-powered resume parsing system that extracts structured information from resumes in **PDF, DOCX, and TXT** formats.

The system leverages a fine-tuned **RoBERTa-base Transformer model** using **spaCy Transformers**, served through a **FastAPI backend** and an intuitive **React frontend**.

**Achieved 96.77% F1-score on Resume Entity Recognition.**

---

## 🚀 Project Overview

This project automatically extracts key information from resumes and converts unstructured text into structured data suitable for:

* Applicant Tracking Systems (ATS)
* Recruitment Platforms
* HR Analytics
* Candidate Search & Matching
* Resume Screening Automation

### Extracted Entities

| Entity             | Description                              |
| ------------------ | ---------------------------------------- |
| 🎯 Skills          | Technical and professional skills        |
| 💼 Work Experience | Employment history and job experience    |
| 🎓 Education       | Academic qualifications and institutions |
| 🌍 Languages       | Spoken and written languages             |

---

## 📊 Model Performance

### Dataset Statistics

| Metric                   | Value      |
| ------------------------ | ---------- |
| Total Resumes            | 60         |
| Total Annotated Entities | 1,555      |
| Training Set             | 42 Resumes |
| Validation Set           | 8 Resumes  |
| Test Set                 | 10 Resumes |

### Model Details

* **Architecture:** RoBERTa-base
* **Framework:** spaCy Transformers
* **Task:** Named Entity Recognition (NER)
* **Fine-Tuning:** Custom annotated resume dataset

### Final Evaluation

| Metric    | Score      |
| --------- | ---------- |
| Precision | 96.85%     |
| Recall    | 96.69%     |
| F1-Score  | **96.77%** |

---

## ✨ Features

### 📂 Multi-Format Resume Support

* PDF (.pdf)
* Microsoft Word (.docx)
* Plain Text (.txt)

### 🤖 AI-Powered Information Extraction

Automatically identifies and extracts:

* 🎯 Skills
* 💼 Work Experience
* 🎓 Education
* 🌍 Languages

### ⚡ Fast Processing

* Real-time parsing
* Structured JSON output
* REST API support

### 💻 Full-Stack Application

* Modern React Frontend
* FastAPI Backend
* Transformer-based NLP Pipeline

---

## 🏗️ System Architecture

```text
Resume Upload
      │
      ▼
Document Parsing
(pdfplumber / docx2txt)
      │
      ▼
Text Extraction
      │
      ▼
RoBERTa-based NER Model
(spaCy Transformers)
      │
      ▼
Entity Recognition
      │
      ▼
Structured JSON Output
      │
      ▼
Frontend Display / API Response
```

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn
* spaCy
* spaCy Transformers
* Hugging Face Transformers

### Frontend

* React
* Next.js
* TypeScript

### Document Processing

* pdfplumber
* docx2txt

### Machine Learning

* RoBERTa-base
* Named Entity Recognition (NER)

---

## 📁 Project Structure

```text
resume-parser/
│
├── backend/
│   ├── main.py
│   ├── model/
│   ├── routes/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── dataset/
│   ├── train/
│   ├── dev/
│   └── test/
│
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/resume-parser.git

cd resume-parser
```

---

### 2. Backend Setup

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

---

### 3. Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs at:

```text
http://localhost:3000
```

---

## 🔌 API Usage

### Parse Resume

**Endpoint**

```http
POST /parse
```

### Example Request

```bash
curl -X POST "http://localhost:8000/parse" \
     -F "file=@sample_resume.pdf"
```

### Example Response

```json
{
  "skills": [
    "Python",
    "React",
    "FastAPI",
    "Machine Learning"
  ],
  "experience": [
    "Software Engineer at XYZ"
  ],
  "education": [
    "B.Tech in Information Technology"
  ],
  "languages": [
    "English",
    "Hindi"
  ]
}
```

---

## 🎯 Use Cases

* Applicant Tracking Systems (ATS)
* Resume Screening Automation
* Candidate Profiling
* Recruitment Analytics
* Talent Search Platforms
* HR Workflow Automation

---

## 🔮 Future Improvements

* Support for additional resume sections
* Resume ranking and matching
* Skill recommendation engine
* Candidate-job fit scoring
* Multilingual resume parsing
* Docker deployment
* Cloud deployment (AWS/GCP/Azure)

---

## 👨‍💻 Author

**Satvik Malkoti**

B.Tech (Information Technology)
Machine Learning • NLP • Full-Stack Development

---

## 📜 License

This project is licensed under the MIT License.

Feel free to fork, improve, and contribute.
