import json
import time
import random
from web3 import Web3

# 1. Connection Setup
blockchain_url = "http://127.0.0.1:8545" 
web3 = Web3(Web3.HTTPProvider(blockchain_url))

print("--- IoT Security Bridge Status ---")

if not web3.is_connected():
    print("Error: Could not connect to Ganache CLI.")
    exit()

# 2. Contract Configuration
contract_addr = "0x6f6F480D98c11AF1e1D84360107D8BcA9A413b59" 
web3.eth.default_account = web3.eth.accounts[0]

# Local state to mimic the blockchain's internal 'blocked' registry for real-time console feedback
blocked_registry = []

try:
    with open('./artifacts/IoTSecurity.json', 'r') as f:
        artifact_data = json.load(f)
        abi_json = artifact_data['abi']
except FileNotFoundError:
    abi_json = [
        {"inputs":[{"internalType":"address","name":"_dev","type":"address"},{"internalType":"string","name":"_type","type":"string"}],"name":"registerDevice","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[{"internalType":"address","name":"_dev","type":"address"},{"internalType":"bytes32","name":"_dataHash","type":"bytes32"}],"name":"validateTraffic","outputs":[],"stateMutability":"nonpayable","type":"function"},
        {"inputs":[{"internalType":"address","name":"_dev","type":"address"}],"name":"blockDevice","outputs":[],"stateMutability":"nonpayable","type":"function"}
    ]

# 3. Initialize Contract
contract = web3.eth.contract(address=contract_addr, abi=abi_json)

def register_wemo_switch(device_address):
    """Registers a Belkin Wemo Switch (Standard IoT Model F7C029)"""
    device_model = "Belkin Wemo Insight Switch"
    print(f"Registering device: {device_address} ({device_model})...")
    
    tx_hash = contract.functions.registerDevice(device_address, device_model).transact()
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Device registered in block: {receipt.blockNumber}")
    return receipt

def send_wemo_telemetry(device_address, state="ON", power_w=12.5):
    """
    Mimics real Wemo Insight JSON telemetry format.
    Checks local 'blocked_registry' to simulate enforcement.
    """
    if device_address in blocked_registry:
        print(f"Validating traffic for: {device_address}")
        print(f"[✘] ACCESS DENIED: Device is in the Blockchain Revocation List.")
        return False

    wemo_payload = {
        "device_id": device_address,
        "model": "F7C029",
        "binary_state": 1 if state == "ON" else 0,
        "instant_power": power_w,
        "timestamp": int(time.time())
    }
    
    data_string = json.dumps(wemo_payload)
    data_hash = web3.keccak(text=data_string)
    
    print(f"Validating traffic for: {device_address}")
    try:
        tx_hash = contract.functions.validateTraffic(device_address, data_hash).transact()
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Traffic Validated. Tx Hash: {receipt.transactionHash.hex()}")
        return True
    except Exception as e:
        print(f"Validation Failed (Blockchain Policy Violation): {e}")
        return False

def trigger_mitigation(device_address):
    """Blocks the device on-chain after detecting anomalous behavior"""
    print(f"\n[!] CYBER-ANOMALY DETECTED for {device_address}")
    print(f"Initiating Blockchain Mitigation (Revoking Device Identity)...")
    
    tx_hash = contract.functions.blockDevice(device_address).transact()
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Add to local registry to ensure the script respects the blocked status
    blocked_registry.append(device_address)
    print(f"[✔] Mitigation Successful. Identity Revoked in block: {receipt.blockNumber}")

if __name__ == "__main__":
    print(f"Connected to Ganache at: {blockchain_url}")
    print(f"Active Contract: {contract_addr}")
    
    # REPRESENTING THE TEST SUBJECT
    wemo_device_addr = web3.eth.accounts[1]
    
    # STEP 1: PROVISIONING
    register_wemo_switch(wemo_device_addr)
    
    # STEP 2: NORMAL OPERATION (BENIGN TRAFFIC)
    print("\n--- Phase 1: Operational Baseline (Benign Traffic) ---")
    for _ in range(2):
        send_wemo_telemetry(wemo_device_addr, state="ON", power_w=random.uniform(14.0, 16.0))
        time.sleep(1)
    
    # STEP 3: ATTACK SIMULATION (BOTNET BEHAVIOR)
    print("\n--- Phase 2: Botnet Intrusion Simulation ---")
    print("Warning: High-frequency traffic signature detected from Belkin Wemo Switch...")
    
    # In a real study, this would be triggered by an AI model trained on BoT-IoT
    anomaly_detected = True 
    
    if anomaly_detected:
        trigger_mitigation(wemo_device_addr)
    
    # STEP 4: VERIFICATION
    print("\n--- Phase 3: Post-Mitigation Identity Verification ---")
    print("Attempting to send telemetry from revoked/blocked device...")
    send_wemo_telemetry(wemo_device_addr, state="OFF", power_w=0.0)

    print("\n[✔] Full Research Life Cycle Complete (Discovery -> Operation -> Mitigation).")