import asyncio
import logging

from util.wallet_manager import WalletManager
from logic.ethc_miner import ETHCMiner
from util.alchemy_connector import w3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_basic_setup():
    """Test basic wallet loading and contract reading"""
    try:
        # Test Alchemy connection
        logger.info("Testing Alchemy connection...")
        connected = w3.is_connected()
        logger.info(f"Connected to Ethereum network: {connected}")
        
        # Test wallet loading
        logger.info("\nTesting wallet loading...")
        wallet_manager = WalletManager()
        wallets = wallet_manager.wallets
        for wallet in wallets:
            logger.info(f"Loaded wallet: {wallet}")
            balance = w3.eth.get_balance(wallet.public_key)
            logger.info(f"Wallet balance: {w3.from_wei(balance, 'ether')} ETH")

        # Test contract reading
        logger.info("\nTesting contract reading...")
        miner = ETHCMiner(wallet_manager)
        
        # Get mining stats
        stats = await miner.get_mining_stats()
        logger.info(f"Mining stats: {stats}")
        
        # Get current block info
        current_block = stats['current_block']
        logger.info(f"\nGetting miners for block {current_block}")
        block_info = await miner.get_block_miners(current_block)
        logger.info(f"Block miners: {block_info}")
        
        # Get halving info
        halving_info = await miner.get_halving_info()
        logger.info(f"\nHalving info: {halving_info}")
        
        # Calculate mining probability
        probability = await miner.estimate_mining_probability(current_block)
        logger.info(f"\nMining probability for current block: {probability}")

    except Exception as e:
        logger.error(f"Error during testing: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_basic_setup())
