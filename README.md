# Law Exam Batch Processor

Enterprise‑grade, self‑hosted system for generating **strict, exam‑oriented Indian law answers**, performing **domain‑prioritized fact‑checking**, and exporting **verified PDFs**.

---

## 1. Overview

**Law Exam Batch Processor** is a production‑ready Flask application designed for Indian law students, researchers, and legal professionals who require:

* Strict, marks‑oriented exam answers
* Minimal but authoritative case‑law usage
* Statute‑first accuracy with verification
* Batch processing of questions
* Single consolidated, printable PDF output

The system combines:

* Local LLM inference (Ollama)
* Self‑hosted metasearch (SearXNG)
* Deterministic prompt control
* Pandoc + wkhtmltopdf publishing

---

## 2. Architecture

### Backend

* **Flask** – REST API and task orchestration
* **Threaded workers** – Non‑blocking batch execution
* **Ollama** – Local LLM inference (Gemma 3 4B)
* **SearXNG** – Fact‑checking via Indian legal domains
* **Pandoc + wkhtmltopdf** – Markdown → PDF pipeline

### Frontend

* Pure HTML + CSS + JavaScript (no framework)
* Dark, distraction‑free exam interface
* Live progress polling
* Incremental answer rendering
* One‑click final PDF export

---

## 3. Key Features

* Strict exam‑safe answer format
* One‑case‑law rule enforced
* Statute‑priority verification
* Domain‑weighted search ranking
* Per‑question Markdown archival
* Final combined verified PDF
* Self‑hosted, offline‑friendly
* No third‑party APIs or data leakage

---

## 4. Answer Policy (Exam Mode)

Each answer strictly follows:

1. Meaning / Direct Answer
2. Statutory Provision
3. Essential Points (brief explanation only)
4. Case Law (ONE most relevant case)
5. Conclusion
6. Confidence Level

**Explicitly excluded**:

* Academic discussion
* Multiple case laws
* Illustrations
* Comparative commentary

---

## 5. Fact‑Checking Strategy

* Queries routed through self‑hosted SearXNG
* Domain‑priority scoring
* Preferred sources:

  * indiankanoon.org
  * sci.gov.in
  * supremecourtofindia.nic.in
  * highcourts.gov.in
  * gov.in
* LLM instructed to:

  * Correct errors only
  * Preserve structure
  * Avoid expansion

---

## 6. Directory Structure

```text
project-root/
│
├── app.py              # Flask backend
├── templates/
│   └── index.html      # Frontend UI
├── md/                 # Per‑question markdown
├── output/
│   ├── *_final.md
│   └── *_final.pdf
└── README.md
```

---

## 7. Requirements

### System

* Linux (recommended)
* Python 3.10+
* 8 GB RAM minimum (16 GB recommended)

### Dependencies

* Flask
* requests
* ollama (local runtime)
* pandoc
* wkhtmltopdf
* SearXNG (self‑hosted)

---

## 8. Installation

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd law-exam-batch-processor
```

### 2. Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask requests ollama
```

### 3. Install System Tools

```bash
sudo apt install pandoc wkhtmltopdf
```

### 4. Setup Ollama

```bash
ollama pull gemma3:4b
```

### 5. Setup SearXNG

* Deploy SearXNG (Docker recommended)
* Ensure `/search?format=json` is accessible
* Update `SEARXNG_BASE_URL` in `app.py`

---

## 9. Running the Application

```bash
python app.py
```

Access UI at:

```text
http://localhost:5000
```

---

## 10. API Endpoints

| Endpoint             | Method | Purpose                |
| -------------------- | ------ | ---------------------- |
| /exam                | POST   | Submit batch questions |
| /progress/<task_id>  | GET    | Poll progress          |
| /download/pdf/<name> | GET    | Download final PDF     |

---

## 11. Security & Privacy

* Fully self‑hosted
* No cloud inference
* No third‑party data sharing
* Local network deployment possible
* Suitable for confidential exam preparation

---

## 12. Intended Use

* Law examinations
* Judicial service preparation
* University assessments
* Legal revision notes
* Offline legal research

**Not intended for**:

* Casual Q&A
* Chat‑style responses
* Opinion‑based analysis

---

## 13. License

This project is released under a **permissive open‑source license**.

You are free to:

* Use
* Modify
* Self‑host
* Deploy commercially

Attribution is appreciated.

---

## 14. Credits & Acknowledgements

This project builds upon and credits the following open‑source software and platforms:

* **Python** – Core language runtime
* **Flask** – Web framework
* **Ollama** – Local LLM serving
* **Gemma Models** – Google DeepMind
* **SearXNG** – Privacy‑respecting metasearch engine
* **Pandoc** – Universal document converter
* **wkhtmltopdf** – HTML/Markdown to PDF rendering
* **Indian Kanoon** – Public legal information (referenced, not scraped)

All trademarks and copyrights belong to their respective owners.

---

## 15. Disclaimer

This software is provided for **educational and research purposes**.

While best efforts are made to ensure legal accuracy, users must independently verify answers before reliance in professional or judicial contexts.

---

## 16. Maintainer

Maintained by an independent legal‑tech developer.

Contributions, audits, and improvements are welcome via pull requests.
