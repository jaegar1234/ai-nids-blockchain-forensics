import json
from solcx import compile_standard, install_solc
from web3 import Web3

# Install specific Solidity compiler version
install_solc('0.8.0')

with open("contracts/forensic_logger.sol", "r") as file:
    contract_source_code = file.read()

# Compile Solidity code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"ForensicLogger.sol": {"content": contract_source_code}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

bytecode = compiled_sol["contracts"]["ForensicLogger.sol"]["ForensicLogger"]["evm"]["bytecode"]["object"]
abi = json.loads(compiled_sol["contracts"]["ForensicLogger.sol"]["ForensicLogger"]["metadata"])["output"]["abi"]

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
assert w3.is_connected(), "Error: Ganache is not running on port 8545"

deployer_account = w3.eth.accounts[0]

# Deploy contract
ForensicContract = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = ForensicContract.constructor().transact({'from': deployer_account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = tx_receipt.contractAddress
print(f"[+] ForensicLogger Contract Deployed to: {contract_address}")

# Save deployment artifacts for pipeline
deployment_info = {
    "contract_address": contract_address,
    "abi": abi
}
with open("contract_info.json", "w") as f:
    json.dump(deployment_info, f, indent=2)

print("[+] Deployment metadata saved to contract_info.json")