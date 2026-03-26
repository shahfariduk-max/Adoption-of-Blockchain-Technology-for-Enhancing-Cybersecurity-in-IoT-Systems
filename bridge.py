import pandas as pd
from web3 import Web3
import json

# 1. Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# 2. Contract Details (Replace these after you deploy in Remix)
contract_address = "YOUR_DEPLOYED_CONTRACT_ADDRESS_HERE"
abi = json.loads('YOUR_CONTRACT_ABI_HERE')

contract = web3.eth.contract(address=contract_address, abi=abi)

# 3. Load BoT-IoT Dataset
# Adjust the path to where your BoT-IoT CSV is located
df = pd.read_csv('../path_to_your_bot_iot_file.csv', nrows=100) 

def simulate_iot_traffic():
    # Use the first account from Ganache
    sender_account = web3.eth.accounts[0]
    
    for index, row in df.iterrows():
        # Create a unique hash for the traffic data
        data_hash = web3.keccak(text=str(row['pkSeqID']))
        
        print(f"Simulating Device: {row['saddr']} | Attack Label: {row['category']}")
        
        # If the dataset says it's an attack, we'd normally block it. 
        # For now, let's just try to validate it on the blockchain.
        try:
            tx_hash = contract.functions.validateTraffic(
                sender_account, 
                data_hash
            ).transact({'from': sender_account})
            
            print(f"Transaction sent: {tx_hash.hex()}")
        except Exception as e:
            print(f"Blocked by Smart Contract: {e}")

if __name__ == "__main__":
    if web3.is_connected():
        print("Connected to Ganache!")
        simulate_iot_traffic()
    else:
        print("Connection failed. Check Ganache.")