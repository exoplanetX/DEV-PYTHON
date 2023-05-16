#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 02:09:54 2020

@author: xuning
"""


from gurobipy import *

try:
    m=Model("mipl")
    
    x=m.addVar(vtype=GRB.BINARY,name="x")
    y=m.addVar(vtype=GRB.BINARY,name="y")
    z=m.addVar(vtype=GRB.BINARY,name="z")
    
    m.setObjective(x+y+2*z,GRB.MAXIMIZE)
    
    m.addConstr(x+2*y+3*z<=4,"c0")
    m.addConstr(x+y>=1,"c1")
    m.optimize()
    
    for v in m.getVars():
        print("%s %g" % (v.varName, v.x))
        
    print('Obj:%g' % m.objVal)
except  GurobiError as e:
    print( 'Error code'+ str(e.errno)+":"+str(e))
    
except AttributeError:
    print("Encountered an attribute error")
    