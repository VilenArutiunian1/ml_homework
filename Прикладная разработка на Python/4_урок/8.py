import numpy as np

def normalize(X: np.ndarray) -> np.ndarray:
    min_vals = np.min(X, axis=0)
    max_vals = np.max(X, axis=0)
    return (X - min_vals) / (max_vals - min_vals)