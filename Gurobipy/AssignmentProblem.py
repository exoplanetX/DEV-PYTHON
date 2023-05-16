import pandas as pd
import numpy as np
import random
from gurobipy import *

order_num=20
profit_matrix=np.zeros((order_num,order_num))
for i in range(order_num):
    for j in range(order_num):
        profit_matrix[i][j]=0
    else:
        random.seed(i*order_num+j)
        profit_matrix[i][j]=round(10*random.random(),1)
profit_matrix
p=pd.DataFrame(profit_matrix)
p

model=Model('Assignment_Problem')

x=[[[] for i in range(order_num)] for j in range(order_num)]
for i in range(order_num):
    for j in range(order_num):
        x[i][j]=model.addVar(lb=0, ub=1, vtype=GRB.CONTINUOUS,
                             name="x_"+str(i)+"_"+str(j))
# objective function
obj=LinExpr(0)
for i in range(order_num):
    for j in range(order_num):
        obj.addTerms(profit_matrix[i][j],x[i][j])
model.setObjective(obj,GRB.MAXIMIZE)
#constraint 1
for j in range(order_num):
    expr=LinExpr(0)
    for i in range(order_num):
        expr.addTerms(1,x[i][j])
    model.addConstr(expr==1,name="D_"+str(i))

#constraint 2
for i in range(order_num):
    expr=LinExpr(0)
    for j in range(order_num):
        expr.addTerms(1,x[i][j])
    model.addConstr(expr==1,name="R_"+str(i))

#solve the constructed model
model.write("model.lp")
model.optimize()

for var in model.getVars():
    if(var.x>0):
        print(var.varName,'\t',var.x)
        