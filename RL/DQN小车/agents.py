import numpy as np
import torch

class q_learn_cient():
    def __init__(self,func,optimizer,n_act,e_greed=0.01,gamma = .9):
        self.criterion = torch.nn.MSELoss()
        self.optimizer = optimizer
        self.func = func
        self.e_greed = e_greed
        self.gamma = gamma
        self.n_act = n_act
    def predict(self,obs):
        q_list = self.func(obs)
        action = int(torch.argmax(q_list).detach().numpy())
        return action
    def act(self,obs):
        if np.random.uniform(0, 1) < self.e_greed:
            action = np.random.choice(self.n_act)
        else:
            action = self.predict(obs)
        return action
    def learn(self,obs,action,reward,next_obs,done):
        cur_Q = self.func(obs)[action]
        if done:
            target_Q = reward
        else:
            target_Q = reward + self.gamma*self.func(next_obs).max()
        loss = self.criterion(target_Q, cur_Q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


