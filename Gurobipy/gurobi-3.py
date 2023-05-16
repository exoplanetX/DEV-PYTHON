from gurobipy import *

md=Model()
z1=md.addVar(vtype=GRB.CONTINUOUS,name='z1')
z2=md.addVar(vtype=GRB.CONTINUOUS,name='z2')
z3=md.addVar(vtype=GRB.CONTINUOUS,name='z3')
z4=md.addVar(vtype=GRB.CONTINUOUS,name='z4')

md.addConstr(6*z1>=25)
md.addConstr(2*z2>=30)
md.addConstr(2*z3>=14)
md.addConstr(z4>=8)
md.addConstr(z1>=0)
md.addConstr(z2>=0)
md.addConstr(z3>=0)
md.addConstr(z4>=0)

md.setObjective(z1+z2+z3+z4,GRB.MINIMIZE)
md.optimize()
for v in md.getVars():
    print(v.varName,'=',v.x)
dual=md.getAttr(GRB.Attr.Pi,md.getConstrs())
print(dual)