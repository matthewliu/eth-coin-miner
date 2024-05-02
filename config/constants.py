import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
DEV_EMAIL = os.getenv('DEV_EMAIL')
TO_EMAILS = os.getenv('TO_EMAILS')