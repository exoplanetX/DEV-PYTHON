"""
《运筹优化常用模型算法及案例实战》

"""

from gurobipy import*
import copy
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

initial_LP=Model("intial LP")
x={}
for i in range(2):
    x[i]=initial_LP.addVar(lb=0,ub=GRB.INFINITY,vtype=GRB.CONTINUOUS,name='x_'+str(i))
initial_LP.setObjective(100*x[0]+150*x[i],GRB.MAXIMIZE)
initial_LP.addConstr(2*x[0]+x[1]<=10)
initial_LP.addConstr(3*x[0]+6*x[1]<=40)
initial_LP.optimize()
for var in initial_LP.getVars():
    print(var.Varname,'=',var.x)
initial_LP.status

class Node:
    def __init__(self):
        self.model=None
        self.x_sol={}
        self.x_int_sol={}
        self.local_LB=0
        self.local_UB=np.inf
        self.is_integer=False
        self.branch_var_list=[]

    def deepcopy(node):
        new_node=Node()
        new_node.local_LB=0
        new_node.local_UB=np.inf
        new_node.x_sol=copy.deepcopy(node.x_sol)
        new_node.x_int_sol=copy.deepcopy(node.x_int_sol)
        new_node.branch_var_list=[]
        new_node.model=node.model.copy()
        new_node.is_integer=node.is_integer
        return new_node

def branch_and_bound(initial_LP):
    ####store UB,LB and solution #####
    trend_UB=[]
    trend_LB=[]
    initial_LP.optimize()
    global_LB=0
    global_UB=initial_LP.ObjVal
    eps=1e-3
    incumbent_node=None
    Gap=np.inf

#####branch and bound begins#######
    Queue=[]
#create root node
    node=Node()
    node.local_LB=0
    node.local_UB=global_UB
    node.model=initial_LP.copy()
    node.model.setParam('OutputFlag',0)
    Queue.append(node)
#cycle
    cnt=0
    while(len(Queue)>0 and global_UB-global_LB>eps):
        cnt+=1
        current_node=Queue.pop()
        current_node.model.optimize()
        Solution_status=current_node.model.status
        Is_Integer=True
        Is_pruned=False
        ###
        if(Solution_status==2):
            for var in current_node.model.getVars():
                current_node.x_sol[var.Varname]=var.x
                print(var.VarName,'=',var.x)
                current_node.x_int_sol[var.VarName]=(int)(var.x)
                if(abs( (int)(var.x)-var.x)>=eps):
                    Is_Integer=False
                    current_node.branch_var_list.append(var.VarName)
            # Update LB and UB
            if(Is_Integer==True):
                current_node.local_LB=current_node.model.ObjVal
                current_node.local_UB=current_node.model.ObjVal
                current_node.is_integer=True
                if(current_node.local_LB>global_LB):
                    global_LB=current_node.local_LB
                    incumbent_node=Node.deepcopy(current_node)
            else:
                Is_Integer=False
                current_node.local_UB=current_node.model.ObjVal
                if current_node.local_UB<global_LB:
                    Is_pruned=True
                    current_node.is_integer=False
                else:
                    Is_pruned=False
                    current_node.is_integer=False
                    for var_name in current_node.x_int_sol.keys():
                        var=current_node.model.getVarByName(var_name)
                        current_node.local_LB+=current_node.x_int_sol[var_name]*var.Obj
                    if(current_node.local_LB>global_LB):
                        global_LB=current_node.local_LB
                        incumbent_node=Node.deepcopy(current_node)
                    #### branch
                    branch_var_name=current_node.branch_var_list[0]
                    left_var_bound=(int)(current_node.x_sol[branch_var_name])
                    right_var_bound=(int)(current_node.x_sol[branch_var_name])+1
                    ####current two child nodes
                    left_node=Node.deepcopy(current_node)
                    right_node=Node.deepcopy(current_node)
                    ####add branching constraints
                    temp_var=left_node.model.getVarByName(branch_var_name)
                    left_node.model.addConstr(temp_var<=left_var_bound,name='branch_left_'+str(cnt))
                    left_node.model.update()

                    temp_var=right_node.model.getVarByName(branch_var_name)
                    right_node.model.addConstr(temp_var>=right_var_bound,name='branch_right_'+str(cnt))
                    right_node.model.update()

                    Queue.append(left_node)
                    Queue.append(right_node)
        ####prune by infeasibility
        elif(Solution_status!=2):
            Is_Integer=False
            Is_pruned=True

        ##update Upper bound
        temp_global_UB=0
        for node in Queue:
            node.model.optimize()
            if(node.model.status==2):
                if(node.model.ObjVal>=temp_global_UB):
                    temp_global_UB=node.model.ObjVal
        global_UB=temp_global_UB
        Gap=100*(global_UB-global_LB)/global_UB
        print('Gap:',Gap,'%')
        trend_UB.append(global_UB)
        trend_LB.append(global_LB)
    print('----------------------')

    print('Solution:',incumbent_node.x_int_sol)
    print('Obj:',global_LB)
    plt.plot(trend_LB,label="LB")
    plt.plot(trend_UB,label="UB")
    plt.xlabel("Iteration")
    plt.ylabel("Bound Update")
    plt.title("Bound Update During Branch and Bound Procedure")
    plt.legend()
    plt.show()
    return incumbent_node,Gap
incumbent_node,Gap=branch_and_bound(initial_LP)

