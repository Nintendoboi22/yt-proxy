import requests
from flask import Flask, request, Response

app = Flask(__name__)

YOUTUBE_BASE = "https://www.youtube.com"

@app.route("/")
def home():
    return "YouTube Proxy is Running!"

@app.route("/proxy")
def proxy():
    url = request.args.get("url")
    if not url or "youtube.com" not in url:
        return "Invalid URL", 400
    
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    return Response(response.content, content_type=response.headers["Content-Type"])

if __name__ == "__main__":
    app.run(debug=True)
