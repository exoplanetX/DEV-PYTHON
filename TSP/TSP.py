from gurobipy import*
import re
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
from matplotlib.lines import lineStyles
import time

starttime=time.time()

def readData(path,nodeNum):
    nodeNum=nodeNum
    cor_X=[]
    cor_Y=[]
    f=open(path,'r')
    lines=f.readlines()
    count=0
    for line in lines:
        count+=1
        if(count>=10 and count<=10+nodeNum):
            line=line[:-1]
            str=re.split(r" +",line)
            cor_X.append(float(str[2]))
            cor_Y.append(float(str[3]))

    disMatrix=[([0]*nodeNum) for p in range(nodeNum)]
    for i in range(0,nodeNum):
        for j in range(0,nodeNum):
            temp=(cor_X[i]-cor_X[j])**2+(cor_Y[i]-cor_Y[j])**2
            disMatrix[i][j]=(int)(math.sqrt(temp))
            temp=0
    return disMatrix
def printData(disMatrix):
    print("-------cost matrix---------\n")
    for i in range(len(disMatrix)):
        for j in range(len(disMatrix)):
            print("%6.1f"%(disMatrix[i][j]),end=" ")
        print()

def reportMIP(model,Routes):
    if model.status==GRB.OPTIMAL:
        print("Best MIP Solution:",model.objVal,"\n")
        var=model.getVars()
        for i in range(model.numVars):
            if(var[i].x>0):
                print(var[i].varName,"=",var[i].x)
                print("Optimal route:",Routes[i])

def getValue(var_dict,nodeNum):
    x_value=np.zeros([nodeNum+1,nodeNum+1])
    for key in var_dict.keys():
        a=key[0]
        b=key[1]
        x_value[a][b]=var_dict[key].x
        return x_value

def getRoute(x_value):
    x=copy.deepcopy(x_value)
    previousPoint=0
    arcs=[]
    route_temp=[previousPoint]
    count=0
    while(len(route_temp)<len(x) and count<len(x)):
        print('previousPoint:',previousPoint,'count:',count)
        if(x[previousPoint][count]>0):
            previousPoint=count
            route_temp.append(previousPoint)
            count=0
            continue
        else:
            count+=1
    return route_temp

# callback
def subtourelim(model,where):
    if(where==GRB.Callback.MIPSOL):
        print('model._vars',model._vars)
        x_value=np.zeros([nodeNum+1,nodeNum+1])
        for m in model.getVars():
            if(m.varName.startswith('x')):
                a=(int)(m.varName.split('_')[1])
                b=(int)(m.varName.split('_')[2])
                x_value[a][b]=model.cbGetSolution(m)
        print("solution=",x_value)
        tour=subtour(x_value)
        print('tour=',tour)
        if(len(tour)<nodeNum+1):
            print("---add sub tour elimination constraint---")
            for i,j in itertools.combinations(tour,2):
                print(i,j)
            model.cbLazy(quicksum(model._vars[i,j]
                                  for i,j in itertools.combinations(tour,2)) <=len(tour)-1)
            LinExpr=quicksum(model._vars[i,j] for i,j in itertools.combinations(tour,2))
            print('LinExpr=',LinExpr)
            print('RHS=',len(tour)-1)

def computeDegree(graph):
    degree=np.zeros(len(graph))
    for i in range(len(graph)):
        for j in range(len(graph)):
            if(graph[i][j]>0.5):
                degree[i]=degree[i]+1
                degree[j]=degree[j]+1
    print('degree',degree)
    return degree

def findEdges(graph):
    edges=[]
    for i in range(1,len(graph)):
        for j in range(1,len(graph)):
            if(graph[i][j]>0.5):
                edges.append((i,j))
    return edges

def subtour(graph):
    degree=computeDegree(graph)
    unvisited=[]
    for i in range(1,len(degree)):
        if(degree[i]>=2):
            unvisited.append(i)
    cycle=range(0,nodeNum+1)
    edges=findEdges(graph)
    edges=tuplelist(edges)
    print(edges)
    while unvisited:
        thiscycle=[]
        neighbors=unvisited
        while neighbors:
            current=neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors=[j for i,j in edges.select(current,'*') if j in unvisited]
            neighbors2=[i for i,j in edges.select('*',current) if i in unvisited]
            if(neighbors2):
                neighbors.extend(neighbors2)
        isLink=((thiscycle[0],thiscycle[-1]) in edges) or ((thiscycle[-1],thiscycle[0]) in edges)
        if(len(cycle)>len(thiscycle) and len(thiscycle)>=3 and isLink):
            cycle=thiscycle
            return cycle
    return cycle

nodeNum=10
path='solomon-100/in/c201.txt'
cost=readData(path,nodeNum)
printData(cost)

model=Model('TSP')
# create decision variables
X={}
mu={}
for i in range(nodeNum+1):
    mu[i]=model.addVar(lb=0.0,
                       ub=100,
                       vtype=GRB.CONTINUOUS,
                       name="mu_"+str(i))
    for j in range(nodeNum+1):
        if(i!=j):
            X[i,j]=model.addVar(vtype=GRB.BINARY,name='x_'+str(i)+'_'+str(j))
#set objective function
obj=LinExpr(0)
for key in X.keys():
    i=key[0]
    j=key[1]
    if(i<nodeNum and j< nodeNum):
        obj.addTerms(cost[key[0]][key[1]],X[key])
    elif(i==nodeNum):
        obj.addTerms(cost[0][key[1]],X[key])
    elif(j==nodeNum):
        obj.addTerms(cost[key[0]][0],X[key])

model.setObjective(obj,GRB.MINIMIZE)
# add constraints 1
for j in range(1,nodeNum+1):
    lhs=LinExpr(0)
    for i in range(0,nodeNum):
        if(i!=j):
            lhs.addTerms(1,X[i,j])
    model.addConstr(lhs==1,name='visit_'+str(j))
# add constraints 2
for i in range(0,nodeNum):
    lhs=LinExpr(0)
    for j in range(1,nodeNum+1):
        if(i!=j):
            lhs.addTerms(1,X[i,j])
    model.addConstr(lhs==1,name='visit_'+str(j))

# set lazy constraints
model._vars=X
model.Params.lazyConstraints=1
model.optimize(subtourelim)
x_value=getValue(X,nodeNum)
