from web3 import Web3
from config import constants

# Connect to the Ethereum network
ALCHEMY_API_KEY = constants.ALCHEMY_API_KEY
w3 = Web3(Web3.HTTPProvider(f'https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}'))