import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
DATABASE_URL = os.getenv('DATABASE_URL')

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
DEV_EMAIL = os.getenv('DEV_EMAIL')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
