import logging
from eth_account import Account
from config.constants import WALLETS
from util.alchemy_connector import w3

logger = logging.getLogger(__name__)

class Transaction:
    def __init__(self, to_address, value_in_wei, gas_limit=21000, data='0x', chain_id=1):
        self.to_address = to_address
        self.value_in_wei = value_in_wei
        self.gas_limit = gas_limit
        self.data = data
        self.chain_id = chain_id

    def to_dict(self, web3, from_address):
        """Convert transaction to dictionary format required by web3"""
        return {
            'nonce': web3.eth.get_transaction_count(from_address),
            'gasPrice': web3.eth.gas_price,
            'gas': self.gas_limit,
            'to': self.to_address,
            'value': self.value_in_wei,
            'data': self.data,
            'chainId': self.chain_id
        }

    def __str__(self):
        return f"Transaction(to={self.to_address}, value={self.value_in_wei} wei)"

class Wallet:
    def __init__(self, name, public_key, private_key):
        self.name = name
        # Convert public key to checksum address
        self.public_key = w3.to_checksum_address(public_key)
        self.private_key = private_key

    def __str__(self):
        return f"Wallet(name={self.name}, address={self.public_key})"

class WalletManager:
    # Singleton instance
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info("Initializing new WalletManager instance")
            cls._instance = super(WalletManager, cls).__new__(cls)
            cls._instance.wallets = []
            cls._instance.web3 = w3
            cls._instance._load_wallets()
        else:
            logger.debug("Using existing WalletManager instance")
        return cls._instance

    def _load_wallets(self):
        logger.info("Loading wallets from config")
        for wallet_data in WALLETS.values():
            try:
                wallet = Wallet(
                    name=wallet_data['name'],
                    public_key=wallet_data['public_key'],
                    private_key=wallet_data['private_key']
                )
                self.wallets.append(wallet)
                logger.info(f"Loaded wallet: {wallet.name} ({wallet.public_key})")
            except KeyError as e:
                logger.error(f"Error loading wallet: Missing required field {e}")

    def get_wallet_by_name(self, name):
        for wallet in self.wallets:
            if wallet.name.lower() == name.lower():
                logger.debug(f"Found wallet: {wallet}")
                return wallet
        logger.warning(f"No wallet found with name: {name}")
        raise ValueError(f"No wallet found with name: {name}")

    def get_wallet_by_address(self, address):
        for wallet in self.wallets:
            if wallet.public_key.lower() == address.lower():
                logger.debug(f"Found wallet: {wallet}")
                return wallet
        logger.warning(f"No wallet found with address: {address}")
        raise ValueError(f"No wallet found with address: {address}")

    def sign_transaction(self, wallet_name, transaction):
        """Sign a transaction using the specified wallet's private key"""
        logger.info(f"Signing transaction with wallet: {wallet_name}")
        wallet = self.get_wallet_by_name(wallet_name)
        account = Account.from_key(wallet.private_key)
        
        # Convert Transaction object to dictionary format
        transaction_dict = transaction.to_dict(self.web3, wallet.public_key)
        
        signed_txn = account.sign_transaction(transaction_dict)
        logger.info(f"Transaction signed successfully")
        return signed_txn.rawTransaction

    def get_all_addresses(self):
        addresses = [wallet.public_key for wallet in self.wallets]
        logger.debug(f"Retrieved {len(addresses)} wallet addresses")
        return addresses

    def get_wallet_names(self):
        names = [wallet.name for wallet in self.wallets]
        logger.debug(f"Retrieved {len(names)} wallet names")
        return names

    def __len__(self):
        return len(self.wallets)

    def __str__(self):
        return f"WalletManager(wallets={len(self.wallets)})"
