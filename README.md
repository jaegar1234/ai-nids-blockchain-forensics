# ai-nids-blockchain-forensics
AI-powered Network Intrusion Detection System (NIDS) built with TensorFlow and Python, integrated with an Ethereum Solidity smart contract to detect network attacks in real time and anchor tamper-proof forensic logs directly to the blockchain.
# AI-Driven NIDS & Blockchain Forensic Logger

A cybersecurity tool that detects network attacks using **Deep Learning** and records tamper-proof incident logs to a local **Ethereum Blockchain**.

---

##  What This Project Does

1. **Detects Cyberattacks:** A deep learning model analyzes incoming network traffic to detect attacks (DoS, Port Scans, SYN Floods) in real time.
2. **Creates Evidence Hashes:** When an attack is detected, the system generates a cryptographic **SHA-256 hash** of the event details.
3. **Locks Logs on Blockchain:** The incident is saved to a **Solidity smart contract**, creating an immutable audit trail that prevents attackers from deleting logs after a breach.

---

##  Built With

* **Python 3.10+** — Core scripting and automation
* **TensorFlow / Keras** — Deep learning intrusion detection model
* **Solidity & Ganache** — Smart contract and local Ethereum blockchain
* **Web3.py** — Connecting Python to the blockchain

---

##  Project Structure

* `contracts/ForensicLogger.sol` — Smart contract that stores the incident records.
* `preprocess.py` — Generates and scales network flow dataset.
* `train_model.py` — Trains the deep neural network classifier.
* `deploy_contract.py` — Deploys the smart contract to Ganache.
* `main_pipeline.py` — Runs live attack detection and sends logs to the blockchain.
* `verify_forensics.py` — Reads and displays the permanent logs from the blockchain.

---

##  Quick Start Guide

### 1. Install Requirements
```bash
npm install -g ganache
pip install tensorflow scikit-learn pandas numpy joblib web3 py-solc-x
2. Run the Blockchain (Terminal 1)
Bash
ganache --port 8545
(Leave this terminal open and running)

3. Run the Detection Pipeline (Terminal 2)
Bash
# Step A: Prepare data and train the AI
python preprocess.py
python train_model.py

# Step B: Deploy the smart contract
python deploy_contract.py

# Step C: Run live detection and logging
python main_pipeline.py

# Step D: View the permanent blockchain audit trail
python verify_forensics.py
 Key Takeaways for SOC / Forensics
Demonstrates machine learning applied to network security telemetry.

Solves log tampering risks by leveraging decentralized immutable storage.

Tracks adversary techniques including volumetric DoS and port scans.
