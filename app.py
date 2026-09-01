from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Planted Secret so Gitleaks catches it (Never do in a Real setting)
AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE"

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/greet")
def greet():
    name = request.args.get("name", "world")
    return jsonify({"message": f"Hello, {name}"})

# Planted vulnerability so Semgrep flags it: user input into a shell = command injection
@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=true, text=true)
    return jsonify({"output": result.stdout})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)