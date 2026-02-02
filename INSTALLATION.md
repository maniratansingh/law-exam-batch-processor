# System Requirements, Dependencies, and Installation Guide

This document provides a **complete, step-by-step installation guide** for setting up the **Law Exam Batch Processor** in a clean, production-ready manner. It explicitly lists **all system requirements, runtime dependencies, models, and services**.

---

## 1. System Requirements

### Operating System

- **Linux (Recommended)**
  - Ubuntu 20.04 / 22.04 / 24.04
  - Debian 11 / 12 / 13

> The application is tested and optimized for Linux environments. Other operating systems are not officially supported.

---

### Hardware

- **CPU**: 4 cores minimum (8 cores recommended)
- **RAM**:
  - Minimum: **8 GB**
  - Recommended: **16 GB or more** (for stable LLM inference)
- **Storage**:
  - Minimum: 10 GB free
  - Recommended: SSD or NVMe

> **GPU is REQUIRED and strongly recommended.**

- **Tested GPU**: NVIDIA RTX 3050 (8 GB VRAM)
- **Minimum VRAM**: 8 GB
- **CUDA support** required for stable and fast inference

> CPU-only inference is **not supported** for production use and may result in timeouts or degraded output quality.

---

### Software

- **Python**: 3.10 or higher
- **pip**: Latest version
- **Git**: For source control

---

## 2. Core Dependencies (Mandatory)

### Python Libraries

These are required for backend operation:

- **Flask** – Web framework
- **requests** – HTTP client
- **ollama** – Python client for local LLM runtime

Install via:

```bash
pip install flask requests ollama
```

---

### System Packages

Required for document generation:

- **Pandoc** – Markdown processor
- **wkhtmltopdf** – PDF rendering engine

Install on Debian / Ubuntu:

```bash
sudo apt update
sudo apt install -y pandoc wkhtmltopdf
```

Verify installation:

```bash
pandoc --version
wkhtmltopdf --version
```

---

## 3. GPU Requirement (Mandatory)

This application is **validated and tested with GPU acceleration**.

### Supported GPU

- NVIDIA RTX 3050 (8 GB VRAM) — **tested and verified**
- Other NVIDIA GPUs with **≥8 GB VRAM** may work but are not officially tested

### NVIDIA Driver & CUDA

Ensure the following are installed:

```bash
nvidia-smi
```

If not present, install:

```bash
sudo apt install nvidia-driver nvidia-cuda-toolkit
```

---

## 4. Ollama (Local LLM Runtime)

### What is Ollama?

**Ollama** is a local Large Language Model runtime that allows fully offline inference without sending data to third-party servers.

This project **requires Ollama** for answer generation and verification.

---

### Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Start the service:

```bash
ollama serve
```

Verify:

```bash
ollama --version
```

---

## 4. Language Model Requirement

### Required Model

- **Model Name**: `gemma3:4b`
- **Provider**: Google DeepMind (Gemma family)

Pull the model:

```bash
ollama pull gemma3:4b
```

> The system is tuned specifically for **Gemma 3 (4B)** due to its balance of reasoning quality and low resource usage.

---

## 5. SearXNG (Self-Hosted Search Engine)

### Purpose

SearXNG is used exclusively for **fact-checking and legal verification** against authoritative Indian legal domains.

No public search APIs are used.

---

### Deployment (Docker – Recommended)

```bash
docker run -d \
  -p 9017:8080 \
  -v searxng:/etc/searxng \
  --name searxng \
  searxng/searxng
```

Verify JSON endpoint:

```bash
curl "http://localhost:9017/search?q=IPC+420&format=json"
```

---

### Configure Application

Update in `app.py`:

```python
SEARXNG_BASE_URL = "http://localhost:9017"
```

Ensure `/search?format=json` is accessible.

---

## 6. Application Setup

### Clone Repository

```bash
git clone <your-repository-url>
cd law-exam-batch-processor
```

---

### Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Install Python Dependencies

```bash
pip install flask requests ollama
```

---

## 7. Running the Application

```bash
python app.py
```

Access the UI at:

```text
http://localhost:5000
```

---

## 8. Optional (Production Hardening)

- Run behind **Nginx**
- Disable Flask debug mode
- Use systemd for Ollama and Flask
- Restrict SearXNG to local network

---

## 9. Dependency Credits

This project depends on the following open-source components:

- **Python** – Programming language
- **Flask** – Web framework
- **Requests** – HTTP client library
- **Ollama** – Local LLM runtime
- **Gemma Models** – Google DeepMind
- **SearXNG** – Privacy-respecting search engine
- **Pandoc** – Document conversion
- **wkhtmltopdf** – PDF generation

All trademarks and copyrights belong to their respective owners.

---

## 10. Notes

- Internet access is required **only** for model download and search indexing
- All inference remains local
- Suitable for offline exam preparation after setup

---

End of documentation.

