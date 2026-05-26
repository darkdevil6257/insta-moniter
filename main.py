import requests
import cloudscraper

BOT_TOKEN = "7983931203:AAE9B5Blt6QFNLyzto-m-NA4rxzhZAnySU8
"
CHAT_ID = "8626017722"

USERNAME = "minakshi_official11"

scraper = cloudscraper.create_scraper()

def send_telegram(msg):

    requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        params={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )

try:

    url = f"https://www.instagram.com/{USERNAME}/"

    r = scraper.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    html = r.text.lower()

    message = (
        f"USERNAME: {USERNAME}\n"
        f"STATUS CODE: {r.status_code}\n"
    )

    if r.status_code == 200:

        if "sorry, this page isn't available" in html:

            message += "RESULT: BANNED"

        else:

            message += "RESULT: ACTIVE"

    elif r.status_code == 404:

        message += "RESULT: BANNED"

    else:

        message += "RESULT: UNKNOWN"

    print(message)

    send_telegram(message)

except Exception as e:

    send_telegram(f"ERROR: {str(e)}")
