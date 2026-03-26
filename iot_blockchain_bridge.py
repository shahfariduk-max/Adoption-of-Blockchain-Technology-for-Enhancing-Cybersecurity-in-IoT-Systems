import pandas as pd
from web3 import Web3
import json

# 1. CONNECT TO GANACHE
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if not web3.is_connected():
    print("Failed to connect to Ganache!")
    exit()

# 2. CONTRACT CONFIGURATION (Based on your deployment)
contract_address = "0x3a0eff57be10988576e20190a9dc56ab09660722"
admin_wallet = "0x592d290385A1BBeaF90789B596EB5F9b4a8FD710"

# Minimal ABI for the functions we need
abi = json.loads('[{"inputs":[{"internalType":"address","name":"_device","type":"address"},{"internalType":"string","name":"_deviceType","type":"string"}],"name":"registerDevice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_device","type":"address"},{"internalType":"string","name":"_data","type":"string"}],"name":"validateTraffic","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

contract = web3.eth.contract(address=contract_address, abi=abi)

# 3. LOAD YOUR DATASET
# Replace with the actual path to your BoT-IoT CSV file
dataset_path = "path_to_your_bot_iot_dataset.csv" 

def run_simulation():
    # Example: Simulating one device registration
    test_device = web3.eth.accounts[1] # Using the second Ganache account as an IoT device
    
    print(f"Registering Device: {test_device}...")
    tx_hash = contract.functions.registerDevice(test_device, "SmartMeter").transact({'from': admin_wallet})
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print("Device registered successfully.")

    # Simulating data flow from your dataset
    # Here we send a "Traffic Log" to the blockchain
    print("Sending traffic data to blockchain for validation...")
    tx_hash = contract.functions.validateTraffic(test_device, "Normal Traffic Flow").transact({'from': admin_wallet})
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    print(f"Transaction Hash: {receipt.transactionHash.hex()}")
    print("Simulation Complete. Check Remix or Ganache logs for events.")

if __name__ == "__main__":
    run_simulation()