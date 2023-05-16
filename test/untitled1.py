#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 15:27:28 2020

@author: xuning
"""

from gurobipy import *
m=Model("mip1")
x=m.addVar(vtype=GRB.BINARY,name="x")
y=m.addVar(vtype=GRB.BINARY,name="y")
z=m.addVar(vtype=GRB.BINARY,name="z")

m.setObjective(x+y+2*z,GRB.MAXIMIZE)

m.addConstr(x+2*y+3*z<=4,"c0")
m.addConstr(x+y>=1,"c1")
m.optimize()
#for v in m.objVal():
#    print(v.varName,v.x)
print(m.objVal)
print("x is:"+str(m.x))