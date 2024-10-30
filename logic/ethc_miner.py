import logging
from decimal import Decimal
from config.constants import ETHC_MINER_CONTRACT_ADDRESS, ETHC_MINER_CONTRACT_ABI
from util.alchemy_connector import w3

logger = logging.getLogger(__name__)

class ETHCMiner:
    def __init__(self, wallet_manager):
        """Initialize the ETHC miner with Web3 connection and contract"""
        self.web3 = w3  # Use existing Alchemy connection
        self.wallet_manager = wallet_manager
        
        # Initialize contract using ABI from constants
        self.contract = self.web3.eth.contract(
            address=ETHC_MINER_CONTRACT_ADDRESS,
            abi=ETHC_MINER_CONTRACT_ABI
        )

    async def get_mining_stats(self):
        """Get current mining statistics"""
        try:
            current_block = self.contract.functions.blockNumber().call()
            block_interval = self.contract.functions.BLOCK_INTERVAL().call()
            mine_cost = self.contract.functions.MINE_COST().call()
            mining_reward = self.contract.functions.miningReward().call()
            last_block_time = self.contract.functions.lastBlockTime().call()
            
            return {
                'current_block': current_block,
                'block_interval': block_interval,
                'mine_cost': self.web3.from_wei(mine_cost, 'ether'),
                'mining_reward': mining_reward,
                'last_block_time': last_block_time
            }
        except Exception as e:
            logger.error(f"Error getting mining stats: {e}")
            raise

    async def get_block_miners(self, block_number):
        """Get miners for a specific block"""
        try:
            miners = self.contract.functions.minersOfBlock(block_number).call()
            miner_count = self.contract.functions.minersOfBlockCount(block_number).call()
            selected_miner = self.contract.functions.selectedMinerOfBlock(block_number).call()
            
            return {
                'miners': miners,
                'miner_count': miner_count,
                'selected_miner': selected_miner
            }
        except Exception as e:
            logger.error(f"Error getting block miners: {e}")
            raise

    async def mine(self, wallet_name, mine_count=1):
        """Submit a mining transaction"""
        try:
            wallet = self.wallet_manager.get_wallet_by_name(wallet_name)
            mine_cost = self.contract.functions.MINE_COST().call()
            total_cost = mine_cost * mine_count
            
            # Build transaction
            if mine_count == 1:
                tx = self.contract.functions.mine().build_transaction({
                    'from': wallet.public_key,
                    'value': total_cost,
                    'nonce': self.web3.eth.get_transaction_count(wallet.public_key),
                    'gasPrice': self.web3.eth.gas_price
                })
            else:
                tx = self.contract.functions.mineBatch(mine_count).build_transaction({
                    'from': wallet.public_key,
                    'value': total_cost,
                    'nonce': self.web3.eth.get_transaction_count(wallet.public_key),
                    'gasPrice': self.web3.eth.gas_price
                })

            # Sign and send transaction
            signed_tx = self.wallet_manager.sign_transaction(wallet_name, tx)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx)
            
            logger.info(f"Mining transaction submitted: {tx_hash.hex()}")
            return tx_hash.hex()
            
        except Exception as e:
            logger.error(f"Error submitting mining transaction: {e}")
            raise

    async def estimate_mining_probability(self, block_number):
        """Estimate probability of winning a block based on current miners"""
        try:
            miner_count = self.contract.functions.minersOfBlockCount(block_number).call()
            if miner_count == 0:
                return 1.0  # 100% chance if no other miners
            return Decimal(1) / Decimal(miner_count + 1)  # +1 to include our potential mine
        except Exception as e:
            logger.error(f"Error estimating mining probability: {e}")
            raise

    async def get_halving_info(self):
        """Get information about halving schedule"""
        try:
            current_block = self.contract.functions.blockNumber().call()
            last_halving = self.contract.functions.lastHalvingBlock().call()
            next_halving = self.contract.functions.nextHalvingBlock().call()
            halving_interval = self.contract.functions.halvingInterval().call()
            
            return {
                'current_block': current_block,
                'last_halving_block': last_halving,
                'next_halving_block': next_halving,
                'halving_interval': halving_interval
            }
        except Exception as e:
            logger.error(f"Error getting halving info: {e}")
            raise

    def subscribe_to_events(self, event_handler):
        """Subscribe to mining-related events"""
        try:
            # Subscribe to Mine events
            mine_event_filter = self.contract.events.Mine.create_filter(fromBlock='latest')
            # Subscribe to NewBlock events
            new_block_filter = self.contract.events.NewBlock.create_filter(fromBlock='latest')
            
            def handle_event(event):
                event_handler(event)
            
            return {
                'mine_filter': mine_event_filter,
                'block_filter': new_block_filter,
                'handler': handle_event
            }
        except Exception as e:
            logger.error(f"Error subscribing to events: {e}")
            raise