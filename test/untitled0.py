#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 02:54:28 2020

@author: xuning
"""

from gurobipy import*
cities=[('A','B'),('A','C'),('B','C'),('B','D'),('C','D')]
routes=tuplelist(cities)
b=[i**2 for i in range(6)]
print(b)