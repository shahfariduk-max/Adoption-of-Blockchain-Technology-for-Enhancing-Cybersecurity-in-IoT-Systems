import pandas as pd
from web3 import Web3
import json

# 1. Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# 2. Update these two lines with your actual data from Remix
CONTRACT_ADDRESS = "PASTE_YOUR_ADDRESS_HERE" 
ABI_JSON = 'PASTE_YOUR_ABI_HERE'

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=json.loads(ABI_JSON))

# 3. Path to your BoT-IoT Dataset
# I've used the path from your earlier tree listing
dataset_path = r"C:\Users\pc\Downloads\new artefact\BoT-IoT_Selected_Features.csv" 

def start_iot_simulation():
    account = w3.eth.accounts[0]
    
    # Load first 20 rows for a quick test
    try:
        df = pd.read_csv(dataset_path, nrows=20)
    except FileNotFoundError:
        print("Dataset not found! Please check the filename in your Downloads folder.")
        return

    print("--- Starting Blockchain-IoT Security Validation ---")

    for i, row in df.iterrows():
        # Representing the IoT packet as a hash
        packet_id = w3.keccak(text=str(row.get('pkSeqID', i)))
        
        print(f"Testing Device: {row.get('saddr', 'Unknown')} | Category: {row.get('category', 'Normal')}")
        
        try:
            # Send transaction to validate on-chain
            tx_hash = contract.functions.validateTraffic(
                account, 
                packet_id
            ).transact({'from': account})
            
            print(f"  [SUCCESS] Blocked/Logged on Chain: {tx_hash.hex()}")
        except Exception as e:
            print(f"  [ALERT] Security Logic Blocked Transaction: {e}")

if __name__ == "__main__":
    if w3.is_connected():
        start_iot_simulation()
    else:
        print("Could not connect to Ganache. Ensure Ganache is running!")