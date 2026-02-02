# app.py
# =====================================================
# STRICT EXAM ANSWERS + FACT CHECK (SEARXNG)
# → EACH ANSWER SAVED AS MD
# → ONE FINAL COMBINED MD
# → ONE FINAL PDF
# =====================================================

from flask import Flask, request, jsonify, send_file, render_template
import threading
import time
import ollama
import requests
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

# =====================================================
# CONFIG
# =====================================================
MODEL_NAME = "gemma3:4b"

SEARXNG_BASE_URL = "http://44.44.44.144:9017"
SEARXNG_SEARCH_ENDPOINT = "/search"
SEARX_DELAY = 3.0
MAX_RESULTS = 5

BASE_DIR = Path(__file__).resolve().parent
MD_DIR = BASE_DIR / "md"
OUT_DIR = BASE_DIR / "output"
MD_DIR.mkdir(exist_ok=True)
OUT_DIR.mkdir(exist_ok=True)

REQUEST_HEADERS = {
    "User-Agent": "LawExamBot/1.0 (+self-hosted)"
}

DOMAIN_PRIORITY = {
    "indiankanoon.org": 5,
    "sci.gov.in": 5,
    "supremecourtofindia.nic.in": 5,
    "highcourts.gov.in": 4,
    "gov.in": 4,
    "scconline.com": 4,
}

app = Flask(__name__)
tasks = {}
lock = threading.Lock()

# =====================================================
# UTILS
# =====================================================
def log(msg):
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] {msg}", flush=True)

def slugify(text: str) -> str:
    return "".join(c.lower() if c.isalnum() else "_" for c in text).strip("_")[:80]

def domain_score(url: str) -> int:
    host = urlparse(url).netloc.lower()
    for d, s in DOMAIN_PRIORITY.items():
        if d in host:
            return s
    return 1

# =====================================================
# SEARXNG FACT CHECK
# =====================================================
def searx_fact_check(query: str):
    time.sleep(SEARX_DELAY)

    resp = requests.get(
        SEARXNG_BASE_URL + SEARXNG_SEARCH_ENDPOINT,
        params={"q": f"{query} site:indiankanoon.org OR site:gov.in", "format": "json"},
        headers=REQUEST_HEADERS,
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()

    results = []
    for r in data.get("results", []):
        if r.get("url") and r.get("content"):
            results.append({
                "content": r["content"],
                "score": domain_score(r["url"]),
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:MAX_RESULTS]

# =====================================================
# PROMPTS
# =====================================================
def exam_prompt(q):
    return f"""
You are writing a STRICT EXAM ANSWER for an Indian law examination.

EXAM RULES (MANDATORY):
- Answer ONLY what is asked.
- Use clear, point-wise format.
- Give slight explanation only where necessary.
- Mention relevant statutory provisions briefly.
- Mention ONLY ONE most important case law.
- Case law: name + one-line principle only.
- No academic discussion, no illustrations.
- Keep the answer concise and scoring-oriented.

FORMAT (DO NOT DEVIATE):
1. Meaning / Direct Answer
2. Statutory Provision
3. Essential Points (with slight explanation)
4. Case Law (ONE only)
5. Conclusion

End with:
Confidence Level: XX%

QUESTION:
{q}

ANSWER:
""".strip()

def fact_check_prompt(q, exam_answer, ctx):
    return f"""
Verify the EXAM ANSWER using SEARCH CONTEXT.
Correct only factual/legal errors.
Do NOT expand.
Keep structure identical.

QUESTION:
{q}

EXAM ANSWER:
{exam_answer}

SEARCH CONTEXT:
{ctx}

FINAL VERIFIED ANSWER:
""".strip()

# =====================================================
# MD → PDF
# =====================================================
def md_to_pdf(md_path: Path, pdf_path: Path):
    subprocess.run(
        ["pandoc", str(md_path), "-o", str(pdf_path), "--pdf-engine=wkhtmltopdf"],
        check=True,
    )

# =====================================================
# ROUTES
# =====================================================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/exam", methods=["POST"])
def exam():
    data = request.get_json(force=True, silent=True) or {}
    questions = data.get("questions", [])
    if not questions:
        return jsonify({"error": "No questions"}), 400

    task_id = str(int(time.time() * 1000))
    log(f"Task {task_id} started")

    with lock:
        tasks[task_id] = {
            "current": 0,
            "total": len(questions),
            "answers": [None] * len(questions),
            "final_pdf": None,
        }

    def worker():
        combined_md = ["# LAW EXAM ANSWERS (VERIFIED)\n"]

        for i, q in enumerate(questions):
            try:
                exam_ans = ollama.generate(
                    model=MODEL_NAME,
                    prompt=exam_prompt(q),
                    options={"temperature": 0.15},
                )["response"].strip()

                sources = searx_fact_check(q)
                ctx = "\n".join(f"- {s['content']}" for s in sources)

                final_ans = ollama.generate(
                    model=MODEL_NAME,
                    prompt=fact_check_prompt(q, exam_ans, ctx),
                    options={"temperature": 0.1},
                )["response"].strip()

                md_path = MD_DIR / f"{slugify(q)}.md"
                md_path.write_text(f"# {q}\n\n{final_ans}\n", encoding="utf-8")

                combined_md.append(f"## {q}\n\n{final_ans}\n")

                with lock:
                    tasks[task_id]["answers"][i] = final_ans
                    tasks[task_id]["current"] = i + 1

            except Exception as e:
                log(f"ERROR: {e}")

        final_md = OUT_DIR / f"{task_id}_final.md"
        final_pdf = OUT_DIR / f"{task_id}_final.pdf"
        final_md.write_text("\n\n".join(combined_md), encoding="utf-8")
        md_to_pdf(final_md, final_pdf)

        with lock:
            tasks[task_id]["final_pdf"] = final_pdf.name

        log(f"Task {task_id} completed")

    threading.Thread(target=worker, daemon=True).start()
    return jsonify({"task_id": task_id})

@app.route("/progress/<task_id>")
def progress(task_id):
    with lock:
        t = tasks.get(task_id)
    if not t:
        return jsonify({"error": "Invalid task"}), 404
    return jsonify(t)

@app.route("/download/pdf/<name>")
def download_pdf(name):
    return send_file(OUT_DIR / name, mimetype="application/pdf")

# =====================================================
# ENTRY
# =====================================================
if __name__ == "__main__":
    log("Starting Exam + Fact-Check Server")
    app.run(host="0.0.0.0", port=5000, debug=True)
