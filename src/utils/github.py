from requests import get
from bs4 import BeautifulSoup
import time

USER_INFO_URL = "https://api.github.com/users/"
_status_cache = {}
CACHE_EXPIRY = 60  # seconds

_last_request_time = 0
MIN_INTERVAL = 2  # seconds between requests

def get_user_data(username: str):
    user_data = get(USER_INFO_URL + username)
    return user_data.json()

def get_status(username: str):
    global _last_request_time

    if username in _status_cache:
        cached_time, cached_status = _status_cache[username]
        if time.time() - cached_time < CACHE_EXPIRY:
            return cached_status

    now = time.time()
    if now - _last_request_time < MIN_INTERVAL:
        wait = MIN_INTERVAL - (now - _last_request_time)
        time.sleep(wait)

    url = f"https://github.com/{username}"
    r = get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    emoji_div = soup.select_one("div.user-status-emoji-container > div")
    message_div = soup.select_one("div.user-status-message-wrapper > div")

    emoji = emoji_div.text.strip() if emoji_div else ""
    message = message_div.text.strip() if message_div else ""

    status = f"{emoji} {message}".strip() if emoji or message else None

    _status_cache[username] = (time.time(), status)
    _last_request_time = time.time()

    return status