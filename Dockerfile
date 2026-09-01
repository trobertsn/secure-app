FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 8080
# FIX: run as a non-root user (Semgrep flagged the missing USER)
RUN useradd -m appuser
USER appuser
CMD ["python", "app.py"]