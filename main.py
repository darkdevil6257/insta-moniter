import requests

BOT_TOKEN = "7983931203:AAE9B5Blt6QFNLyzto-m-NA4rxzhZAnySU8"
CHAT_ID = "8626017722"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
    )
}


def send_telegram(message):

    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=20
    )


def check_username(username):

    try:

        url = f"https://www.instagram.com/{username}/"

        r = requests.get(
            url,
            headers=HEADERS,
            timeout=20,
            allow_redirects=True
        )

        html = r.text.lower()

        print(username, r.status_code)

        # ACCOUNT EXISTS
        if (
            r.status_code == 200
            and username.lower() in html
        ):

            return "active"

        # ACCOUNT NOT FOUND
        if (
            r.status_code == 404
            or "sorry, this page isn't available" in html
            or "page isn't available" in html
        ):

            return "banned"

        return "unknown"

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

    status = check_username(username)

    print(username, status)

    if status == "banned":

        send_telegram(
            f"🚨 ID BANNED\n\n@{username}"
        )
