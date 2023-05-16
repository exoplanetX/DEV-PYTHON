#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 11:07:40 2020

@author: xuning
"""

from gurobipy import *
m=Model("milp2")
x=m.addVar(vtype=GRB.BINARY,name="xx")
y=m.addVar(vtype=GRB.BINARY,name="y")
z=m.addVar(vtype=GRB.BINARY,name="z")
m.setObjective(x+y+2*z,GRB.MAXIMIZE)
m.addConstr(x+2*y+3*z<=4,"c0")
m.addConstr(x+y>=1,"c1")
m.optimize()