FROM python:3.11-slim
WORKDIR /app
# FIX: upgrade the vulnerable build tooling that ships in the base image
# (Trivy flagged jaraco.context and wheel with fixable HIGH CVEs)
RUN pip install --no-cache-dir --upgrade pip wheel "jaraco.context>=6.1.0"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 8080
RUN useradd -m appuser
USER appuser
CMD ["python", "app.py"]