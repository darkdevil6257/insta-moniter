import requests
import cloudscraper

BOT_TOKEN = "7983931203:AAE9B5Blt6QFNLyzto-m-NA4rxzhZAnySU8"
CHAT_ID = "8626017722"

scraper = cloudscraper.create_scraper()


def send_telegram(message):

    try:

        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={
                "chat_id": CHAT_ID,
                "text": message
            },
            timeout=20
        )

    except Exception as e:

        print("Telegram Error:", e)


def check_instagram(username):

    try:

        url = f"https://www.instagram.com/{username}/"

        response = scraper.get(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0 Safari/537.36"
                )
            },
            timeout=30
        )

        html = response.text.lower()

        print(f"{username} => {response.status_code}")

        if response.status_code == 404:

            return "banned"

        if (
            "sorry, this page isn't available" in html
            or "the link you followed may be broken" in html
            or "page isn't available" in html
        ):

            return "banned"

        return "active"

    except Exception as e:

        print("Instagram Error:", e)

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
            f"🚨 INSTAGRAM ID BANNED\n\n@{username}"
        )
