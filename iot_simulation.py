import pandas as pd
from web3 import Web3
import json

# 1. Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# 2. Paste your data from Remix here
CONTRACT_ADDRESS = "PASTE_YOUR_COPIED_ADDRESS_HERE"
CONTRACT_ABI = json.loads('PASTE_YOUR_COPIED_ABI_HERE')

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# 3. Load your Dataset (Update this path to your BoT-IoT CSV)
dataset_path = r"C:\Users\pc\Downloads\new artefact\path_to_your_bot_iot.csv"
df = pd.read_csv(dataset_path, nrows=50) # Testing with first 50 rows

def run_simulation():
    account = w3.eth.accounts[0] # Using the first Ganache account
    
    print(f"--- Starting IoT Security Simulation ---")
    
    for i, row in df.iterrows():
        # We use a hash of the sequence ID to represent the "Data Packet"
        data_hash = w3.keccak(text=str(row['pkSeqID']))
        
        print(f"Testing Packet {i} | Source: {row['saddr']} | Category: {row['category']}")
        
        try:
            # This sends the data to the Blockchain for validation
            tx = contract.functions.validateTraffic(
                account, 
                data_hash
            ).transact({'from': account})
            
            print(f"  [PASSED] Blockchain Logged: {tx.hex()}")
        except Exception as e:
            print(f"  [BLOCKED] Security Alert: {e}")

if __name__ == "__main__":
    if w3.is_connected():
        run_simulation()
    else:
        print("Error: Could not connect to Ganache. Is it running?")