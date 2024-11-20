import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")

def get_updates():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    updates = get_updates()
    print(updates)