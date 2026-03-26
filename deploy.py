from web3 import Web3
import json
import os

# 1. Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
if not w3.is_connected():
    print("Error: Could not connect to Ganache at 127.0.0.1:8545")
    exit()

w3.eth.default_account = w3.eth.accounts[0]

# 2. Path to your artifact
artifact_path = './artifacts/IoTSecurity.json'

try:
    with open(artifact_path, 'r') as f:
        artifact = json.load(f)
    
    # Extract ABI
    abi = artifact.get('abi')
    
    # Handle different JSON structures for Bytecode (Truffle vs Hardhat vs Solc)
    bytecode = artifact.get('bytecode')
    if isinstance(bytecode, dict): # Hardhat format
        bytecode = bytecode.get('object')
    if not bytecode: # Solc standard output format
        bytecode = artifact.get('evm', {}).get('bytecode', {}).get('object')

    if not bytecode or bytecode == "0x":
        print(f"Error: No bytecode found in {artifact_path}. Try recompiling your .sol file.")
        exit()

    # 3. Create & Deploy Contract
    print("Deploying IoTSecurity contract...")
    IoTSecurity = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    tx_hash = IoTSecurity.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print("\n" + "="*30)
    print("DEPLOYMENT SUCCESSFUL")
    print("="*30)
    print(f"Contract Address: {tx_receipt.contractAddress}")
    print(f"Deployed by:      {w3.eth.default_account}")
    print("="*30)
    print("\nCopy the Contract Address into your 'iot_bridge.py' script.")

except FileNotFoundError:
    print(f"Error: Could not find {artifact_path}. Ensure you are in the correct directory.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")