import asyncio
import logging
from decimal import Decimal

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

async def test_batch_mine():
    """Test mining multiple times in a single block"""
    try:
        wallet_manager = WalletManager()
        miner = ETHCMiner(wallet_manager)
        
        # Get current block info
        block_info = await miner.get_current_block()
        
        # Get current miners and estimate probability
        miners = await miner.get_block_miners(block_info['current_block'])
        logger.info(f"Current miners: {miners['miner_count']}")
        
        # Calculate optimal mine count based on current miners
        miner_count = miners['miner_count']
        mine_count = min(50, max(10, miner_count // 3))  # Dynamic mine count
        
        # Calculate base probability
        base_probability = await miner.estimate_mining_probability(block_info['current_block'])
        
        # Calculate cumulative probability with multiple attempts
        cumulative_prob = 1 - (1 - base_probability) ** mine_count
        logger.info(f"Base win probability: {base_probability:.1%}")
        logger.info(f"Mining {mine_count} times for cumulative probability: {cumulative_prob:.1%}")
        
        # Get mining costs
        mine_cost = miner.contract.functions.mineCost().call()
        total_mine_cost = mine_cost * mine_count
        logger.info(f"Total mining cost: {miner.web3.from_wei(total_mine_cost, 'ether')} ETH")
        
        # Calculate mining reward for profitability check
        mining_reward = miner.contract.functions.miningReward().call()
        logger.info(f"Potential block reward: {miner.web3.from_wei(mining_reward, 'ether')} ETH")
        
        # Expected value calculation
        expected_value = (Decimal(mining_reward) * Decimal(cumulative_prob)) - Decimal(total_mine_cost)
        logger.info(f"Expected value: {miner.web3.from_wei(int(expected_value), 'ether')} ETH")
        
        if expected_value <= 0:
            logger.warning("⚠️ Warning: Expected value is negative, mining may not be profitable")
            return None
        
        # Attempt batch mining with higher gas limit for larger batch
        logger.info(f"\nAttempting to mine {mine_count} times with Wallet 1...")
        tx_hash = await miner.mine("Wallet 1", mine_count=mine_count)
        
        # Wait for confirmation
        logger.info("\nWaiting for transaction confirmation...")
        tx_receipt = miner.web3.eth.wait_for_transaction_receipt(tx_hash)
        
        if tx_receipt.status == 1:
            logger.info(f"Batch mining transaction confirmed!")
            logger.info(f"Gas used: {tx_receipt.gasUsed}")
            logger.info(f"Transaction hash: {tx_receipt.transactionHash.hex()}")
            
            # Check if we won the block
            next_block = block_info['current_block'] + 1
            await asyncio.sleep(65)  # Wait for next block to be mined
            
            winner = miner.contract.functions.selectedMinerOfBlock(next_block).call()
            our_wallet = wallet_manager.get_wallet_by_name("Wallet 1")
            
            if winner.lower() == our_wallet.public_key.lower():
                logger.info("🎉 We won the block!")
                logger.info(f"Block reward: {miner.web3.from_wei(mining_reward, 'ether')} ETH")
                profit = mining_reward - total_mine_cost - (tx_receipt.gasUsed * tx_receipt.effectiveGasPrice)
                logger.info(f"Net profit: {miner.web3.from_wei(profit, 'ether')} ETH")
            else:
                logger.info("We did not win this block")
                loss = total_mine_cost + (tx_receipt.gasUsed * tx_receipt.effectiveGasPrice)
                logger.info(f"Net loss: {miner.web3.from_wei(loss, 'ether')} ETH")
                
        else:
            logger.error("Mining transaction failed!")
            logger.error(f"Transaction hash: {tx_receipt.transactionHash.hex()}")
            
        return tx_receipt
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(test_batch_mine())
