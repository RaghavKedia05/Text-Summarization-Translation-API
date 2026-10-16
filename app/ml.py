# This file holds the two AI models and the functions that use them.
from transformers import pipeline  # Hugging Face helper that wraps model + tokenizer

# Pretrained models, downloaded from Hugging Face the first time they are used
SUMMARIZER_MODEL = "google/pegasus-cnn_dailymail"  # Pegasus: writes abstractive summaries
TRANSLATOR_MODEL = "facebook/m2m100_418M"          # M2M100: translates between 100 languages

# Languages shown in the web page (code -> name). M2M100 uses these codes.
LANGUAGES = {
    "en": "English", "hi": "Hindi", "pa": "Punjabi", "bn": "Bengali",
    "ta": "Tamil", "mr": "Marathi", "gu": "Gujarati", "ur": "Urdu",
    "fr": "French", "de": "German", "es": "Spanish", "it": "Italian",
    "pt": "Portuguese", "ru": "Russian", "ja": "Japanese", "ko": "Korean",
    "zh": "Chinese", "ar": "Arabic",
}

# Models are big, so we load each one only once, on the first request, and reuse it
_summarizer = None
_translator = None


def summarize(text, min_length, max_length):
    global _summarizer
    if _summarizer is None:  # first call: load the model
        _summarizer = pipeline("summarization", model=SUMMARIZER_MODEL)
    # truncation=True cuts input that is longer than the model can read
    result = _summarizer(text, min_length=min_length, max_length=max_length, truncation=True)
    # Pegasus marks line breaks with "<n>", so we swap them for spaces
    return result[0]["summary_text"].replace("<n>", " ")


def translate(text, source_lang, target_lang):
    global _translator
    if _translator is None:  # first call: load the model
        _translator = pipeline("translation", model=TRANSLATOR_MODEL)
    result = _translator(text, src_lang=source_lang, tgt_lang=target_lang, max_length=400)
    return result[0]["translation_text"]
