from gurobipy import *
import numpy as np
scenario_num=5
sto_model=Model('Stochastic Programming')
prob=[0.2,0.2,0.2,0.2,0.2]

profit=[2,3]
b=[8,16,12]

a_11=np.random.normal(1,0.2,scenario_num)
a_12=np.random.normal(2,0.2,scenario_num)
a_21=np.random.normal(4,0.2,scenario_num)
a_32=np.random.normal(4,0.2,scenario_num)

x_sto={}
for i in range(2):
    for s in range(scenario_num):
        x_sto[i,s]=sto_model.addVar(lb=0,ub=GRB.INFINITY,vtype=GRB.CONTINUOUS,name='x_'+str(i)+'_'+str(s))

obj=LinExpr(0)
for key in x_sto.keys():
    product_ID=key[0]
    scenario_ID=key[1]
    obj.addTerms(prob[scenario_ID]*profit[product_ID],x_sto[key])
sto_model.setObjective(obj,GRB.MAXIMIZE)

for s in range(scenario_num):
    lhs=LinExpr(0)
    lhs.addTerms(a_11[s],x_sto[0,s])
    lhs.addTerms(a_12[s],x_sto[1,s])
    sto_model.addConstr(lhs<=b[0],name='cons_'+str(0))

for s in range(scenario_num):
    lhs=LinExpr(0)
    lhs.addTerms(a_21[s],x_sto[0,s])
    sto_model.addConstr(lhs<=b[1],name='cons_'+str(1))

for s in range(scenario_num):
    lhs=LinExpr(0)
    lhs.addTerms(a_32[s],x_sto[1,s])
    sto_model.addConstr(lhs<=b[2],name='cons_'+str(2))

sto_model.optimize()
print('Obj=',sto_model.ObjVal)

for s in range(scenario_num):
    print('------scenario  ',s,'---------')
    for i in range(2):
        print(x_sto[i,s].varName,'=',x_sto[i,s].x)
    print('\n\n')

