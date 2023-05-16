
from gurobipy import *

model = Model('Benders decomposition')

""" create decision variables """
y = model.addVar(lb=0, ub=1000, vtype=GRB.INTEGER, name='y')
x = {}

for i in range(10):
    x[i] = model.addVar(lb=0, ub=100, vtype=GRB.CONTINUOUS, name='x_' + str(i))

""" set objective function """
obj = LinExpr()
obj.addTerms(1.045, y)
for i in range(10):
    obj.addTerms(1 + 0.01 * (i + 1), x[i])
model.setObjective(obj, GRB.MAXIMIZE)

""" add constraints """
lhs = LinExpr()
lhs.addTerms(1, y)
for i in range(10):
    lhs.addTerms(1, x[i])
model.addConstr(lhs <= 1000, name='budget')

model.optimize()
print('\n\n\n')
print('Obj:', model.ObjVal)
print('Saving account : ', y.x)
for i in range(10):
    if(x[i].x > 0):
        print('Fund ID {}: amount: {}'.format(i+1, x[i].x))
