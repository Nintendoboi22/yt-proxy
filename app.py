from flask import Flask, request, Response
import requests

app = Flask(__name__)
YOUTUBE_BASE = "https://www.youtube.com"
@app.route("/")
def youtube():
    try:
        response = requests.get("https://www.youtube.com", headers={"User-Agent": "Mozilla/5.0"})
        return Response(response.content, content_type=response.headers["Content-Type"])
    except Exception as e:
        return f"Error fetching YouTube: {str(e)}", 500

@app.route("/robots.txt")
def robots():
    try:
        response = requests.get("robots.txt")
        return Response(response.content, content_type=response.headers["Content-Type"])
    except Exception as e:
        return f"Error fetching robots.txt: {str(e)}", 500

@app.errorhandler(404)
def not_found(e):
    param = request.full_path
    try:
        response = requests.get(f"{YOUTUBE_BASE}{param}")
        return Response(response.content, content_type=response.headers["Content-Type"])
    except Exception as e:
        return str(e), 500

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app)
handler = app