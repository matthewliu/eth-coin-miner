# ETH Coin Miner

## Overview

This project is a simple script to mine ETHC (ethcoin.org) coins programmatically.

## To Dos

1. Use a python Web3 wallet library to load one or more Ethereum wallets from private keys. The app must be very secure. Private keys should never be stored in the readable code or on Github.
2. Use the Web3 library to connect to the ETHC Ethereum network.
3. Use the Web3 wallet library to interact with the EthCoin smart contracts.
4. Every EthCoin block (distinct from Ethereum blocks), the app should check the EthCoin smart contract to detect current mining power of the other miners.
5. If the collective mining power of other miners is a reasonable amount, the app should create a transaction to compete in this block to mine ETHC. This will be done by calculating the probability of winning the block based.
6. We will use the approximate price of ETHC from a DEX to determine the value of the block reward and net profitability.
7. The app should then monitor the pending transactions and mined transactions to detect if the app has won the block or not.
8. The app should then record the block number, transaction hash, and the amount of ETHC mined. This can be stored in a simple Postgres database.
9. Once every hour, the app should send a summary of the previous hour's earnings to the admin email address.