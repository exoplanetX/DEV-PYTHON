"""
@author: xuning

"""
import random
import time
import math
import numpy as np
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
	];
city_size=len(city)

class Solution:
    def __init__(self,data):
        self.route=initialize(data)
        self.cost = total_distance(self.route)

    def print(self):
        print(self.route[0], end="")
        for i in range(1, len(self.route) - 1):
            print("->", self.route[i], end="")
        print("->", self.route[0])
        print("the distance is %.4f" % self.cost)

    def update(self):
        self.cost=total_distance(self.route)


def distance(X,Y):
    r=((X[0]-Y[0])**2+(X[1]-Y[1])**2)**0.5
    return r

def initialize(city):
    r=list(range(1,len(city)))
    random.shuffle(r)
    solution=[0]+r
    return solution

def total_distance(solution):
    total=0
    for i in range(len(solution)):
        if i<len(solution)-1:
            total+=distance(city[solution[i]],city[solution[i+1]])
        else:
            total+=distance(city[solution[i]],city[solution[0]])
    return total

def print_route(solution):
    print(solution[0],end="")
    for i in range(1,len(solution)-1):
        print("->",solution[i],end="")
    print("->",solution[0])
    print("the total distance is %.4f"%total_distance(solution))

def two_opt_operator(solution,index_i,index_j):
    solution[index_i],solution[index_j]=solution[index_j],solution[index_i]
    return solution

def calc_delta(solution,index_i,index_j):
    before_i = index_i - 1
    after_i=index_i+1
    before_j=index_j-1
    if index_j==city_size-1:
        after_j = 0
    else:
        after_j = index_j + 1
    if index_i+1==index_j:
        delta=-distance(city[solution[before_i]],city[solution[index_i]])\
              -distance(city[solution[after_j]],city[solution[index_j]])\
              +distance(city[solution[before_i]],city[solution[index_j]])\
              +distance(city[solution[after_j]],city[solution[index_i]])

    else:
        delta=-distance(city[solution[before_i]],city[solution[index_i]])\
              -distance(city[solution[after_i]],city[solution[index_i]])\
              +distance(city[solution[before_i]],city[solution[index_j]])\
              +distance(city[solution[after_i]],city[solution[index_j]])\
              -distance(city[solution[before_j]],city[solution[index_j]])\
              -distance(city[solution[after_j]],city[solution[index_j]])\
              +distance(city[solution[before_j]],city[solution[index_i]])\
              +distance(city[solution[after_j]],city[solution[index_i]])
    return delta



#生成初始化路径
max_iteration=500
#current_route=initialize(city)
current_route=Solution(city)
#total=total_distance(current_route)
order_list=range(1,city_size-1) #路径顺序索引
for i in range(max_iteration):
    index_i,index_j=random.sample(order_list,2)
    if index_i>index_j:
        index_i,index_j=index_j,index_i
    delta = calc_delta(current_route.route, index_i, index_j)

    if delta<0:
        current_route.route=two_opt_operator(current_route.route,index_i,index_j)
        current_route.update()
        #total+=delta
    #print("selected index are: %d,%d"%(index_i,index_j))
    print("the %d th iteration"%(i))
    current_route.print()






