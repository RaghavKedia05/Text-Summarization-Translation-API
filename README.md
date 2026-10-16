---
title: Text Summarization & Translation API
emoji: 📝
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
---

# Transformer-Based Text Summarization & Translation API

A FastAPI service with a web page. It uses two pretrained Hugging Face models:

- **Summarization:** Pegasus (`google/pegasus-cnn_dailymail`) writes a short abstractive summary.
- **Translation:** M2M100 (`facebook/m2m100_418M`) translates between 18 languages.

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 for the web page, or http://127.0.0.1:8000/docs for the API docs.
The first request downloads the models (about 4 GB total), so it is slow. After that it is fast.

## Endpoints

| Method | URL | Body | Returns |
|---|---|---|---|
| GET | `/api/languages` | none | language codes and names |
| POST | `/api/summarize` | `text`, `min_length`, `max_length` | `summary` |
| POST | `/api/translate` | `text`, `source_lang`, `target_lang` | `translation` |

## Files

```
app/ml.py          loads the two models, has summarize() and translate()
app/main.py        the API routes
static/index.html  the web page (HTML + CSS + JavaScript in one file)
```

## How it works

1. The browser sends text to an API route with `fetch`.
2. FastAPI checks the input (length limits, language codes) and calls a function in `ml.py`.
3. `ml.py` loads the model on first use, runs it, and returns the result.
4. The browser shows the result.
