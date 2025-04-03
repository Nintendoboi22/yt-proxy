from flask import Flask, render_template, request, Response
import requests

app = Flask(__name__)

YOUTUBE_BASE = "https://www.youtube.com"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/proxy")
def proxy():
    url = request.args.get("url")
    if not url or "youtube.com" not in url:
        return "Invalid URL", 400
    
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    return Response(response.content, content_type=response.headers["Content-Type"])

if __name__ == "__main__":
    app.run(debug=True)
