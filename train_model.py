import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from sklearn.metrics import classification_report
import joblib
from preprocess import load_and_preprocess

X_train, X_test, y_train, y_test, num_classes = load_and_preprocess()

def build_model(input_dim, classes):
    model = models.Sequential([
        layers.Input(shape=(input_dim,)),
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.2),
        layers.Dense(32, activation='relu'),
        layers.Dense(classes, activation='softmax')
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

model = build_model(X_train.shape[1], num_classes)

early_stop = callbacks.EarlyStopping(monitor='val_loss', patience=4, restore_best_weights=True)

print("[*] Training Deep Learning NIDS model...")
model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=25,
    batch_size=64,
    callbacks=[early_stop],
    verbose=1
)

model.save('models/nids_model.keras')
print("[+] Model saved to models/nids_model.keras")

# Evaluate Model Performance
y_pred = np.argmax(model.predict(X_test), axis=1)
encoder = joblib.load('models/encoder.pkl')
print("\n--- MODEL PERFORMANCE METRICS ---")
print(classification_report(y_test, y_pred, target_names=encoder.classes_))