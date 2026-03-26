import os
from web3 import Web3
import json

# 1. Connection Settings
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# 2. Contract Details (From your successful deployment)
contract_address = "0x3a0eff57be10988576e20190a9dc56ab09660722"
admin_account = "0x592d290385A1BBeaF90789B596EB5F9b4a8FD710"

# Minimal ABI for the functions we are using
abi = json.loads('[{"inputs":[{"internalType":"address","name":"_device","type":"address"},{"internalType":"string","name":"_type","type":"string"}],"name":"registerDevice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_device","type":"address"},{"internalType":"string","name":"_data","type":"string"}],"name":"validateTraffic","outputs":[],"stateMutability":"nonpayable","type":"function"}]')

contract = web3.eth.contract(address=contract_address, abi=abi)

def simulate_security_audit():
    dataset_path = r"C:\Users\pc\Downloads\new artefact\SolidiFI-benchmark-master\buggy_contracts"
    
    # We will treat each vulnerability folder as a "Device Type" for the simulation
    vulnerabilities = ["Overflow-Underflow", "Re-entrancy", "Timestamp-Dependency"]

    for vuln in vulnerabilities:
        folder_path = os.path.join(dataset_path, vuln)
        if os.path.exists(folder_path):
            files = os.listdir(folder_path)
            
            # Simulate a "Device ID" based on the folder index
            device_id = web3.eth.accounts[vulnerabilities.index(vuln) + 1]
            
            print(f"--- Processing {vuln} ---")
            
            # Step A: Register the "Device" (The Vulnerability Class)
            tx_hash = contract.functions.registerDevice(device_id, vuln).transact({'from': admin_account})
            web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Registered {vuln} as Device {device_id}")

            # Step B: Log a "Traffic" event for the first file found
            if files:
                report_data = f"Scanning {files[0]} - Anomalies detected: TRUE"
                log_tx = contract.functions.validateTraffic(device_id, report_data).transact({'from': admin_account})
                print(f"Logged security audit for {files[0]} to blockchain.")

simulate_security_audit()