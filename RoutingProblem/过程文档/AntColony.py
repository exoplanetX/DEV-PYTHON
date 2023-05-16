
import random
import time
import matplotlib.pyplot as plt
import copy
from city52 import *



class Ant:
    bestroute=[]
    bestcost=None

    def __init__(self,num):
        self.name=num
        self.route=[]
        self.cost=0
        self.tau=2
        self.elite=False

    def printRoute(self):
        print(self.route[0], end="")
        for i in range(1, len(self.route) - 1):
            if i%26==0:
                print("->", self.route[i], end="\n")
            else:
                print("->", self.route[i], end="")
        print("->", self.route[0])
        print("the distance is %.4f" % self.cost)


    def refresh(self):
        self.tau=2
def search(ant):


Swarm=500 #种群数量
rho=0.3 #挥发率
max_iteration=200
colony=[Ant(i) for i in range(Swarm)]
for iter in range(max_iteration):
    for ant in colony:
