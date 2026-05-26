import requests
import cloudscraper
import json
import os

BOT_TOKEN = "7983931203:AAE9B5Blt6QFNLyzto-m-NA4rxzhZAnySU8"
CHAT_ID = "8626017722"

scraper = cloudscraper.create_scraper()

STATUS_FILE = "status.json"


def send_telegram(message):

    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


def check_instagram(username):

    try:

        url = f"https://www.instagram.com/{username}/"

        r = scraper.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=30
        )

        html = r.text.lower()

        if (
            "sorry, this page isn't available" in html
            or "page isn't available" in html
            or "the link you followed may be broken" in html
            or '"user":null' in html
            or f'"username":"{username.lower()}"' not in html
        ):

            return "banned"

        return "active"

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

    print(username, status)

    new_status[username] = status

    old = old_status.get(username)

    if old == "active" and status == "banned":

        send_telegram(
            f"🚨 ID BANNED\n\n@{username}"
        )

    elif old is None:

        print(f"First check: {username} => {status}")


save_status(new_status)
