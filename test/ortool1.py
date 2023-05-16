#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 02:09:54 2020

@author: xuning
"""

from __future__ import print_function
from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver('simple_lp_program',
                             pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    
    xx = solver.NumVar(0,1,'x')
    yy = solver.NumVar(0,2,'y')
    
    print('Number of variable = ', solver.NumVariables())
    
    ct=solver.Constraint(0,2,'ct')
    ct.SetCoefficient(xx,1)
    ct.SetCoefficient(yy,1)
    
    print('Number of constraints = ', solver.NumConstraints())
    
    objective= solver.Objective()
    objective.SetCoefficient(xx,3)
    objective.SetCoefficient(yy,1)
    objective.SetMaximization()
    
    solver.Solve()
    
    print('Solution:')
    print('Objective value= ',objective.Value())
    print('x= ',xx.solution_value())
    print('y= ',yy.solution_value())
    
if __name__ == '__main__':
    main()