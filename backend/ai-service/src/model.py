"""
model.py

Contains LSTM model architecture and training functions for Pi price prediction.

Features:
- Configurable LSTM model with multiple layers.
- Advanced preprocessing utilities.
- Training loop with early stopping.
- Model saving and loading utilities.
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import numpy as np
import os

class PiPriceLSTM:
    def __init__(self, sequence_length: int, feature_dim: int = 1, lstm_units: int = 100,
                 dropout_rate: float = 0.2, model_dir: str = "model"):
        self.sequence_length = sequence_length
        self.feature_dim = feature_dim
        self.lstm_units = lstm_units
        self.dropout_rate = dropout_rate
        self.model_dir = model_dir
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential([
            LSTM(self.lstm_units, return_sequences=True, input_shape=(self.sequence_length, self.feature_dim)),
            Dropout(self.dropout_rate),
            LSTM(self.lstm_units // 2),
            Dropout(self.dropout_rate),
            Dense(1, activation='linear')
        ])
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model

    def train(self, X_train: np.ndarray, y_train: np.ndarray,
              X_val: np.ndarray, y_val: np.ndarray,
              batch_size: int = 64, epochs: int = 100, patience: int = 10):
        """
        Train the LSTM model with early stopping and model checkpoint

        Args:
            X_train (np.ndarray): Training feature data shape (samples, sequence_length, features)
            y_train (np.ndarray): Training labels shape (samples,)
            X_val (np.ndarray): Validation feature data
            y_val (np.ndarray): Validation labels
            batch_size (int): Batch size for training
            epochs (int): Maximum number of epochs
            patience (int): Number of epochs with no improvement to stop training

        Returns:
            History object from model.fit()
        """
        os.makedirs(self.model_dir, exist_ok=True)
        checkpoint_path = os.path.join(self.model_dir, "pi_price_lstm_best.h5")

        early_stopping = EarlyStopping(monitor='val_loss', patience=patience, restore_best_weights=True)
        checkpoint = ModelCheckpoint(checkpoint_path, monitor='val_loss', save_best_only=True, verbose=1)

        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            batch_size=batch_size,
            epochs=epochs,
            callbacks=[early_stopping, checkpoint],
            verbose=2
        )
        return history

    def predict(self, X_input: np.ndarray) -> np.ndarray:
        """
        Perform prediction given input sequences

        Args:
            X_input (np.ndarray): Input features shape (samples, sequence_length, features)

        Returns:
            np.ndarray: Predicted price values
        """
        return self.model.predict(X_input)

    def save_model(self, path: str):
        self.model.save(path)

    def load_model(self, path: str):
        self.model = tf.keras.models.load_model(path)

# Utilities for data preprocessing

def normalize_data(data: np.ndarray):
    """
    Normalize data using min-max scaling to [0,1]

    Args:
        data (np.ndarray): Array to normalize

    Returns:
        normalized_data, min_val, max_val
    """
    min_val = np.min(data)
    max_val = np.max(data)
    normalized_data = (data - min_val) / (max_val - min_val) if max_val > min_val else np.zeros_like(data)
    return normalized_data, min_val, max_val

def denormalize_data(normalized_data: np.ndarray, min_val: float, max_val: float):
    """
    Restore original scale from normalized data

    Args:
        normalized_data (np.ndarray): Normalized data array
        min_val (float): Minimum value used in normalization
        max_val (float): Maximum value used in normalization

    Returns:
        Denormalized data array
    """
    return normalized_data * (max_val - min_val) + min_val

def create_sequences(data: np.ndarray, seq_length: int):
    """
    Create overlapping sequences from 1D data array for LSTM input.

    Args:
        data (np.ndarray): 1D array of price data
        seq_length (int): Length of each sequence

    Returns:
        np.ndarray: Array of shape (num_samples, seq_length, 1)
    """
    sequences = []
    labels = []
    for i in range(len(data) - seq_length):
        seq = data[i:i+seq_length]
        label = data[i+seq_length]
        sequences.append(seq)
        labels.append(label)
    return np.array(sequences).reshape(-1, seq_length, 1), np.array(labels)

if __name__ == "__main__":
    # Example usage: train on dummy data for testing
    import matplotlib.pyplot as plt

    # Generate dummy sine wave data for demonstration
    timesteps = 500
    x = np.linspace(0, 50, timesteps)
    data = np.sin(x) + np.random.normal(scale=0.1, size=timesteps)

    normalized_data, min_val, max_val = normalize_data(data)

    seq_len = 20
    X, y = create_sequences(normalized_data, seq_len)

    split = int(len(X) * 0.8)
    X_train, y_train = X[:split], y[:split]
    X_val, y_val = X[split:], y[split:]

    model_obj = PiPriceLSTM(sequence_length=seq_len)
    history = model_obj.train(X_train, y_train, X_val, y_val, epochs=30)

    # Plot training loss
    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.legend()
    plt.title("Training Loss")
    plt.show()

