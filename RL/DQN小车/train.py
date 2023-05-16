import torch
from agents import q_learn_cient
from mlp_model import MLP
import gym


class Trainmodule():
    def __init__(self,env,eposides = 500,e_greed = .1,lr = .01,gamma = .9):
        self.env = env
        self.eposides = eposides
        obs = 4
        n_act = 2
        self.func = MLP(obs,n_act)
        optimizer = torch.optim.AdamW(self.func.parameters(),lr=lr)
        self.agent = q_learn_cient(self.func,optimizer,n_act,e_greed =e_greed,gamma=gamma)

    def train_eposide(self):
        total_reward = 0
        obs = self.env.reset()[0]
        obs = torch.FloatTensor(obs)
        while True:
            action = self.agent.act(obs)
            next_obs, reward, done, info, _ = self.env.step(action)
            if done:
                break
            next_obs = torch.FloatTensor(next_obs)
            self.agent.learn(obs, action, reward, next_obs, done)
            obs = next_obs
            total_reward += reward
            self.env.render()
        return total_reward
    def ts_eposide(self):
        total_reward = 0
        obs = self.env.reset()
        obs = torch.FloatTensor(obs)
        while True:
            action = self.agent.predict(obs)
            next_obs, reward, done, info, _ = self.env.step(action)
            next_obs = torch.FloatTensor(next_obs)
            obs = next_obs
            total_reward += reward
            if done:
                break
        return total_reward

    def train(self):
        for i in range(self.eposides):
            ep_reward = self.train_eposide()
            print(f'train_reward:{ep_reward}')
    # ts_reward = ts_eposide(env,agent)
    # print(f'test_reward:{ts_reward}')

if __name__ == '__main__':
    env1 = gym.make("CartPole-v1", render_mode="human")
    tm = Trainmodule(env1)
    tm.train()
