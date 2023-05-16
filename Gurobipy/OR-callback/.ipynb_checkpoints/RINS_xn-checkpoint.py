from gurobipy import *
import random
def RINScallback(model,where):
    if where==GRB.Callback.MIPNODE:
        if model.cbGet(GRB.Callback.MIPNODE_NODCNT)%100==0 and\
            model.cbGet(GRB.Callback.MIPNODE_STATUS)==GRB.OPTIMAL:
            submodel=model.copy()
            suby=submodel.getVars()
            yrelaxation=model.cbGetNodeRel(model._y)
            for i in range(model._N):
                if abs(yrelaxation[i])<0.01:
                    suby[i].ub=0
                elif abs(yrelaxation[i]-1)<0.01:
                    suby[i].lb=1
            submodel.setParam(GRB.Param.TimeLimit,30)
            submodel.setParam(GRB.Param.OutputFlag,0)
            submodel.optimize()
            if submodel.objval>model.cbGet(GRB.Callback.MIPNODE_OBJBST):
                for i in range(model._N):
                    if abs(suby[i].x)<0.001:
                        model.cbSetSolution(model._y[i],0.0)
                    elif abs(suby[i].x-1)<0.001:
                        model.cbSetSolution(model._y[i],1.0)
try:
    random.seed(1)
    N=20
    Cmatrix={(i,j):random.randint(0,100) for i in range(N) for j in range(N)}
    m=Model('maxcut')

    y=m.addVars(N,vtype=GRB.BINARY,name='y')
    obj=QuadExpr()
    for i in range(N):
        for j in range(N):
            obj=obj+Cmatrix[i,j]*(y[i]+y[j]-2*y[i]*y[j])
    m.setObjective(0.5*obj,GRB.MAXIMIZE)
    m.Params.TimeLimit=600
    m._y=y
    m._y=N
    m.optimize(RINScallback)
    print("obj=",m.ObjVal)
    for i in range(N):
        print(y[i].VarName,'=',y[i].x)


except GurobiError:
    print('Error reported')
