import logging
from decimal import Decimal
from config.constants import ETHC_CONTRACT_ADDRESS, ETHC_CONTRACT_ABI
from util.alchemy_connector import w3
import asyncio

logger = logging.getLogger(__name__)

class ETHCMiner:
    def __init__(self, wallet_manager):
        """Initialize the ETHC miner with Web3 connection and contract"""
        logger.info("Initializing ETHCMiner...")
        self.web3 = w3
        self.wallet_manager = wallet_manager
        
        # Initialize contract using ABI from constants
        self.contract = self.web3.eth.contract(
            address=ETHC_CONTRACT_ADDRESS,
            abi=ETHC_CONTRACT_ABI
        )
        logger.info(f"Contract initialized at proxy address: {ETHC_CONTRACT_ADDRESS}")

    async def get_current_block(self):
        """Get current block and timing information from contract"""
        try:
            current_block = self.contract.functions.blockNumber().call()
            last_block_time = self.contract.functions.lastBlockTime().call()
            current_time = self.web3.eth.get_block('latest').timestamp
            
            # Block interval is constant (1 minute)
            block_interval = 60
            
            time_since_last = current_time - last_block_time
            blocks_ready = time_since_last // block_interval
            
            block_info = {
                'current_block': current_block,
                'next_block': current_block + 1,
                'last_block_time': last_block_time,
                'time_since_last': time_since_last,
                'blocks_ready': blocks_ready,
                'next_block_available': True
            }
            
            logger.debug(f"Block info: {block_info}")
            return block_info
        except Exception as e:
            logger.error(f"Error getting current block: {e}")
            raise

    async def get_mining_stats(self):
        """Get current mining statistics"""
        try:
            logger.info("Fetching mining stats...")
            # Get block info first
            block_info = await self.get_current_block()
            
            # Get costs and rewards from contract
            mine_cost = self.contract.functions.mineCost().call()
            mining_reward = self.contract.functions.miningReward().call()
            last_block_time = self.contract.functions.lastBlockTime().call()
            
            stats = {
                'current_block': block_info['current_block'],
                'block_interval': 60,  # 1 minute in seconds
                'mine_cost': self.web3.from_wei(mine_cost, 'ether'),
                'mining_reward': mining_reward,
                'last_block_time': last_block_time,
                'time_since_last': block_info['time_since_last'],
                'blocks_ready': block_info['blocks_ready']
            }
            logger.info(f"Mining stats retrieved: {stats}")
            return stats
        except Exception as e:
            logger.error(f"Error getting mining stats: {e}")
            raise

    async def get_block_miners(self, block_number):
        """Get miners for a specific block"""
        try:
            miners = self.contract.functions.minersOfBlock(block_number).call()
            miner_count = self.contract.functions.minersOfBlockCount(block_number).call()
            
            # Use selectedMinerOfBlock function
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
            # Get current block info (but don't wait)
            block_info = await self.get_current_block()
            
            # Get contract state before mining
            logger.info("\nChecking contract state:")
            logger.info(f"- Block number from contract: {self.contract.functions.blockNumber().call()}")
            logger.info(f"- Last block time: {self.contract.functions.lastBlockTime().call()}")
            logger.info(f"- Current chain time: {self.web3.eth.get_block('latest').timestamp}")
            logger.info(f"- Time since last block: {block_info['time_since_last']}s")
            
            # Get mining cost from contract
            mine_cost = self.contract.functions.mineCost().call()
            logger.info(f"- Mining cost from contract: {self.web3.from_wei(mine_cost, 'ether')} ETH")
            
            wallet = self.wallet_manager.get_wallet_by_name(wallet_name)
            
            # Calculate total cost including gas
            total_mine_cost = mine_cost * mine_count
            gas_limit = self.contract.functions.mine(mine_count).estimate_gas({
                'from': wallet.public_key, 
                'value': total_mine_cost
            })
            gas_limit = int(gas_limit * 1.2)  # Add 20% buffer
            
            # Get current gas prices
            base_fee = self.web3.eth.get_block('latest').baseFeePerGas
            priority_fee = self.web3.eth.max_priority_fee
            max_fee_per_gas = base_fee * 2 + priority_fee  # Double the base fee for buffer
            
            max_gas_cost = gas_limit * max_fee_per_gas
            total_cost = total_mine_cost + max_gas_cost
            
            logger.info("Cost breakdown:")
            logger.info(f"- Mining cost: {self.web3.from_wei(total_mine_cost, 'ether')} ETH")
            logger.info(f"- Max gas cost: {self.web3.from_wei(max_gas_cost, 'ether')} ETH")
            logger.info(f"- Total needed: {self.web3.from_wei(total_cost, 'ether')} ETH")
            
            # Check wallet balance
            balance = self.web3.eth.get_balance(wallet.public_key)
            logger.info(f"- Wallet balance: {self.web3.from_wei(balance, 'ether')} ETH")
            
            if balance < total_cost:
                raise ValueError("Insufficient funds for mining")
                
            # Build transaction
            nonce = self.web3.eth.get_transaction_count(wallet.public_key, 'latest')
            
            transaction = {
                'from': wallet.public_key,
                'value': total_mine_cost,
                'nonce': nonce,
                'gas': gas_limit,
                'maxFeePerGas': max_fee_per_gas,
                'maxPriorityFeePerGas': priority_fee,
                'type': 2,  # EIP-1559 transaction
                'chainId': self.web3.eth.chain_id
            }
            
            # Build and sign transaction
            tx = self.contract.functions.mine(mine_count).build_transaction(transaction)
            signed_tx = self.web3.eth.account.sign_transaction(tx, wallet.private_key)
            
            # Send transaction
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            return tx_hash
            
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
            # Always get fresh block number
            current_block = await self.get_current_block()
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

    async def wait_for_next_block(self):
        """Wait until the next block is available for mining"""
        max_attempts = 5  # Prevent infinite waiting
        attempt = 0
        
        while attempt < max_attempts:
            try:
                block_info = await self.get_current_block()
                logger.info(f"Current block: {block_info['current_block']}, Time since last: {block_info['time_since_last']}s")
                
                if block_info['next_block_available']:
                    logger.info(f"Block {block_info['current_block']} is ready for mining")
                    return block_info
                
                time_to_wait = min(60 - block_info['time_since_last'], 10)  # Wait max 10 seconds at a time
                logger.info(f"Waiting {time_to_wait} seconds before next check...")
                await asyncio.sleep(time_to_wait)
                attempt += 1
                
            except Exception as e:
                logger.error(f"Error while waiting for next block: {e}")
                raise
        
        raise TimeoutError("Max attempts reached waiting for next block")

    async def has_mined_block(self, wallet_address, block_number):
        """Check if the wallet has already mined this block"""
        try:
            miners = await self.get_block_miners(block_number)
            return wallet_address in miners['miners']
        except Exception as e:
            logger.error(f"Error checking if wallet has mined block: {e}")
            raise