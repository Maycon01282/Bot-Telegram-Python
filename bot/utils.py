import os
from dotenv import load_dotenv
import requests
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
AGENT_CHAT_ID = os.getenv("AGENT_CHAT_ID")

logger = logging.getLogger(__name__)

def fetch_data(endpoint):
    url = f"{API_BASE_URL}/{endpoint}"
    headers = {
        'Authorization': f'Token {BOT_TOKEN}'
    }
    logger.info(f"Fetching data from {url}")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Data fetched: {data}")
        return data
    except requests.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        return None

def generate_keyboard(buttons):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, callback_data=data)] for text, data in buttons])

def calculate_total_value(cart):
    total = 0
    for prod_id in cart:
        product = fetch_data(f'products/{prod_id}/')
        if product:
            total += product['price']
    return total