import gurobipy as gb
#from gurobipy import*
m=gb.Model()
x=m.addVar(name='x')
y=m.addVar(name='y')
m.setObjective(x+2*y,gb.GRB.MAXIMIZE)
m.addConstr(x+y<=4)
m.optimize()
print(m.getVars())