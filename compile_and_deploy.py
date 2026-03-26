import json
from web3 import Web3
from solcx import compile_standard, install_solc

# 1. Setup Connection
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.eth.default_account = w3.eth.accounts[0]

# 2. Compile the Solidity Contract
print("Installing Solidity compiler...")
install_solc("0.8.20") # You can change this to match your .sol pragma version

with open("IoTSecurity.sol", "r") as file:
    iot_security_file = file.read()

print("Compiling IoTSecurity.sol...")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"IoTSecurity.sol": {"content": iot_security_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.20",
)

# Extract Bytecode and ABI
# Note: Ensure the contract name matches 'IoTSecurity' inside your .sol file
bytecode = compiled_sol["contracts"]["IoTSecurity.sol"]["IoTSecurity"]["evm"]["bytecode"]["object"]
abi = json.loads(compiled_sol["contracts"]["IoTSecurity.sol"]["IoTSecurity"]["metadata"])["output"]["abi"]

# 3. Deploy to Ganache
print("Deploying to Ganache...")
IoTSecurity = w3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = IoTSecurity.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("\n" + "="*40)
print(f"DEPLOYMENT SUCCESSFUL!")
print(f"Contract Address: {tx_receipt.contractAddress}")
print("="*40)

# 4. Save the new ABI to your artifacts folder for iot_bridge.py
with open("./artifacts/IoTSecurity.json", "w") as f:
    json.dump({"abi": abi}, f)
print("\nUpdated './artifacts/IoTSecurity.json' with the new ABI.")