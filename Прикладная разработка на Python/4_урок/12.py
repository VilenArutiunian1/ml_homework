import numpy as np

def fill_na_with_median(X: np.ndarray) -> np.ndarray:

    j = []
    for i in range(len(X[0])):
        a = []
        for s in range(len(X)):
            a.append(X[s][i])
        j.append(np.array(a))

        
    j = np.array(j)
    for i in range(len(X[0])):
        median = np.nanmedian(j[i])
        for s in range(len(j[i])):
            if np.isnan(j[i][s]):
                print(j[i][s], 'a')
                j[i][s] = median

    return j.T