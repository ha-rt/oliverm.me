from flask import Flask, render_template
from utils.github import get_user_data, get_status
from dotenv import load_dotenv
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

if __name__ == "__main__":
    app.run(debug=True)