import json
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

HOST = os.getenv('HOST')
DATABASE_URL = os.getenv('DATABASE_URL')

ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY')

# Load all wallet configurations from environment
WALLETS = {}
for key, value in os.environ.items():
    if key.startswith('WALLET_'):
        try:
            WALLETS[key] = json.loads(value)
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in {key}")

ETHC_ERC_20_CONTRACT_ADDRESS=os.getenv('ETHC_ERC_20_CONTRACT_ADDRESS')
ETHC_MINER_CONTRACT_ADDRESS=os.getenv('ETHC_MINER_CONTRACT_ADDRESS')

# Load ABI from JSON file
abi_path = Path(__file__).parent / 'abi' / 'ethc_miner_contract.json'
with open(abi_path) as f:
    ETHC_MINER_CONTRACT_ABI = json.load(f)['abi']

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
DEV_EMAIL = os.getenv('DEV_EMAIL')