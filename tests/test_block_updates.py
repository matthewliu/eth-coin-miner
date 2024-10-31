import asyncio
import logging
import time
from logic.ethc_miner import ETHCMiner
from util.wallet_manager import WalletManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_block_updates():
    """Test if block number updates correctly"""
    wallet_manager = WalletManager()
    miner = ETHCMiner(wallet_manager)
    
    try:
        # Check block number multiple times
        for i in range(3):
            block = await miner.get_current_block()
            logger.info(f"Current block: {block}")
            await asyncio.sleep(10)  # Wait 10 seconds between checks
            
    except Exception as e:
        logger.error(f"Error during testing: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_block_updates())