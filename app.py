from flask import Flask, jsonify, render_template, send_from_directory , request
import pandas as pd
from flask_cors import CORS
import os
import subprocess
import sys


app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join("data", "ai_news.csv")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/articles")
def get_articles():
    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "Data file not found. Run the scraper first."}), 404
    
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    df = pd.read_csv(DATA_FILE)
    df.columns = [c.strip().lower() for c in df.columns]

    df["scraped_at"] = pd.to_datetime(df["scraped_at"], errors="coerce")

    
    # Remove rows with empty titles
    df = df[df["title"].notna() & (df["title"].str.strip() != "")]

    df = df.sort_values(by="scraped_at", ascending=False)

    start = (page - 1) * limit
    end = start + limit
    df = df.iloc[start:end]

    # Convert scraped_at to ISO string so JSON serialization works correctly
    df["scraped_at"] = df["scraped_at"].dt.strftime("%Y-%m-%dT%H:%M:%S").fillna("")
    # Replace remaining NaN with empty string so JSON stays valid
    df = df.fillna("")
    return jsonify(df.to_dict(orient="records"))

@app.route("/refresh", methods=["POST"])
def refresh_articles():
    """Trigger the scraper pipeline (main.py) and return status."""
    try:
        result = subprocess.run(
            [sys.executable, "main.py"],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode != 0:
            return jsonify({"status": "error", "message": result.stderr or "Scraper failed"}), 500
        return jsonify({
            "status": "ok",
            "message": "Scraper completed successfully",
            "output": result.stdout
        })
    except subprocess.TimeoutExpired:
        return jsonify({"status": "error", "message": "Scraper timed out after 5 minutes"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)