import logging
from telegram.ext import Application
from dotenv import load_dotenv
import os
from bot.handlers import setup_handlers
from bot.states import EMAIL_VALIDATION, NEW_CUSTOMER, CUSTOMER_REGISTRATION, PAYMENT_METHOD, ORDER_CONFIRMATION

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL")
AGENT_CHAT_ID = os.getenv("AGENT_CHAT_ID")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

if not BOT_TOKEN:
    logger.error("Bot token not found. Check the .env file.")
else:
    logger.info(f"Bot token loaded: {BOT_TOKEN}")

if not API_BASE_URL:
    logger.error("API base URL not found. Check the .env file.")
else:
    logger.info(f"API base URL loaded: {API_BASE_URL}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    setup_handlers(application)
    application.run_polling()

if __name__ == "__main__":
    main()