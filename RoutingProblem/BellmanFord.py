"""
@author: xuning
TSP部分继承自TSP-test-OOP-v3.py
"""
import random
import time
import numpy as np
import matplotlib.pyplot as plt

city = [
[ 565,575 ],[ 25,185 ],[ 345,750 ],[ 945,685 ],[ 845,655 ],
[ 880,660 ],[ 25,230 ],[ 525,1000 ],[ 580,1175 ],[ 650,1130 ],
[ 1605,620 ],[ 1220,580 ],[ 1465,200 ],[ 1530,5 ],
[ 845,680 ],[ 725,370 ],[ 145,665 ],
[ 415,635 ],[ 510,875 ],[ 560,365 ],[ 300,465 ],[ 520,585 ],[ 480,415 ],
[ 835,625 ],[ 975,580 ],[ 1215,245 ],[ 1320,315 ],[ 1250,400 ],[ 660,180 ],
[ 410,250 ],[ 420,555 ],[ 575,665 ],[ 1150,1160 ],[ 700,580 ],[ 685,595 ],
[ 685,610 ],[ 770,610 ],[ 795,645 ],[ 720,635 ],[ 760,650 ],[ 475,960 ],
[ 95,260 ],[ 875,920 ],[ 700,500 ],[ 555,815 ],[ 830,485 ],[ 1170,65 ],
[ 830,610 ],[ 605,625 ],[ 595,360 ],[ 1340,725 ],[ 1740,245 ]
	]
city_size=len(city)

class Tuplelist:
    def __init__(self,data):
        self.dict=self.distlist(data)
        self.citysize=len(data)
        self.routesize=len(self.dict)
        self.tabu=self.inittabu()

    def find(self,start,findmax=False):
        best = 0
        for i in range(city_size):
            temp = self.dict[(start, i)]
            if findmax==False:
                if self.dict[(start, best)] > temp:
                    best = i
            else:
                if self.dict[(start, best)] < temp:
                    best = i
        return best

    def distance(self,X,Y):
        #利用坐标计算两城市的距离
        r=((X[0]-Y[0])**2+(X[1]-Y[1])**2)**0.5
        return r

    def lock(self,i,j,length=15,opposite=True):
        self.tabu[(i,j)]=length
        if opposite==True:
            self.tabu[(j,i)]=length

    def feasibletabu(self):
        flist=list({k for k,v in self.tabu.items() if v==0})
        return flist

    def loosetabu(self):
        key=list(self.tabu.keys())
        value=list(self.tabu.values())
        for i in range(len(key)):
            if value[i]>0:
                self.tabu[key[i]]-=1

    def distlist(self,data):
        tlist={}
        for i in range(city_size):
            for j in range(city_size):
                if i==j:
                    tlist.update({(i,j):0})
                else:
                    tlist.update({(i,j):self.distance(data[i],data[j])})
        return tlist

    def inittabu(self):
        tlist={}
        for i in range(city_size):
            for j in range(city_size):
                if i==j:
                    tlist.update({(i,j):-1})
                else:
                    tlist.update({(i,j):0})
        return tlist


def greedy(route_list):
    route=[]
    for i in range(city_size):
        route.append(route_list.find(i))
    #route.append([0])
    return route


class Solution:
    def __init__(self,route_list):
        #self.route=initialize(data)
        self.route=greedy(route_list)
        self.size=len(self.route)
        self.cost = 0
        self.delta = 0

    def print(self):
        print(self.route[0], end="")
        for i in range(1, len(self.route) - 1):
            if i%26==0:
                print("->", self.route[i], end="\n")
            else:
                print("->", self.route[i], end="")
        print("->", self.route[0])
        print("the distance is %.4f" % self.cost)

    def update(self):
        if self.cost==0:
            for i in range(city_size):
                if i < city_size - 1:
                    self.cost += self.distance(i, i + 1)
                else:
                    self.cost += self.distance(i, 0)
            return self.cost
        else:
            self.cost +=self.delta
            self.delta=0
        route_list.loosetabu()

    def distance(self,index_i,index_j):
        #计算路径中第i结点和第j结点的距离
        dis=route_list.dict[(self.route[index_i],self.route[index_j])]
        return dis

    def findindex(self,node):
        s=0
        for i in range(self.size):
            if self.route[i]==node:
                s=i
                break
        return s

    def select(self):
        field=route_list.feasibletabu()
        if len(field)==0:
            return -1,-1
        else:
            s=random.sample(range(len(field)),1)[0]
        index_i=self.findindex(field[s][0])
        index_j=self.findindex(field[s][1])
        return index_i,index_j

    def swap(self,index_i,index_j):
        self.route[index_i],self.route[index_j]=self.route[index_j],self.route[index_i]
        route_list.lock(self.route[index_i],self.route[index_j])

    def calc_delta(self, i, j):
        """
        :param i: index_i
        :param j: index_j
        :return:
        """
        before_i = i - 1
        after_i = i + 1
        before_j = j - 1
        if j == city_size - 1:
            after_j = 0
        else:
            after_j = j + 1
        if i + 1 == j:
            delta = -self.distance(before_i,i)-self.distance(j,after_j)-self.distance(i,j)\
                    +self.distance(before_i,j)+self.distance(i,after_j)+self.distance(j,i)
        else:
            delta = -self.distance(before_i,i)-self.distance(i,after_i)\
                    +self.distance(before_i,j)+self.distance(j,after_i)\
                    -self.distance(before_j,j)-self.distance(j,after_j)\
                    +self.distance(before_j,i)+self.distance(i,after_j)
        self.delta=delta
        return delta

    def routeplot(self):
        for i in range(self.size):
            if i==self.size-1:
                plt.plot([city[self.route[i]][0],city[0][0]],[city[self.route[i]][1],city[0][1]],'o-',color='b')
            else:
                plt.plot([city[self.route[i]][0],city[self.route[i+1]][0]],[city[self.route[i]][1],city[self.route[i+1]][1]],'o-',color='b')

        plt.plot(city[0][0],city[0][1],'or')
        plt.show()

#生成初始化路径
max_iteration=4000
route_list=Tuplelist(city)
current_route=Solution(route_list)
current_route.update()
#order_list=range(1,route_list.citysize-1) #路径顺序索引
start=time.time()
for i in range(max_iteration):
    (index_i,index_j)=current_route.select()
    if index_i==-1:
        print("feasible list is empty")
        break
    if index_i>index_j:
        index_i,index_j=index_j,index_i
    if current_route.calc_delta(index_i,index_j)<0:
        current_route.swap(index_i,index_j)
        current_route.update()
    #print("the %d th iteration"%(i))
end=time.time()
duration=end-start
current_route.print()
print("time cost is:",duration)
current_route.routeplot()

#计算子路径，bellman-ford算法
#生成BMlist距离矩阵
n=len(current_route.route)
bmlist=np.zeros((n,n))
for i in range(n):
    for j in np.arange(i+1,n):
        if i==0:
            bmlist[0,j]=current_route.distance(0,j)+current_route.distance(j,0)
        else:
            s=i
            while s<j:
                bmlist[i,j]+=current_route.distance(s,s+1)
                s=s+1
            bmlist[i, j]+=current_route.distance(0,i)+current_route.distance(j,0)

#执行bellman-ford算法

