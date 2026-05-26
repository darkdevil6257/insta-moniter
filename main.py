import requests

BOT_TOKEN = "7983931203:AAE9B5Blt6QFNLyzto-m-NA4rxzhZAnySU8"
CHAT_ID = "8626017722"

HEADERS = {
    "User-Agent": "Instagram 219.0.0.12.117 Android"
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

        url = (
            "https://i.instagram.com/api/v1/"
            f"users/web_profile_info/?username={username}"
        )

        r = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        )

        text = r.text.lower()

        print(username)
        print(text[:200])

        # USER EXISTS
        if '"user":{' in text:

            return "active"

        # USER NOT FOUND / BANNED
        if '"user":null' in text:

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
            f"🚨 INSTAGRAM ID BANNED\n\n@{username}"
        )
