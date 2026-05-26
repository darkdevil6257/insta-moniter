import requests
import cloudscraper
import json
import os

BOT_TOKEN = "7983931203:AAE9B5Blt6QFNLyzto-m-NA4rxzhZAnySU8"
CHAT_ID = "8626017722"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

scraper = cloudscraper.create_scraper()

STATUS_FILE = "status.json"

def send_telegram(msg):

    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

def check_instagram(username):

    try:

        r = scraper.get(
            f"https://www.instagram.com/{username}/",
            headers=HEADERS,
            timeout=30
        )

        html = r.text.lower()

        if r.status_code == 200:

            if "sorry, this page isn't available" in html:
                return "banned"

            return "active"

        if r.status_code == 404:
            return "banned"

        return "unknown"

    except:
        return "error"

def load_status():

    if os.path.exists(STATUS_FILE):

        with open(STATUS_FILE, "r") as f:
            return json.load(f)

    return {}

def save_status(data):

    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)

with open("usernames.txt", "r") as f:

    usernames = [
        x.strip()
        for x in f.readlines()
        if x.strip()
    ]

old_status = load_status()

new_status = {}

for username in usernames:

    status = check_instagram(username)

    new_status[username] = status

    old = old_status.get(username)

    print(username, status)

    if old == "active" and status == "banned":

        send_telegram(
            f"🚨 ID BANNED\n\n@{username}"
        )

    if old == "banned" and status == "active":

        send_telegram(
            f"✅ ID RETURNED\n\n@{username}"
        )

save_status(new_status)
send_telegram("tTEST OK")
