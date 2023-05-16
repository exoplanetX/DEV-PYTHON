from gurobipy import *

MP = Model('Benders decomposition-MP')

""" create decision variables """
y = MP.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.INTEGER, name='y')
z = MP.addVar(lb=0, ub=GRB.INFINITY, vtype=GRB.INTEGER, name='z')

MP.setObjective(z, GRB.MAXIMIZE)

MP.addConstr(1000 - y >= 0, name='benders feasibility cut iter 1')

MP.optimize()
print('\n\n\n')
print('Obj:', MP.ObjVal)
print('z = %4.1f' % (z.x))
print('y = %4.1f' % (y.x))