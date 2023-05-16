#Cutting Stock Problem
#Column generation method
from gurobipy import *
from random import randint
from math import floor
#不同宽度产品数量
k=50
#基础材料数量
L=750
#每一个产品的长度或者宽度
l={i:randint(10,floor(L/3)) for i in range(k)}
#每个产品的需求
d={i:randint(5,200) for i in range(k)}
#----Pricing Model-----
PP=Model("Pricing Problem")
Pvars=PP.addVars(k,obj=-1,vtype=GRB.INTEGER,name='w')
PP.addConstr(Pvars.prod(l)<=L)
PP.update()

#----Master Model-----
M=Model('Master Problem')
s=M.addVars(k,name='slack',obj=1000)
c=M.addConstrs(s[i]>=d[i] for i in range(k))
M.write('initial.lp')
M.optimize()

#---Adding a set of initial variables---
PP.Params.OutputFlag=0
for i in range(k):
    obj={i:-1 for i in range(k)}
    obj[i]=-L-1
    PP.setObjective(Pvars.prod(obj))
    PP.optimize()
    col=Column()
    for j in range(k):
        col.addTerms(Pvars[j].x,c[j])
    M.addVar(obj=1,column=col)
M.optimize()
M.write('base.lp')

#----
M.Params.OutputFlag=0
Iter=0
while M.Status==GRB.OPTIMAL:
    pi={i:-c[i].pi for i in range(k)}
    PP.setObjective(Pvars.prod(pi))
    PP.optimize()
    if PP.Status!=GRB.OPTIMAL:
        raise('Unexpected optimization status')
    if PP.ObjVal> -1.0001:
        break
    if Iter % 20 ==0:
        print('Iteration MasterValue Pricing Value')
    print('%8d %12.5g %12.5g' % (Iter,M.ObjVal,PP.ObjVal))
    Iter+=1

    col=Column()
    for j in range(k):
        col.addTerms(Pvars[j].x,c[j])
    M.addVar(obj=1,column=col)
    M.optimize()
M.write('final.lp')
rootbound=M.ObjVal

#-----
M.Params.OutputFlag=1
Mvars=M.getVars()
for v in Mvars:
    v.vtype=GRB.INTEGER
M.optimize()
print('Proven column generation gap %.3f%%' % (100*(M.ObjVal-rootbound)/M.ObjVal))
