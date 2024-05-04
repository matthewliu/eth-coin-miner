import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
DATABASE_URL = os.getenv('DATABASE_URL')

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
DEV_EMAIL = os.getenv('DEV_EMAIL')