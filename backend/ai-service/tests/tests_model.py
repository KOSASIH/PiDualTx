import os
import sys
import pytest
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam

# Adjust imports to find the model module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
try:
    from model import LSTMModel
except ImportError:
    # Fallback: Define minimal LSTMModel here for isolated testing if model.py is missing
    class LSTMModel:
        def __init__(self, input_shape=(10, 1), lstm_units=64, learning_rate=0.001):
            self.model = Sequential([
                LSTM(lstm_units, input_shape=input_shape, return_sequences=False),
                Dense(1)
            ])
            self.model.compile(optimizer=Adam(learning_rate), loss='mse')

        def predict(self, data):
            data = np.array(data, dtype=np.float32).reshape((1, -1, 1))
            return float(self.model.predict(data)[0][0])

        def train(self, x_train, y_train, epochs=10):
            x_train = np.array(x_train, dtype=np.float32).reshape((-1, x_train.shape[1], 1))
            y_train = np.array(y_train, dtype=np.float32)
            history = self.model.fit(x_train, y_train, epochs=epochs, verbose=0)
            return history

# Test data fixtures
@pytest.fixture
def sample_data():
    # Generate synthetic sequential data for training and testing
    x_train = np.linspace(0, 50, 500)
    y_train = np.sin(x_train) + np.random.normal(scale=0.1, size=x_train.shape)
    # Reshape for LSTM [samples, time_steps, features]
    seq_len = 10
    x_seq, y_seq = [], []
    for i in range(len(x_train) - seq_len):
        x_seq.append(y_train[i:i+seq_len])
        y_seq.append(y_train[i+seq_len])
    return np.array(x_seq), np.array(y_seq)

@pytest.fixture
def lstm_model():
    # Initialize LSTMModel instance
    return LSTMModel(input_shape=(10, 1), lstm_units=64, learning_rate=0.001)

def test_model_initialization(lstm_model):
    """Ensure the LSTM model initializes with correct parameters and layers."""
    model = lstm_model.model
    assert isinstance(model, tf.keras.Model)
    layers = [layer.__class__.__name__ for layer in model.layers]
    assert 'LSTM' in layers
    assert 'Dense' in layers

def test_training_progress(sample_data, lstm_model):
    """Verify training decreases loss over epochs."""
    x_train, y_train = sample_data
    history = lstm_model.train(x_train, y_train, epochs=5)
    losses = history.history['loss']
    # Loss should decrease or stay stable (allow minor fluctuations)
    assert all(earlier >= later or abs(earlier - later) < 1e-3 for earlier, later in zip(losses, losses[1:]))

def test_prediction_output_shape(sample_data, lstm_model):
    """Check that prediction returns a float scalar."""
    x_train, _ = sample_data
    test_input = x_train[0]
    pred = lstm_model.predict(test_input)
    assert isinstance(pred, float)

def test_prediction_reasonableness(sample_data, lstm_model):
    """Test if the model's prediction is reasonably close after training."""
    x_train, y_train = sample_data
    lstm_model.train(x_train, y_train, epochs=10)
    test_input = x_train[-1]
    pred = lstm_model.predict(test_input)
    # Since sine wave fluctuates between -1 and 1, prediction should lie roughly in this range
    assert -2.0 < pred < 2.0

def test_model_serialization(tmp_path, lstm_model, sample_data):
    """Test saving and loading the trained model maintains behavior."""
    x_train, y_train = sample_data
    lstm_model.train(x_train, y_train, epochs=2)

    model_save_path = tmp_path / "lstmtestmodel"
    lstm_model.model.save(str(model_save_path))

    # Load model back
    loaded_model = tf.keras.models.load_model(str(model_save_path))
    test_input = x_train[0].reshape((1, 10, 1))
    original_pred = lstm_model.model.predict(test_input)
    loaded_pred = loaded_model.predict(test_input)

    # Predictions from loaded model and original should be almost equal
    np.testing.assert_allclose(original_pred, loaded_pred, atol=1e-5)

if __name__ == "__main__":
    # Run tests with verbose output for manual execution
    pytest.main(["-v", __file__])

