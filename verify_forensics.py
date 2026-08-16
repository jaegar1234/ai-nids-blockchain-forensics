import json
from web3 import Web3
import datetime

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

with open("contract_info.json", "r") as f:
    contract_meta = json.load(f)

contract = w3.eth.contract(
    address=contract_meta["contract_address"],
    abi=contract_meta["abi"]
)

total = contract.functions.totalIncidents().call()
print(f"=================================================================")
print(f"       IMMUTABLE FORENSIC AUDIT TRAIL (Total Incidents: {total})")
print(f"=================================================================")

for idx in range(1, total + 1):
    rec = contract.functions.getIncident(idx).call()
    rec_id, inc_hash, src, dst, attack, conf, block_ts = rec
    
    readable_date = datetime.datetime.fromtimestamp(block_ts, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    
    print(f"\n[Incident Record #{rec_id}]")
    print(f"  • Block Timestamp : {readable_date}")
    print(f"  • Attack Vector   : {attack} (Confidence: {conf / 100:.2f}%)")
    print(f"  • Source / Target : {src} -> {dst}")
    print(f"  • Evidence Hash   : {inc_hash}")