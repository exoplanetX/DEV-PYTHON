"""
@author: xuning

"""
import random
import time
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
#citysize=len(city)
def check(solution):
    target=list(range(solution.atlas.citysize))
    test=copy.copy(solution.route)
    test.sort()
    indicator= target==test
    return indicator

class Tuplelist:
    def __init__(self,data):
        self.data=data
        self.citysize=len(data)
        self.citylist=list(range(len(self.data)))
        self.dict=self.initDist(data) # dict of all paths
        self.pathsize=len(self.dict) #routesize ->pathsize
        self.tabu=self.initTabu()

    def initDist(self,data):
        tlist={}
        for i in range(self.citysize):
            for j in range(self.citysize):
                if i==j:
                    tlist.update({(i,j):0})
                else:
                    tlist.update({(i,j):self.distance(data[i],data[j])})
        return tlist

    def initTabu(self):
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

    def getDistance(self,start,end):
        return self.dict[(start,end)]

    def getNextnode(self,start,flist,findmax=False):
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

    def feasibletabu(self,start=True):
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

def greedy(atlas):
    route=[0]
    flist=list(range(len(atlas.data)))
    flist.remove(0)
    start=0
    while len(flist)>0:
        end=atlas.getNextnode(start, flist)
        route.append(end)
        flist.remove(end)
        start=end
    return route

class Solution:
    def __init__(self,atlas):
        self.atlas=atlas
        self.unused = []
        self.route=greedy(atlas)
        self.size=len(self.route)
        self.index=range(1,self.size-1)
        self.cost = self.calcCost()
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

    def calcCost(self):
        cost=0
        for i in range(self.size):
            if i < self.size - 1:
                cost += self.distance(i, i + 1)
            else:
                cost += self.distance(i, 0)
        self.cost=cost

    def distance(self,index_i,index_j):
        #计算路径中第i结点和第j结点的距离
        #dis=self.atlas.dict[(self.route[index_i],self.route[index_j])]
        dis=self.atlas.getDistance(self.route[index_i],self.route[index_j])
        return dis

    def findIndex(self,node):
        #给出城市（结点）编号，转换为路径中的索引值。
        s=None
        for i in range(self.size):
            if self.route[i]==node:
                s=i
                break
        return s

    def findCity(self,index):
        #给出路径中索引，转换为城市（结点）编号
        s=0
        if index==52:
            index=0
        for i in range(self.atlas.citysize):
            if self.route[index]==i:
                s=i
                break
        return s

    def selectRand(self):
        #挑出符合tabu限制的两个待交换结点索引
        field=self.atlas.feasibletabu()
        if len(field)==0:  #如果禁忌表的可行结点为空
            return -1,-1
        else:
            s=random.sample(range(len(field)),1)[0]
        temp=list(field[s])
        i=self.findIndex(temp[0])
        j=self.findIndex(temp[1])
        #index_j=self.findIndex(field[s][1])
        return i,j

    # def swap(self,index_i,index_j):
    #     #交换路径中第index_i和index_j的城市，交换后两者锁定进入tabu表
    #     self.route[index_i],self.route[index_j]=self.route[index_j],self.route[index_i]
    #     route_list.lock(self.route[index_i],self.route[index_j])

    def cutNode(self,index):
        # self.delta=self.distance(index-1,index+1)\
        #            -self.distance(index-1,index)-self.distance(index,index-1)
        temp=self.route[index]
        self.route.remove(temp)
        self.size-=1
        self.unused.append(temp)

    def insertNode(self,index):
        #将unused队列中的空闲元素插入到路径route队列的index位置
        if index==self.size-1: #如果插入位置index是队尾
            #self.delta =-self.distance(index,0)+self.atlas.getDistance(self.route[index],self.unused[0])+self.atlas.dict[(self.unused[0],0)]
            self.route.append(self.unused[0])
        else: #如果index位置非队尾
            # self.delta=-self.distance(index-1,index)\
            #            +self.atlas.dict[(self.route[index-1],self.unused[0])]\
            #            +self.atlas.dict[(self.unused[0],self.route[index])]
            self.route.insert(index,self.unused[0])
        self.size+=1
        self.unused.remove(self.unused[0])

    def calcDelta(self, ifrom, jto):
        """
        :param i: index_i selected
        :param j: index_j target position
        """
        before_ifrom = ifrom - 1
        if ifrom==self.size:
            after_ifrom=0
        else:
            after_ifrom = ifrom + 1
        before_jto = jto - 1
        if jto == self.size - 1:
            after_jto = 0
        else:
            after_jto = jto + 1
        if ifrom + 1 == jto or jto+1==i:
            delta = -self.distance(before_ifrom,ifrom)-self.distance(jto,after_jto)-self.distance(ifrom,jto)\
                    +self.distance(before_ifrom,jto)+self.distance(ifrom,after_jto)+self.distance(jto,ifrom)
        else:
            delta = -self.distance(before_ifrom,ifrom)-self.distance(ifrom,after_ifrom)\
                    +self.distance(before_ifrom,after_ifrom)\
                    -self.distance(before_jto,jto)\
                    +self.distance(before_jto,ifrom)+self.distance(ifrom,jto)
        self.delta=delta
        return delta

    def plotRoute(self):
        for i in range(self.size):
            if i==self.size-1:
                plt.plot([city[self.route[i]][0],city[0][0]],[city[self.route[i]][1],city[0][1]],'o-',color='b')
            else:
                plt.plot([city[self.route[i]][0],city[self.route[i+1]][0]],[city[self.route[i]][1],city[self.route[i+1]][1]],'o-',color='b')

        plt.plot(city[0][0],city[0][1],'or')
        plt.show()

#算法主体
max_iteration=4000
data=Tuplelist(city)
solution=Solution(data)
solution.calcCost()
initialroute=copy.copy(solution.route)
print("initial cost is ",solution.cost)
start=time.time()
for i in range(max_iteration):
    index_i,index_j=solution.selectRand()
    if index_i==-1:
        print("feasible list is empty")
        break
    if index_i>index_j:
        index_i,index_j=index_j,index_i
    if solution.calcDelta(index_i,index_j)<0:
        #print("delta is ",solution.delta)
        solution.cutNode(index_i)
        solution.insertNode(index_j)
        solution.atlas.lock(solution.route[index_i],solution.route[index_j])
        solution.atlas.loosetabu()
        #print("the %d th iteration,city %d to %d"%(i,solution.route[index_i],solution.route[index_j]))
solution.calcCost()
end=time.time()
duration=end-start
solution.print()
print("time cost is:",duration)
solution.plotRoute()






