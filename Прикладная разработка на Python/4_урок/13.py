import numpy as np

def one_hot_encode(categories: np.ndarray) -> tuple[np.ndarray, list[str]]:
    #categories = sorted(categories)
    unique_categories = sorted(list(set(categories)))

    if len(categories) == 0:
        return np.zeros((0, 0), dtype=int), []
    
    s = {}

    for i in range(len(unique_categories)):
        if s.get(unique_categories[i]) == None:
            s[unique_categories[i]] = i
        i += 1


    r = []
    for category in categories:
        l = []
        for i in range(len(unique_categories)):
            if i == s[category]:
                l.append(1)
            else:
                l.append(0)

        r.append(l)

    return (np.array(r), unique_categories)