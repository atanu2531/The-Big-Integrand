import tensorflow as tf
import numpy as np
import os

def generate_data(n_samples=1000):
    """Generates synthetic data for a simple regression task."""
    np.random.seed(42)
    X = np.random.randn(n_samples, 10).astype(np.float32)
    # y = 3*x1 - 2*x2 + 0.5*x3 + noise
    y = 3 * X[:, 0] - 2 * X[:, 1] + 0.5 * X[:, 2] + np.random.randn(n_samples).astype(np.float32) * 0.1
    y = y.reshape(-1, 1)
    return X, y

def train():
    """Trains a simple neural network using TensorFlow."""
    print("Generating data...")
    X, y = generate_data()

    print("Building model...")
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(16, activation='relu', input_shape=(10,)),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')

    print("Training model...")
    model.fit(X, y, epochs=10, batch_size=32, verbose=1)

    print("Evaluating model...")
    loss = model.evaluate(X, y, verbose=0)
    print(f"Final Loss: {loss:.4f}")

    # Save the model
    os.makedirs('models', exist_ok=True)
    model.save('models/tf_model.h5')
    print("Model saved to models/tf_model.h5")

if __name__ == "__main__":
    train()
