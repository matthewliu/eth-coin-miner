import os
import json
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST')
DATABASE_URL = os.getenv('DATABASE_URL')

ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY')

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
DEV_EMAIL = os.getenv('DEV_EMAIL')

# Load all wallet configurations from environment
WALLETS = {}
for key, value in os.environ.items():
    if key.startswith('WALLET_'):
        try:
            WALLET_CONFIGS[key] = json.loads(value)
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {key}")