import pandas as pd
import numpy as np
from gurobipy import *

if __name__=='__main__':
    data=pd.read_csv('VRPSPD2.csv').values
    vehicleNum=5
    vehicleQ=40

    c=np.zeros(shape=[data.shape[0],data.shape[0]])
    for i in range(data.shape[0]):
        for j in range(data.shape[0]):
            if i!=j:
                c[i,j]=( (data[i,1]-data[j,1])**2+(data[i,2]-data[j,2])**2 )**0.5
    VRPSPD=Model()

    x={}
    for i in range(data.shape[0]):
        for j in range(data.shape[0]):
            for k in range(vehicleNum):
                if i!=j:
                    x[i,j,k]=VRPSPD.addVar(obj=c[i,j],vtype=GRB.BINARY,name='x_'+str(i)+'_'+str(j)+'_'+str(k))
    y={}
    for i in range(data.shape[0]):
        for j in range(data.shape[0]):
            if i!=j:
                y[i,j]=VRPSPD.addVar(lb=0,vtype=GRB.CONTINUOUS,name='y_'+str(i)+'_'+str(j))
    z={}
    for i in range(data.shape[0]):
        for j in range(data.shape[0]):
            if i!=j:
                z[i,j]=VRPSPD.addVar(lb=0,vtype=GRB.CONTINUOUS,name='z_'+str(i)+'_'+str(j))

    for i in range(1,data.shape[0]):
        expr1=LinExpr(0)
        for j in range(data.shape[0]):
            for k in range(vehicleNum):
                if i!=j:
                    expr1.addTerms(1,x[i,j,k])
    VRPSPD.addConstr(expr1==1,name='cons1')

    for i in range(data.shape[0]):
        for k in range(vehicleNum):
            expr2=LinExpr(0)
            for j in range(data.shape[0]):
                if i!=j:
                    expr2.addTerms(1,x[i,j,k])
                    expr2.addTerms(-1,x[j,i,k])
            VRPSPD.addConstr(expr2==0,name='cons2')

    for k in range(vehicleNum):
        expr3=LinExpr(0)
        for i in range(1,data.shape[0]):
            expr3.addTerms(1,x[0,i,k])
        VRPSPD.addConstr(expr3<=1,name='cons3')

    for i in range(data.shape[0]):
        for j in range(data.shape[0]):
            if i!=j:
                expr4=LinExpr(0)
                expr4.addTerms(1,y[i,j])
                expr4.addTerms(1,z[i,j])
                for k in range(vehicleNum):
                    expr4.addTerms(-vehicleQ,x[i,j,k])
                VRPSPD.addConstr(expr4<=0,name='cons4')
    for i in range(1,data.shape[0]):
        expr5=LinExpr(0)
        for j in range(data.shape[0]):
            if i!=j:
                expr5.addTerms(1,y[i,j])
                expr5.addTerms(-1,y[j,i])
        VRPSPD.addConstr(expr5==data[i,3],name='cons5')

    for i in range(1,data.shape[0]):
        expr6=LinExpr(0)
        for j in range(data.shape[0]):
            if i!=j:
                expr6.addTerms(1,z[j,i])
                expr6.addTerms(-1,z[i,j])
        VRPSPD.addConstr(expr6==data[i,4],name='cons6')

    VRPSPD.optimize()
    VRPSPD.write('VRPSPD.lp')

    S=[]
    for i in range(1,data.shape[0]):
        for k in range(vehicleNum):
            if i not in S and x[0,i,k].x>1-1e-3:
                print('[0-'+str(i),end='')
                currNode=i
                S.append(currNode)
                flag=True
                while flag:
                    flag=False
                    for j in range(1,data.shape[0]):
                        if j not in S and x[currNode,j,k].x>1-1e-3:
                            print('-'+str(j),end='')
                            currNode=j
                            S.append(currNode)
                            flag=True
                            break
                print('-0]')









