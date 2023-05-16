import random
import time
import numpy as np
import matplotlib.pyplot as plt
import copy

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
class Graph:
    def __init__(self,data):
        self.Vertex=data
        self.n=len(data)  #citysize,数据中结点数量，包括其实点
        self.Edge=self.distlist(data)
        self.edgeNum=len(self.Edge)

    def distance(self,X,Y):
        #利用坐标计算两城市的距离
        r=((X[0]-Y[0])**2+(X[1]-Y[1])**2)**0.5
        return r

    def distlist(self,data):
        tlist={}
        for i in range(self.n):
            for j in range(self.n):
                if i==j:
                    tlist.update({(i,j):0})
                else:
                    tlist.update({(i,j):self.distance(data[i],data[j])})
        return tlist
    
    def find(self,start,findmax=False):
        """
        寻找某结点能够到达的下一个最小或最大距离结点编号。
        :param start: 要寻找的起始城市编号
        :param findmax: 是否寻找最大距离的连接结点
        :return: 与start结点连接的最大/最小路径结点编号
        """
        best = 0
        for i in range(self.n):
            temp = self.Edge[(start, i)]
            if findmax==False:
                if self.Edge[(start, best)] > temp:
                    best = i
            else:
                if self.Edge[(start, best)] < temp:
                    best = i
        return best

    def findNode(self,start,dess,findmax=False):
        """
        在指定关联结点集合中寻找路径最短的目的地。如果des集合中包含start,则先取出start。
        :param start: 结点编号
        :param des: 目标结点编号集合
        :param findmax: 默认最短路
        :return:
        """
        best = copy.copy(dess[0])
        des=copy.copy(dess)
        if start in des:
            des.remove(start)
        for i in range(len(des)):
            temp = self.Edge[(start, des[i])]
            if findmax==False:
                if self.Edge[(start, best)] > temp:
                    best = des[i]
            else:
                if self.Edge[(start, best)] < temp:
                    best = des[i]
        return best

class Solution:
    """
    以Graph类为基础，路径中结点为node。
    """
    def __init__(self,graph):
        self.nodeNum=graph.n   #len(self.route)
        self.Edge=graph.Edge
        self.edgeNum=graph.edgeNum
        self.tabu=self.inittabu()
        self.graph=graph

        self.route=self.greedy()
        self.cost = 0
        self.delta = 0
        self.update()

    def lock(self,i,j,length=20,opposite=True):
        """
        length：交换过后的路径结点对被赋予length的锁定期。
        """
        self.tabu[(i,j)]=length
        if opposite==True:
            self.tabu[(j,i)]=length

    def feasibletabu(self):
        flist=list({k for k,v in self.tabu.items() if v==0})
        ftlist=list()
        for i in range(len(flist)):
            if 0 not in flist[i]:
                ftlist.append(flist[i])
        return ftlist

    def loosetabu(self):
        key=list(self.tabu.keys())
        value=list(self.tabu.values())
        for i in range(len(key)):
            if value[i]>0:
                self.tabu[key[i]]-=1
    
    def inittabu(self):
        tlist={}
        for i in range(self.nodeNum):
            for j in range(self.nodeNum):
                if i==j:
                    tlist.update({(i,j):-1}) #斜对角线元素为-1
                else:
                    tlist.update({(i,j):0})
        return tlist

    def greedy(self):
        """
        初始化方法，贪心法生成初始路径解。
        :return:
        """
        route = [0]
        last=list(range(1,self.nodeNum))
        for i in range(self.nodeNum-1):
            if i==self.nodeNum:
                route.append(last[0])
            else:
                current=self.graph.findNode(i,last) #找到由i出发路径最短的目的地结点。
                route.append(current)
                last.remove(current)
        return route

    def update(self):
        """[summary]
        更新路径solution的状态，计算路径总长。
        Returns:
            [type]: [description]
        """
        if self.cost==0:
            for i in range(self.nodeNum):
                if i < self.nodeNum - 1:
                    self.cost += self.distance(i, i + 1)
                else:
                    self.cost += self.distance(i, 0)
            return self.cost
        else:
            self.cost +=self.delta
            self.delta=0
        self.loosetabu()

    def distance(self,index_i,index_j):
        #计算路径中第i结点和第j结点的距离
        dis=self.Edge[(self.route[index_i],self.route[index_j])]
        return dis

    def randomroute(self):
        """
        利用全部结点生成一条随机路径序列。
        """
        self.route=[0]
        nodes=list(range(1,self.nodeNum))
        for i in range(self.nodeNum):
            s=random.sample(nodes,1)
            nodes.remove(s[0])
            self.route.append(s[0])

    def getIndex(self,node):
        """
        给出结点编号，找出结点在路径序列中的索引号。
        :param node: 结点编号
        :return: route中的索引号
        """
        s=0
        for i in range(self.nodeNum):
            if self.route[i]==node:
                s=i
                break
        return s

    def getNode(self,i):
        s=self.route[i]
        return s

    def selectPair(self):
        """[summary]
        选取路径中的两个结点，在禁忌表允许的范围内随机选取两个结点索引。
        Returns:
            [type]: [description]
        """
        field=self.feasibletabu()
        if len(field)==0:
            return -1,-1
        else:
            s=random.sample(field,1)[0]
        index_i=self.getNode(s[0])
        index_j=self.getNode(s[1])
        return index_i,index_j

    def swap(self,index_i,index_j):
        self.route[index_i],self.route[index_j]=self.route[index_j],self.route[index_i]
        self.lock(self.route[index_i],self.route[index_j])
        self.update()

    def calc_delta(self, i, j):
        """
        计算结点i和j交换后的路径长度差delta。
        :param i: index_i
        :param j: index_j
        :return:
        """
        before_i = i - 1
        after_i = i + 1
        before_j = j - 1
        if j == self.nodeNum - 1:
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

    def print(self):
        for i in range(len(self.route)):
            if i==0:
                print( self.route[i], end="")
            else:
                print("->", self.route[i], end="")
        print("\n the distance is %.4f" % self.cost)

    def routeplot(self):
        for i in range(self.nodeNum):
            if i==self.nodeNum-1:
                break
            else:
                plotpath(self.route[i],self.route[i+1])
        plotpath(self.route[self.nodeNum-1],self.route[0])
        plt.plot(city[0][0],city[0][1],'or')
        plt.show()

def plotpath(start,end):
    """
    绘制路径序列中两个节点间的路径
    :param start:
    :param end:
    :return:
    """
    plt.plot([city[start][0],city[end][0]] ,[ city[start][1],city[end][1] ],'o-',color='b')

#def algorithm():
    #生成初始化路径
max_iteration=4000
graph=Graph(city)
solution=Solution(graph)
solution.update()
solution.print()
start=time.time()
for i in range(max_iteration):
    index_i,index_j=solution.selectPair() #从路径中随机抽取两个元素的索引
    if index_i==-1:
        print("feasible list is empty")
        break
    if index_i>index_j:
        index_i,index_j=index_j,index_i
    if solution.calc_delta(index_i,index_j)<0:
        solution.swap(index_i,index_j)
    print("the %d th iteration"%(i))
    print("swap nodes:",index_i,index_j)
    solution.print()
end=time.time()
duration=end-start
solution.print()
print("time cost is:",duration)
solution.routeplot()

#if __name__=='__main__':
    #main()
#     algorithm()
    