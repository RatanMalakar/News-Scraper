from flask import Flask, jsonify, render_template, send_from_directory
import pandas as pd
from flask_cors import CORS
import os

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
    df = pd.read_csv(DATA_FILE)
    df.columns = [c.strip().lower() for c in df.columns]
    # Remove rows with empty titles
    df = df[df["title"].notna() & (df["title"].str.strip() != "")]
    # Replace NaN with empty string so JSON stays valid
    df = df.fillna("")
    return jsonify(df.to_dict(orient="records"))

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)