# This file defines the web API: the URLs the browser can call.
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import ml  # our model code from ml.py

app = FastAPI(title="Text Summarization & Translation API")

# Folder that holds the web page (index.html)
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


# What the client must send to /api/summarize. FastAPI rejects bad input automatically.
class SummarizeRequest(BaseModel):
    text: str = Field(min_length=40, max_length=20000)  # text to summarize
    min_length: int = 30    # shortest summary, in tokens
    max_length: int = 120   # longest summary, in tokens


# What the client must send to /api/translate
class TranslateRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)  # text to translate
    source_lang: str = "en"                           # language of the text
    target_lang: str = "hi"                           # language to translate into


# GET /api/languages -> the language list for the dropdowns
@app.get("/api/languages")
def languages():
    return ml.LANGUAGES


# POST /api/summarize -> summary of the text
@app.post("/api/summarize")
def summarize(req: SummarizeRequest):
    if req.min_length >= req.max_length:
        raise HTTPException(400, "min_length must be smaller than max_length")
    summary = ml.summarize(req.text, req.min_length, req.max_length)
    return {
        "summary": summary,
        "input_words": len(req.text.split()),
        "summary_words": len(summary.split()),
    }


# POST /api/translate -> translated text
@app.post("/api/translate")
def translate(req: TranslateRequest):
    if req.source_lang not in ml.LANGUAGES or req.target_lang not in ml.LANGUAGES:
        raise HTTPException(400, "Unsupported language code")
    if req.source_lang == req.target_lang:
        raise HTTPException(400, "Source and target languages must differ")
    return {"translation": ml.translate(req.text, req.source_lang, req.target_lang)}


# Serve files from /static, and send the home page (/) to index.html
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC_DIR / "index.html")
