# Starting point: a small Linux image with Python 3.11
FROM python:3.11-slim

# Hugging Face runs containers as a normal user (id 1000), so we create one
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

# Install libraries first (Docker caches this step, so rebuilds are fast).
# CPU-only torch is much smaller than the default build, and free hosting has no GPU.
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Download both models now so the website doesn't have to on the first visit
RUN python -c "from transformers import pipeline; pipeline('summarization', model='google/pegasus-cnn_dailymail'); pipeline('translation', model='facebook/m2m100_418M')"

# Copy our code in
COPY --chown=user . .

# Hugging Face expects the app on port 7860
EXPOSE 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
