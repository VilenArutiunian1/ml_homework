import torch
from torch import nn
from torch import utils
from torch import optim

def create_model():
    model = nn.Sequential(
        nn.Linear(100, 10),
        nn.ReLU(),
        nn.Linear(10, 1)
    )

    return model

def train(model: nn.Module, data_loader: utils.data.DataLoader, optimizer: optim.Optimizer, loss_fn):
    model.train()
    losses = []

    for x, y in data_loader:
        optimizer.zero_grad()

        loss = loss_fn(model(x), y)
        loss.backward() 

        print(round(loss.item(), 5))
        losses.append(loss.item())
        optimizer.step()

    return sum(losses) / len(losses)

def evaluate(model: nn.Module, data_loader: utils.data.DataLoader, loss_fn):
    model.eval()
    losses = []

    for x, y in data_loader:
        with torch.no_grad():
            loss = loss_fn(model(x), y)
            losses.append(loss.item())

    return sum(losses) / len(losses)