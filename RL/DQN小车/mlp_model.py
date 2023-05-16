import numpy as np
import torch
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self,opt_n,act_n):
        super(MLP, self).__init__()
        self.f1 = nn.Sequential(
            nn.Linear(opt_n,50),
            nn.ReLU(),
            nn.Linear(50, 50),
            nn.ReLU(),
            nn.Linear(50, act_n)
        )
    def forward(self,x):
        x = self.f1(x)
        return x

