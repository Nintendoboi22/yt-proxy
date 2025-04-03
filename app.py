from flask import Flask, request, send_file, Response
import os
import time
import requests
import youtube_dl

app = Flask(__name__)
YOUTUBE_BASE = "https://www.youtube.com"
PUBLIC_FOLDER = "public"
CORRECT_PASSWORD = "linux123"

@app.route("/")
def home():
    return send_file(os.path.join(PUBLIC_FOLDER, "home.html"))

@app.route("/youtube")
def youtube():
    url = request.args.get("url", YOUTUBE_BASE)
    try:
        response = requests.get(url)
        return Response(response.content, content_type=response.headers["Content-Type"])
    except Exception as e:
        return str(e), 500

@app.route("/error")
def error():
    return "An error occurred."

@app.route("/clear")
def clear():
    password = request.args.get("auth")
    if password != CORRECT_PASSWORD:
        return "Authentication failed."

    deleted_count = 0
    file_count = 0
    oldest_file_date = 0.0

    for file in os.listdir(PUBLIC_FOLDER):
        if file.endswith(".mp4"):
            file_count += 1
            file_path = os.path.join(PUBLIC_FOLDER, file)
            file_age_days = (time.time() - os.path.getmtime(file_path)) / 86400.0
            oldest_file_date = max(oldest_file_date, file_age_days)
            if file_age_days >= 1.0:
                os.remove(file_path)
                deleted_count += 1

    return f"{deleted_count} File(s) deleted out of {file_count} total files. Oldest file is now {oldest_file_date:.2f} days old!"

@app.route("/watch")
def watch():
    video_id = request.args.get("v")
    if not video_id:
        return "Video ID is required.", 400

    watch_url = f"{YOUTUBE_BASE}/watch?v={video_id}"
    video_path = None
    video_info = None

    ydl_opts = {
        'format': 'best[height<=360][ext=mp4]',
        'outtmpl': os.path.join(PUBLIC_FOLDER, '%(title)s.%(ext)s'),
        'quiet': True,
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(watch_url, download=True)
            video_title = info_dict.get('title', 'Unknown Title')
            video_description = info_dict.get('description', 'No description available.')
            video_path = os.path.join(PUBLIC_FOLDER, f"{video_title}.mp4")
            sanitized_name = video_title.translate(str.maketrans({"[": "(", "]": ")", "'": "", "_": "", "#": ""}))
    except Exception as e:
        return f"Error downloading video: {str(e)}", 500

    return f"""
    <html>
    <body>
    <h1>{video_title}</h1>
    <form action="/youtube">
    <input type="submit" value="Go back to Youtube"/>
    </form>
    <div>
    <center>
    <embed src="{sanitized_name}.mp4" width="720" height="480" scale="tofit" autoplay="false">
    <object data="{sanitized_name}.mp4" width="720" height="480"></object>
    </center>
    </div>
    <h2><u>Description</u></h2>
    <small>{video_description}</small>
    </body>
    </html>
    """

@app.errorhandler(404)
def not_found(e):
    param = request.full_path
    try:
        response = requests.get(f"{YOUTUBE_BASE}{param}")
        return Response(response.content, content_type=response.headers["Content-Type"])
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(port=4567, debug=True)
