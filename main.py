import time
import requests
import cloudscraper
from datetime import datetime

# =========================
# TELEGRAM CONFIG
# =========================

BOT_TOKEN = "7983931203:AAE9B5Blt6QFNLyzto-m-NA4rxzhZAnySU8"
CHAT_ID = "8626017722"

# =========================
# SETTINGS
# =========================

CHECK_INTERVAL = 300
REQUEST_DELAY = 8

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X)"
    )
}

scraper = cloudscraper.create_scraper()

known_status = {}

# =========================
# TELEGRAM ALERT
# =========================

def send_telegram(message):

    try:

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        requests.get(
            url,
            params={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=30
        )

    except Exception as e:

        print("Telegram Error:", e)

# =========================
# CHECK INSTAGRAM
# =========================

def check_instagram(username):

    try:

        url = f"https://www.instagram.com/{username}/"

        r = scraper.get(
            url,
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

        if r.status_code == 429:
            return "rate_limited"

        return "unknown"

    except Exception as e:

        print(username, e)

        return "error"

# =========================
# LOAD USERNAMES
# =========================

def load_usernames():

    with open("usernames.txt", "r", encoding="utf-8") as f:

        return [
            line.strip()
            for line in f.readlines()
            if line.strip()
        ]

# =========================
# START
# =========================

send_telegram("✅ Instagram monitor started")

# =========================
# LOOP
# =========================

while True:

    print("\n====================")
    print("CHECK:", datetime.now())
    print("====================")

    usernames = load_usernames()

    for username in usernames:

        status = check_instagram(username)

        old_status = known_status.get(username)

        print(username, "=>", status)

        if old_status is None:

            known_status[username] = status

        else:

            if old_status == "active" and status == "banned":

                send_telegram(
                    f"🚨 ID BANNED\n\n@{username}"
                )

            if old_status == "banned" and status == "active":

                send_telegram(
                    f"✅ ID RETURNED\n\n@{username}"
                )

            known_status[username] = status

        time.sleep(REQUEST_DELAY)

    time.sleep(CHECK_INTERVAL)
