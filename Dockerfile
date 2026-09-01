From python:3.11-slim
WORKDIR /app
COPY reqirements.txt .
EXPOSE 8080
CMD ["python", "app.py"]