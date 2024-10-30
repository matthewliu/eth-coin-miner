## To Dos

✅ 1. Use a python Web3 wallet library to load one or more Ethereum wallets from private keys.
   - Implemented in wallet_manager.py
   - Private keys stored securely in .env
   - ❌ Need to test wallet loading and transactions

✅ 2. Use the Web3 library to connect to the ETHC Ethereum network.
   - Implemented in alchemy_connector.py
   - Using Alchemy as provider
   - ❌ Need to test connection and basic Web3 calls

🔄 3. Use the Web3 wallet library to interact with the EthCoin smart contracts.
   - Contract ABI stored in config/abi/
   - Basic contract interactions implemented in ethc_miner.py
   - ❌ Need to test all contract functions:
     - Test read operations (view functions)
     - Test mining cost calculation
     - Test transaction building
     - Test basic mining operation

4. Every EthCoin block (distinct from Ethereum blocks), the app should check the EthCoin smart contract to detect current mining power of the other miners.
5. If the collective mining power of other miners is a reasonable amount, the app should create a transaction to compete in this block to mine ETHC. This will be done by calculating the probability of winning the block based.
6. We will use the approximate price of ETHC from a DEX to determine the value of the block reward and net profitability.
7. The app should then monitor the pending transactions and mined transactions to detect if the app has won the block or not.
8. The app should then record the block number, transaction hash, and the amount of ETHC mined. This can be stored in a simple Postgres database.
9. Once every hour, the app should send a summary of the previous hour's earnings to the admin email address.

## Style preferences

1. Do not use Python typed hints.
2. Add appropriate logging for error handling.
3. Bias towards classes and objects to ensure a clean and maintainable codebase.
4. Reference .env variables and constants in config to imports.
5. Reference /util files to import rather than write in-line code.
6. When importing libraries, import system libraries first, then third-party libraries, then custom code.

## Next Steps Priority (Updated)

1. Test basic contract interactions
   - Write test script for view functions
   - Test with small mining transaction
   - Verify ABI and contract addresses are correct

2. Implement block monitoring service
3. Add DEX price fetching
4. Create database schema and operations
5. Set up transaction monitoring
6. Implement email service
7. Add scheduled tasks

## Notes

- ✅ = Completed
- 🔄 = In Progress
- ❌ = Not Started
- Items marked complete but untested should be considered 🔄