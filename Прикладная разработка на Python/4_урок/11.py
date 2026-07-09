import numpy as np

def ridge_inverse(X: np.ndarray, lambda_: float) -> np.ndarray:
    """
    Возвращает обратную матрицу для Ridge регрессии:
    (X^T X + lambda * I)^-1
    """
    return np.linalg.inv(((X.T).dot(X) + lambda_ * np.eye(len(X[0]))))

