from requests import get, exceptions
from bs4 import BeautifulSoup
import time
import sys
from typing import List, Dict, Optional, Any

USER_INFO_URL = "https://api.github.com/users/"
_status_cache = {}
_repo_cache: Dict[str, tuple[float, List[Dict[str, Any]]]] = {}
CACHE_EXPIRY = 60

_last_request_time = 0
MIN_INTERVAL = 2

def get_user_data(username: str):
    user_data = get(USER_INFO_URL + username)
    return user_data.json()

def get_user_repos(username: str) -> Optional[List[Dict[str, Any]]]:
    global _last_request_time

    if username in _repo_cache:
        cached_time, cached_repos = _repo_cache[username]
        if time.time() - cached_time < CACHE_EXPIRY:
            print(f"[{username}] Returning cached repository data.", file=sys.stderr)
            return cached_repos

    now = time.time()
    if now - _last_request_time < MIN_INTERVAL:
        wait = MIN_INTERVAL - (now - _last_request_time)
        print(f"[{username}] Waiting {wait:.2f} seconds before next API request...", file=sys.stderr)
        time.sleep(wait)

    api_url = f"{USER_INFO_URL}{username}/repos"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    print(f"[{username}] Making API request to: {api_url}", file=sys.stderr)
    try:
        response = get(api_url, headers=headers)
        response.raise_for_status()

        repos_data = response.json()

        _repo_cache[username] = (time.time(), repos_data)
        _last_request_time = time.time()

        return repos_data
    except exceptions.RequestException as e:
        print(f"Error fetching repositories for '{username}': {e}", file=sys.stderr)
        return None

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