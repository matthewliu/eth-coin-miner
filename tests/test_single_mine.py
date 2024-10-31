import asyncio
import logging

from logic.ethc_miner import ETHCMiner
from util.wallet_manager import WalletManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# Disable noisy logging
logging.getLogger("web3").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def test_single_mine():
    """Test mining a single block with detailed logging"""
    try:
        wallet_manager = WalletManager()
        miner = ETHCMiner(wallet_manager)
        
        # Get current block info
        block_info = await miner.get_current_block()
        
        # Get current miners and estimate probability
        miners = await miner.get_block_miners(block_info['current_block'])
        logger.info(f"Current miners: {miners['miner_count']}")
        
        # Calculate probability
        probability = await miner.estimate_mining_probability(block_info['current_block'])
        logger.info(f"Estimated win probability: {probability:.1%}")
        
        # Attempt to mine
        logger.info("\nAttempting to mine with Wallet 1...")
        tx_hash = await miner.mine("Wallet 1", mine_count=1)
        
        # Wait for confirmation
        logger.info("\nWaiting for transaction confirmation...")
        # Use synchronous wait_for_transaction_receipt
        tx_receipt = miner.web3.eth.wait_for_transaction_receipt(tx_hash)
        
        if tx_receipt.status == 1:
            logger.info(f"Mining transaction confirmed! Gas used: {tx_receipt.gasUsed}")
            logger.info(f"Transaction hash: {tx_receipt.transactionHash.hex()}")
        else:
            logger.error("Mining transaction failed!")
            logger.error(f"Transaction hash: {tx_receipt.transactionHash.hex()}")
            
        return tx_receipt
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_single_mine())
