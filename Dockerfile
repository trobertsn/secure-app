# ---- STAGE 1: builder ----
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt

# ---- STAGE 2: final runtime ----
FROM python:3.11-slim
WORKDIR /app
# Upgrade the base image's build tooling to patched versions,
# then remove pip's cache. This clears the flagged setuptools/wheel CVEs.
RUN pip install --no-cache-dir --upgrade "setuptools>=78.1.1" "wheel>=0.46.2" \
    && pip uninstall -y pip 2>/dev/null || true
COPY --from=builder /app/deps /app/deps
ENV PYTHONPATH=/app/deps
COPY app.py .
EXPOSE 8080
RUN useradd -m appuser
USER appuser
CMD ["python", "app.py"]