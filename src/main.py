from flask import Flask, render_template, request
from utils.github import get_user_data, get_status
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo
from os import getenv

app = Flask(__name__)
load_dotenv()

GITHUB_USERNAME = getenv("GITHUB_USERNAME")

@app.route("/")
def main():
    return render_template(
        "index.html", 
        avatar_url=get_user_data(GITHUB_USERNAME or "ha-rt")["avatar_url"],
        username=GITHUB_USERNAME or "ha-rt",
        status=get_status(GITHUB_USERNAME or "ha-rt")
    )

@app.route("/projects")
def projects():
    if request.headers.get("HX-Request"):
        return render_template(
            "components/projects.html", 
            avatar_url=get_user_data(GITHUB_USERNAME or "ha-rt")["avatar_url"],
            username=GITHUB_USERNAME or "ha-rt",
            status=get_status(GITHUB_USERNAME or "ha-rt")
        )
    else:
        return render_template(
                "projects.html",
                page="projects",
                avatar_url=get_user_data(GITHUB_USERNAME or "ha-rt")["avatar_url"],
                username=GITHUB_USERNAME or "ha-rt",
                status=get_status(GITHUB_USERNAME or "ha-rt")
            ) 

@app.route("/api/time")
def current_time():
    return datetime.now(tz=ZoneInfo("America/Los_Angeles")).strftime("%H:%M")

if __name__ == "__main__":
    app.run()