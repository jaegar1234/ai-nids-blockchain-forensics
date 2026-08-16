import time
import json
import hashlib
import numpy as np
import joblib
import tensorflow as tf
from web3 import Web3

# 1. Connect to Local Blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
assert w3.is_connected(), "Ganache node unreachable"

account = w3.eth.accounts[0]

# 2. Load Contract Artifacts
with open("contract_info.json", "r") as f:
    contract_meta = json.load(f)

contract = w3.eth.contract(
    address=contract_meta["contract_address"],
    abi=contract_meta["abi"]
)

# 3. Load Trained ML Model & Preprocessors
model = tf.keras.models.load_model('models/nids_model.keras')
scaler = joblib.load('models/scaler.pkl')
encoder = joblib.load('models/encoder.pkl')

def compute_evidence_hash(timestamp, src_ip, dst_ip, attack_type, confidence_score):
    raw_payload = f"{timestamp}|{src_ip}|{dst_ip}|{attack_type}|{confidence_score}"
    return hashlib.sha256(raw_payload.encode('utf-8')).hexdigest()

def process_flow(flow_vector, src_ip, dst_ip):
    # Feature Scaling
    scaled = scaler.transform([flow_vector])
    
    # DL Inference
    probs = model.predict(scaled, verbose=0)[0]
    pred_idx = np.argmax(probs)
    confidence = float(probs[pred_idx])
    label = encoder.inverse_transform([pred_idx])[0]

    curr_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    print(f"\n--- [TELEMETRY] Ingress Flow from {src_ip} -> {dst_ip} ---")
    print(f"Prediction: {label} | Confidence: {confidence*100:.2f}%")

    # Threat Detection Trigger
    if label != "BENIGN" and confidence >= 0.85:
        scaled_conf = int(confidence * 10000) # e.g., 99.12% -> 9912
        evidence_hash = compute_evidence_hash(curr_time, src_ip, dst_ip, label, scaled_conf)
        
        print(f"[!] THREAT DETECTED: Anchoring to Blockchain...")
        print(f"    Evidence SHA-256: {evidence_hash}")

        # Send Transaction to Smart Contract
        tx_hash = contract.functions.logIncident(
            evidence_hash,
            src_ip,
            dst_ip,
            label,
            scaled_conf
        ).transact({'from': account})

        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"[+] IMMUTABLE COMMIT SUCCESSFUL!")
        print(f"    Tx Hash: {receipt.transactionHash.hex()}")
        print(f"    Block Number: {receipt.blockNumber} | Gas Used: {receipt.gasUsed}")
    else:
        print("[+] Status: Normal Traffic Permitted.")

if __name__ == "__main__":
    print("[*] NIDS & Blockchain Forensic Pipeline Running...")
    
    # Test Vector 1: Normal benign web request
    normal_vector = [95, 11, 7, 240, 1, 1, 4800]
    process_flow(normal_vector, src_ip="192.168.1.45", dst_ip="10.0.0.1")

    # Test Vector 2: High-volume DoS flow
    dos_vector = [1600, 220, 12, 1250, 1, 0, 85000]
    process_flow(dos_vector, src_ip="185.220.101.5", dst_ip="10.0.0.1")

    # Test Vector 3: SYN Flood flow
    syn_vector = [310, 520, 0, 62, 510, 0, 47000]
    process_flow(syn_vector, src_ip="198.51.100.77", dst_ip="10.0.0.1")