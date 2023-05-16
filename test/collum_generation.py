import gurobipy as grb
m=grb.Model()

z1=m.addVar(vtype=grb.GRB.CONTINUOUS,name='z1')
z2=m.addVar(vtype=grb.GRB.CONTINUOUS,name='z2')
z3=m.addVar(vtype=grb.GRB.CONTINUOUS,name='z3')
z4=m.addVar(vtype=grb.GRB.CONTINUOUS,name='z4')

m.addConstr(6*z1>=25)
m.addConstr(2*z2>=30)
m.addConstr(2*z3>=14)
m.addConstr(z4>=8)
m.addConstr(z1>=0)
m.addConstr(z2>=0)
m.addConstr(z3>=0)
m.addConstr(z4>=0)

m.setObjective(z1+z2+z3+z4,grb.GRB.MINIMIZE)

m.optimize()

for v in m.getVars():
    print(v.varName,'=',v.x)

dual=m.getAttr(grb.GRB.Attr.Pi,m.getConstrs())
print(dual)