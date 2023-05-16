from gurobipy import*
import time
m = Model("mipl")

x = m.addVar(vtype=GRB.BINARY, name="x")
y = m.addVar(vtype=GRB.BINARY, name="y")
z = m.addVar(vtype=GRB.BINARY, name="z")

m.setObjective(x + y + 2 * z, GRB.MAXIMIZE)

m.addConstr(x + 2 * y + 3 * z <= 4, "c0")
m.addConstr(x + y >= 1, "c1")
start=time.time()
m.optimize()
end=time.time()
for v in m.getVars():
    print("%s %g" % (v.varName, v.x))
print("cost time is:%g" % (end-start))