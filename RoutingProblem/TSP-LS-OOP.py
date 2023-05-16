"""
@author: xuning

"""
import random
import time
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

def distance(X,Y):
    r=((X[0]-Y[0])**2+(X[1]-Y[1])**2)**0.5
    return r

def tuplelist(data):
    tlist={}
    for i in range(city_size):
        for j in range(city_size):
            if i==j:
                tlist.update({(i,j):0})
            else:
                tlist.update({(i,j):distance(data[i],data[j])})
    return tlist

def initialize(data):
    r=list(range(1,len(data)))
    random.shuffle(r)
    route=[0]+r
    return route

class Solution:
    def __init__(self,data):
        self.route=initialize(data)
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

    def distance(self,i,j):
        dis=route_list[(self.route[i],self.route[j])]
        return dis

    def swap(self,i,j):
        self.route[i],self.route[j]=self.route[j],self.route[i]

    def calc_delta(self, i, j):
        before_i = i - 1
        after_i = i + 1
        before_j = j - 1
        if index_j == city_size - 1:
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
        for i in range(city_size):
            #plt.scatter(city[self.route[i]][0],city[self.route[i]][1])
            if i==city_size-1:
                plt.plot([city[self.route[i]][0],city[0][0]],[city[self.route[i]][1],city[0][1]],'o-',color='b')
            else:
                plt.plot([city[self.route[i]][0],city[self.route[i+1]][0]],[city[self.route[i]][1],city[self.route[i+1]][1]],'o-',color='b')
        plt.plot(city[0][0],city[0][1],'or')
        plt.show()


#生成初始化路径
max_iteration=4000
route_list=tuplelist(city)
current_route=Solution(city)
current_route.update()
order_list=range(1,city_size-1) #路径顺序索引
start=time.time()
for i in range(max_iteration):
    index_i,index_j=random.sample(order_list,2)
    if index_i>index_j:
        index_i,index_j=index_j,index_i
    #delta=current_route.calc_delta(index_i,index_j)
    if current_route.calc_delta(index_i,index_j)<0:
        current_route.swap(index_i,index_j)
        current_route.update()
    print("the %d th iteration"%(i))
end=time.time()
duration=end-start
current_route.print()
print("time cost is:",duration)
current_route.routeplot()






