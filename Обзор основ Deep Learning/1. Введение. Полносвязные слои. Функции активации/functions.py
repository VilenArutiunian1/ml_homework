import torch
from torch import nn

torch.manual_seed(42)

def function01(tensor: torch.Tensor, count_over: str) -> torch.Tensor:
    if count_over == 'columns':
        return tensor.mean(axis=0)
    elif count_over == 'rows':
        return tensor.mean(axis=1)

print(function01(torch.tensor([[0.8823, 0.9150, 0.3829],[0.9593, 0.3904, 0.6009],[0.2566, 0.7936, 0.9408]]), 'rows'))
print(function01(torch.tensor([[0.8823, 0.9150, 0.3829],[0.9593, 0.3904, 0.6009],[0.2566, 0.7936, 0.9408]]), 'columns'))

def function02(dataset: torch.Tensor):
    return torch.rand(dataset.shape[1], dtype=torch.float32, requires_grad = True)

def function03(x: torch.Tensor, y: torch.Tensor):
    weights = function02(x)
    learning_rate = 1e-2
    n_steps = 300

    for i in range(n_steps):
        y_pred = x @ weights
        mse = torch.mean((y_pred - y) ** 2)

        print(f'Шаг {i + 1:3d}: MSE = {mse.item():.5f}')

        mse.backward()
        with torch.no_grad():
            weights -= weights.grad * learning_rate 

        weights.grad.zero_()

    return weights

def function04(x: torch.Tensor, y: torch.Tensor):
    layer = nn.Linear(in_features=x.shape[1], out_features=1)

    max_steps = 10000
    learning_rate = 1e-2
    mse = 10**10

    i = 0

    while mse > 0.3 and i < max_steps:
        y_pred = layer(x).ravel()
        mse = torch.mean((y - y_pred) ** 2)

        print(f'Шаг {i + 1:3d}: MSE = {mse.item():.5f}')

        mse.backward()
        
        with torch.no_grad():
            for p in layer.parameters():
                p -= p.grad * learning_rate
                p.grad.zero_()

        i += 1

    return layer