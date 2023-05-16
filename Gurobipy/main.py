from gurobipy import*

model=Model('production plan')
x={}
for i in range(1,3):
    x[i] = model.addVar(lb=0,ub=GRB.INFINITY,vtype=GRB.CONTINUOUS,name='x_'+str(i))

model.setObjective(2*x[1]+3*x[2],GRB.MAXIMIZE)
model.addConstr(x[1]+2*x[2]<=8,name='cons_1')
model.addConstr(4*x[1]<=16,name='cons_2')
model.addConstr(4*x[2]<=12,name='cons_3')

model.optimize()
print('Obj=',model.ObjVal)
for key in x.keys():
    print(x[key].varName,'=',x[key].x)
