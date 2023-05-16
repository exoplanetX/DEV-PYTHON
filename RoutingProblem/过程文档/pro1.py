#!/usr/bin/env python3

'''
from sklearn.datasets import load_iris

iris=load_iris()
print(iris.data)
'''
from sympy import diff, symbols,exp,log
x1,x2,t=symbols('x1 x2 t')
func=t*(-70*x1-30*x2)-log(-3*x1-9*x2+540)-log(-5*x1-5*x2+450)-log(-9*x1-3*x2+720)-log(-x1)-log(-x2)
res=diff(func,x1,1)
print(res)
x1=5
print(res)