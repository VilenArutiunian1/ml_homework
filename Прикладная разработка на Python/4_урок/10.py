import numpy as np
import pandas as pd

def detect_outliers(x: np.ndarray) -> np.ndarray:
    s = pd.Series(x)
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5*iqr
    upper = q3 + 1.5*iqr
    return np.array((s < lower) | (s > upper))