from flask import Flask, request, jsonify
import subprocess
import shlex

app = Flask(__name__)

# FIX 1: Secret removed entirely.
# Real secrets belong in environment variables / a secrets manager, never in code.
# (nothing here anymore — that's the point)


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/greet")
def greet():
    name = request.args.get("name", "world")
    return jsonify({"message": f"Hello, {name}"})

# FIX 2: Command injection fixed.
# - Validate the input (only allow hostname-safe characters)
# - Use a list of args with shell=False (no shell interpretation)
# - Never pass user input into a shell string


@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    # Only allow simple hostnames/IPs — reject anything with shell metacharacters
    if not all(c.isalnum() or c in ".-" for c in host):
        return jsonify({"error": "invalid host"}), 400
    # shell=False + list args = the shell never interprets the input
    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True, text=True, timeout=5
    )
    return jsonify({"output": result.stdout})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
