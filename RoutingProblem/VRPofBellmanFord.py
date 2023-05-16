from city52 import *
from TSPtabu import *
import random
import time
import matplotlib.pyplot as plt
import copy

def check(route,citysize):
    indicator=True
    target=range(citysize)
    label=[0]*citysize
    for i in target:
        for j in range(len(route)):
            if i==route[j] and label[i]==0:
                label[i]=1
            else:
                label[i]=0
    if 0 in label:
        indicator=False
        print("Duplicate node in route")
    print("label sequence:",label)
    return indicator

class Tuplelist:
    def __init__(self,data):
        self.citysize=len(data)
        self.dict=self.distlist(data)
        self.citylist=list(range(self.citysize))
        self.routesize=len(self.dict)
        self.tabu=self.inittabu()


    def find(self,start,flist,findmax=False):
        #找到从start结点出发的最近路程结点
        best = flist[0]
        temp=self.dict[(start,flist[0])]

        for i in flist:
            if findmax==False:
                if self.dict[(start, i)] > temp :
                    best = i
            else:
                if self.dict[(start, i)] < temp :
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
        if 0 in flist:
            flist.remove(0)
        return flist

    def loosetabu(self):
        key=list(self.tabu.keys())
        value=list(self.tabu.values())
        for i in range(len(key)):
            if value[i]>0:
                self.tabu[key[i]]-=1

    def distlist(self,data):
        tlist={}
        for i in range(self.citysize):
            for j in range(self.citysize):
                if i==j:
                    tlist.update({(i,j):0})
                else:
                    tlist.update({(i,j):self.distance(data[i],data[j])})
        return tlist

    def inittabu(self):
        #初始化tabu属性，生成self.tabu字典类型
        tlist={}
        for i in range(self.citysize):
            for j in range(self.citysize):
                if i==0:
                    tlist.update({(i,j):-1})
                elif i==j:
                    tlist.update({(i,j):-1})
                elif j==0:
                    tlist.update({(i, j): -1})
                else:
                    tlist.update({(i,j):0})
        return tlist

def greedy(route_list):
    route=[0]
    flist=route_list.citylist
    flist.remove(0)
    # table=list(enumerate(route_list.label))
    # flist=[a for a,b in table if b==0]
    #for i in range(route_list.citysize-1):
    start=0
    while len(flist)>0:
        end=route_list.find(start, flist)
        route.append(end)
        # print(end)
        # print(flist)
        flist.remove(end)
        start=end

    return route

class Solution:
    def __init__(self,route_list):
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
            for i in range(self.size):
                if i < self.size - 1:
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
        #给出城市（结点）编号，转换为路径中的索引值。
        s=0
        for i in range(self.size):
            if self.route[i]==node:
                s=i
                break
        return s

    def select(self):
        #挑出符合tabu限制的两个待交换结点索引
        field=route_list.feasibletabu()
        if len(field)==0:
            return -1,-1
        else:
            s=random.sample(range(len(field)),1)[0]
        index_i=self.findindex(field[s][0])
        index_j=self.findindex(field[s][1])
        return index_i,index_j

    def swap(self,index_i,index_j):
        #交换路径中第index_i和index_j的城市，交换后两者锁定进入tabu表
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
        if j == self.size - 1:
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


def BellmanFord(route_list):

def BellmanMap(current_route):
    tlist={}
    n=current_route.size
    for(i in range(n)):
        for(j in range(i,n)):
            if i==0:
                tlist.update({(0,j): (route_list.dict[(0,current_route.route[j])]+route_list.dict[(current_route.route[j],0)])})
            else:
                tlist.update({(i,j): route_list.dict[(0,current_route.route[j])]\
                                        +route_list.dict[(current_route.route[i],current_route.route[j])]\
                                        +route_list.dict[(current_route.route[j],0)]})






if __name__ == '__main__':
    max_iteration = 4000
    route_list = Tuplelist(city)
    current_route = Solution(route_list)
    current_route.update()
    check(current_route.route, len(city))
    main()


