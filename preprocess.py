import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib

os.makedirs('data', exist_ok=True)
os.makedirs('models', exist_ok=True)

CSV_PATH = 'data/network_traffic.csv'

# Generate synthetic network flow data if no CSV exists
if not os.path.exists(CSV_PATH):
    print("[*] Generating synthetic network flow dataset for initial pipeline testing...")
    np.random.seed(42)
    n_samples = 8000

    # Flow Features: duration, fwd_pkts, bwd_pkts, pkt_len_mean, syn_flags, ack_flags, bytes_sec
    benign = np.random.normal(loc=[100, 10, 8, 250, 1, 1, 5000], scale=[20, 2, 2, 30, 0.2, 0.2, 500], size=(n_samples // 2, 7))
    dos = np.random.normal(loc=[1500, 200, 10, 1200, 1, 0, 80000], scale=[100, 20, 3, 100, 0.1, 0.1, 5000], size=(n_samples // 6, 7))
    portscan = np.random.normal(loc=[10, 2, 0, 40, 1, 0, 200], scale=[2, 1, 0.1, 5, 0.1, 0.1, 50], size=(n_samples // 6, 7))
    synflood = np.random.normal(loc=[300, 500, 0, 60, 500, 0, 45000], scale=[30, 40, 0.1, 10, 30, 0.1, 3000], size=(n_samples // 6, 7))

    data = np.vstack([benign, dos, portscan, synflood])
    labels = (['BENIGN'] * (n_samples // 2) + 
              ['DoS'] * (n_samples // 6) + 
              ['PortScan'] * (n_samples // 6) + 
              ['SYN_Flood'] * (n_samples // 6))

    cols = ['flow_duration', 'fwd_pkts', 'bwd_pkts', 'pkt_len_mean', 'syn_flags', 'ack_flags', 'bytes_sec']
    df = pd.DataFrame(data, columns=cols)
    df['label'] = labels
    df.to_csv(CSV_PATH, index=False)
    print(f"[+] Dataset saved to {CSV_PATH}")

def load_and_preprocess():
    df = pd.read_csv(CSV_PATH)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)

    X = df.drop(columns=['label'])
    y = df['label']

    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)
    joblib.dump(encoder, 'models/encoder.pkl')

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    joblib.dump(scaler, 'models/scaler.pkl')

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    print(f"[+] Features scaled. Classes: {list(encoder.classes_)}")
    return X_train, X_test, y_train, y_test, len(encoder.classes_)

if __name__ == "__main__":
    load_and_preprocess()
