from web3 import Web3

# Connect to your fresh Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3.eth.default_account = w3.eth.accounts[0]

# Standard ABI for your IoTSecurity.sol
abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"device","type":"address"},{"indexed":False,"internalType":"string","name":"reason","type":"string"}],"name":"AccessDenied","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"device","type":"address"},{"indexed":False,"internalType":"bytes32","name":"dataHash","type":"bytes32"}],"name":"DataLogged","type":"event"},{"inputs":[{"internalType":"address","name":"_dev","type":"address"}],"name":"blockDevice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"devices","outputs":[{"internalType":"bool","name":"isRegistered","type":"bool"},{"internalType":"bool","name":"isBlocked","type":"bool"},{"internalType":"string","name":"deviceType","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_dev","type":"address"},{"internalType":"string","name":"_type","type":"string"}],"name":"registerDevice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_dev","type":"address"},{"internalType":"bytes32","name":"_dataHash","type":"bytes32"}],"name":"validateTraffic","outputs":[],"stateMutability":"nonpayable","type":"function"}]

# Compiled Bytecode for your IoTSecurity.sol
bytecode = "608060405234801561001057600080fd5b5033600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506102608061005e6000396000f3fe608060405234801561001057600080fd5b506004361061005b5760003560e01c8063162394541261001057806326e069271161003e57806326e06927146100985780633b4904f4146100c1578063945c79e6146100e4575b806307374b59146100605780631165a6c314610075575b600080fd5b6100736004803603602081101561007157600080fd5b5035610107565b005b6100736004803603602081101561008b57600080fd5b503561014e565b6100af600480360360208110156100ae57600080fd5b50356000908152602081905260409020546001600160a01b031681565b6040516001600160a01b03909116815260200161004b565b6100af600480360360208110156100d757600080fd5b503561018c565b610073600480360360408110156100fa57600080fd5b50803560208201356101db565b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16331461014c576040517f08c379a00000000000000000000000000000000000000000000000000000000060048152602060248152600e604481526d4e6f7420617574686f72697a656460901b60648252608490f35b565b6000908152602081905260409020600082016001905550565b60009081526020819052604090208054600101905550565b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff163314610225576040517f08c379a00000000000000000000000000000000000000000000000000000000060048152602060248152600e604481526d4e6f7420617574686f72697a656460901b60648252608490f35b60009182526020918290526040912060008201600190556001820160009055505056fea26469706673582212204c86518f8e08d66929a67a052903944297bec5a9b8044176b7ed526165272ac464736f6c63430008120033"

print("Deploying new contract to fresh Ganache...")
Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Contract.constructor().transact()
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"\nSUCCESS! New Contract Address: {receipt.contractAddress}")
print("Update your scripts with this address now.")