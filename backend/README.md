# NOMS Backend

FastAPI backend for Network Operations & Monitoring System.

## Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python -m scripts.create_admin
uvicorn app.main:app --reload