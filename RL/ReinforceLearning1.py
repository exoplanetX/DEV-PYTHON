import random
import torch
import torch.nn as nn
import numpy as np
import gym

class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(4, 24),
            nn.ReLU(),
            nn.Linear(24, 24),
            nn.ReLU(),
            nn.Linear(24, 2)
        )
        self.mls = nn.MSELoss()
        self.opt = torch.optim.Adam(self.parameters(), lr = 0.001)

    def forward(self, inputs):
        return self.fc(inputs)


env = gym.envs.make('CartPole-v1')
env = env.unwrapped
net = Network()  # 学习的网络
net2 = Network()  # 延迟的网络

memory_count = 0  # 经验池中已经遇到的情况
memory_size = 2000  # 记忆库大小
epsilon = 0.5  # 贪婪系数
gama = 0.9  # 时间折扣
b_size = 500  # batch size每次从记忆库中提取的数据
learn_time = 0
update_time = 10  # 每10步更新一次网络
memory = np.zeros((memory_size, 10))  # s=4,a=1,s=4,r=1,
start_study = False
for i in range(50000):
    s = env.reset()
    while True:
        if random.randint(0,100) < 100*(epsilon**learn_time):
            a = random.randint(0,1)
        else:
            totalreward = net(torch.Tensor(s))
            a = torch.argmax(totalreward).data.item()
        s_, r, done, info = env.step(a)
        r = ( env.theta_threshold_radians - abs(s_[2]) ) / env.theta_threshold_radians * 0.7  +  ( env.x_threshold - abs(s_[0]) ) / env.x_threshold * 0.3  # (杆子角度为0最好，在中间也很好，比例定为7/3)
        memory[memory_count % memory_size][0:4] = s
        memory[memory_count % memory_size][4:5] = a
        memory[memory_count % memory_size][5:9] = s_
        memory[memory_count % memory_size][9:10] = r
        memory_count += 1
        s = s_

        if memory_count > memory_size:

            if learn_time % update_time == 0:
                net2.load_state_dict(net.state_dict())  # 延迟更新

            index = random.randint(0, memory_size - b_size -1)
            b_s  = torch.Tensor(store[index:index + b_size, 0:4])
            b_a  = torch.Tensor(store[index:index + b_size, 4:5]).long()
            b_s_ = torch.Tensor(store[index:index + b_size, 5:9])
            b_r  = torch.Tensor(store[index:index + b_size, 9:10])

            q = net(b_s).gather(1, b_a)
            q_next = net2(b_s_).detach().max(1)[0].reshape(b_size, 1)
            tq = b_r + gama * q_next
            loss = net.mls(q, tq) # 让总收益等于下一步收益加之后的收益
            net.opt.zero_grad()
            loss.backward()
            net.opt.step()

            learn_time += 1
            if not start_study:
                print('start study')
                start_study = True
                break
        if done:
            break

        env.render()