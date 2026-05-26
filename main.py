import requests
import cloudscraper

BOT_TOKEN = "7983931203:AAE9B5Blt6QFNLyzto-m-NA4rxzhZAnySU8"
CHAT_ID = "8626017722"

scraper = cloudscraper.create_scraper()


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

        print(f"{username} => {r.status_code}")

        if (
            "sorry, this page isn't available" in html
            or "page isn't available" in html
            or "the link you followed may be broken" in html
            or '"user":null' in html
            or f'"username":"{username.lower()}"' not in html
        ):

            return "banned"

        return "active"

    except Exception as e:

        print(e)

        return "error"


with open("usernames.txt", "r") as f:

    usernames = [
        x.strip()
        for x in f.readlines()
        if x.strip()
    ]


for username in usernames:

    status = check_instagram(username)

    print(f"{username} => {status}")

    if status == "banned":

        send_telegram(
            f"🚨 ID BANNED\n\n@{username}"
        )

    elif status == "active":

        send_telegram(
            f"✅ ACTIVE\n\n@{username}"
        )

    else:

        send_telegram(
            f"⚠️ ERROR\n\n@{username}"
        )
