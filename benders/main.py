# coding:utf-8

import numpy as np
from gurobipy import*
import random

class Benders_Decomposition(object):
    def __init__(self):
        self.Original_MIP_model=None
        self.MP=None
        self.SP=None
        self.Dual_SP=None
        self.opt_sol={}
        self.opt_obj_val=None
        self.LB=0
        self.UB=np.inf
        self.Gap=np.inf
        self.eps=0
        self.MP_y_sol=0
        self.bender_iter=0

    def build_and_solve_original_MIP(self, solve=False, print_sol=False):
        self.Original_MIP_model=Model('Benders decomposition')
        y=self.Original_MIP_model.addVar(lb=0, ub=1000, vtype=GRB.INTEGER, name='y')
        x={}

        for i in range(10):
            x[i]=self.Original_MIP_model.addVar(lb=0,ub=100,vtype=GRB.CONTINUOUS, name='x_'+str(i))

        obj=LinExpr()
        obj.addTerms(1.045,y)
        for i in range(10):
            obj.addTerms(1+0.01*(i+1),x[i])
        self.Original_MIP_model.setObjective(obj,GRB.MAXIMIZE)

        lhs=LinExpr()
        lhs.addTerms(1,y)
        for i in range(10):
            lhs.addTerms(1,x[i])
        self.Original_MIP_model.addConstr(lhs<=1000, name='budget')
        self.Original_MIP_model.update()
        if(solve==True):
            self.Original_MIP_model.optimize()
            if(solve==True and print_sol==True):
                print('\n\n\n')
                print('Obj:',self.Original_MIP_model.ObjVal)
                print('Saving account: ', y.x)
                for i in range(10):
                    if(x[i].x>0):
                        print('Fund ID {}: amount: {}'.format(i+1, x[i].x))

    def build_MP(self):
        self.MP=Model('Benders decomposition-MP')
        y=self.MP.addVar(lb=0, ub=1500, vtype=GRB.INTEGER, name='y')
        z=self.MP.addVar(lb=0, ub=1500, vtype=GRB.INTEGER, name='z')
        self.MP.setObjective(z, GRB.MAXIMIZE)
        self.MP.update()

    def solve_MP(self):
        self.MP.optimize()
        if(print_sol==True):
            print('\n\n\n')
            print('Obj:',self.MP.ObjVal)
            print('z=%4.1f'%(self.getVarByName('z').x))
            print('y=%4.1f'%(self.getVarByName('y').x))

    def build_SP(self,y_var=0,solve=False,print_sol=False):
        self.SP=Model('SP of Benders decomposition')
        x={}

        for i in range(10):
            x[i]=self.Original_MIP_model.addVar(lb=0,ub=100,vtype=GRB.CONTINUOUS,name='x_'+str(i))

        obj=LinExpr()
        for i in range(10):
            obj.addTerms(1+0.01*(i+1),x[i])
        self.SP.setObjective(obj,GRB.MAXIMIZE)

        lhs=LinExpr()
        for i in range(10):
            lhs.addTerms(1,x[i])
        self.SP.addConstr(lhs<=1000-y_var,name='budget')
        self.SP.update()
        if(solve==True):
            self.SP.optimize()

    def update_SP(self,y_bar=0, solve=False, print_sol=False):
        new_budget_constr_rhs=1000-y_bar
        budget_con=self.SP.getConstrByName('budget')
        budget_con.RHS=new_budget_constr_rhs
        self.SP.update()

    def build_Dual_SP(self, y_var=0):
        # 169
        y_bar=1500
        self.Dual_SP = Model('Dual SP')
        alpha_0 = self.Dual_SP.addVar(lb=0, ub=GRB.INFINITY,vtype=GRB.CONTINUOUS, name='alpha_0')
        alpha={}
        for i in range(10):
            alpha[i] = self.Dual_SP.addVar(lb=i, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS )

        """ create objective"""
        obj=LinExpr()
        obj.addTerms(1000-y_bar,alpha_0)
        for  i in range(10):
            obj.addTerms(100,alpha[i])

        self.Dual_SP.setObjective(obj,GRB.MINIMIZE)

        """add constrains 1"""
        # Dual_SP.addConstr(alpha_0>=1.045)

        """add constrains 2-11"""
        for i in range(10):
            self.Dual_SP.addConstr(alpha_0+alpha[i]>=1+0.01*(i+1))

        self.Dual_SP.setParam('InfUnbdInfo', 1)
        self.Dual_SP.update()

    def update_Dual_SP(self,y_bar=0, solve=False):
        new_alpha_0_coef=1000-y_bar
        self.Dual_SP.getVarByName('alpha_0').Obj=new_alpha_0_coef
        self.Dual_SP.update()

    def solve_Dual_SP(self,print_sol=False):
        self.Dual_SP.optimize()
        if(print_sol==True):
            print('\n\n\n')
            print('Model status:',self.Dual_SP.status)
            if(self.Dual_SP.status==2):
                print('Obj:',self.Dual_SP.ObjVal)
                for var in self.Dual_SP.getVars():
                    if(var.x>0):
                        print('{}={}'.format(var.varName,var.x))
            else:
                print('=======Infeasible or Unbounded information======')
                var_alpha_0=self.Dual_SP.getVarByName('alpha_0')
                print('extreme ray: {}={}'.format(var_alpha_0.varName,varName.UnbdRay))
                for i in range(10):
                    var_alpha=self.Dual_SP.getVarByName('alpha_'+str(i))
                    print('extreme ray: {}={}'.format(var_alpha.varName,var_alpha.UnbdRay))

    def print_optimal_sol(self):
        print('Gap: %8.4f' % (self.Gap), end='%\n')
        print('Obj: {}'.format(self.MP.ObjVal))
        print('==== Solution ===== ')
        print('{} = {}'.format('y', self.MP.getVarByName('y').x))
        cnt = 1
        for con in self.Dual_SP.getConstrs():
            if(con.Pi > 0):
                print('x {} = {}'.format(cnt, con.Pi))
                cnt += 1
# 255
    def add_benders_cuts(self,use_Dual_SP=True, y_var=0,benders_iter=0 ):
        """
        This function is tp generate the 'Benders feasibility cut' and 'Benders optimality cut'.
        If the dual subproblem has bounded feasible solution, then a 'Benders optimality cut' will be generated and returned.
        If the dual subproblem is unbounded , then, a 'Benders feasibility cut' will be generated and returned.

        :param self:
        :param use_Dual_SP:  boolean.
            if 'True', we generate cuts via Dual_SP.
            if 'False', we generate cuts via SP itself
        :param y_var:
        :param bender_iter:
        :return:
        """
        if(use_Dual_SP==True):
            """ generate the cut by the Dual SP."""
            Cut_lhs=LinExpr()
            if(self.Dual_SP.status==2):
                """The Dual_SP has bounded feasible solution, then generate benders optimality cut."""
                """Cut: 1.045y+(1000-y)*alpha_0+sum_{i=1}^{10} alpha_i * 100>=z"""
                var_y=self.MP.getVarByName('y')
                var_z=self.MP.getVarByName('z')
                var_y_coef=1.045
                Cut_lhs.addTerms(1.045,var_y)

                alpha_0_value=self.Dual_SP.getVarByName('alpha_0').x
                Cut_lhs.addTerms(-alpha_0_value,var_y)
                var_y_coef=var_y_coef-alpha_0_value

                constant=0
                for var in self.Dual_SP.getVars():
                    if(var.varName=='alpah_0'):
                        constant+=1000*var.x
                    else:
                        constant+=100*var.x
                con_name='Benders optimality cut iter '+str(benders_iter)
                Cut=self.MP.addConstr(Cut_lhs+constant>=var_z,name=con_name)
                self.MP.update()
                print("\nIter: {}, Add optimality cut : {}+{} >= z\n".format(benders_iter,Cut_lhs,constant))
            if(self.Dual_SP.status!= 2):
                """ The Dual_SP is unbounded, then generate benders feasibility cut. """
                """ Cut: (1000-y)*alpha_0 +sum_{i=1}^{10} alpha_i * 100>= 0"""
                var_y=self.MP.getVarByName('y')
                alpha_0_ray=self.Dual_SP.getVarByName('alpha_0').UnbdRay
                Cut_lhs.addTerms(-alpha_0_ray,var_y)

                var_y_coef=-alpha_0_ray

                constant=0
                for var in self.Dual_SP.getVars():
                    if(var.varName=='alpah_0'):
                        constant+=1000*var.UnbdRay
                    else:
                        constant+=100*var.UnbdRay
                con_name='Benders feasibility cut iter'+str(benders_iter)
                Cut=self.MP.addConstr(Cut_lhs+constant>=0, name=con_name)
                self.MP.update()
                print("\n Iter: {}, Add feasibility cut: {} + {}>=0 \n".format(benders_iter, Cut_lhs, constant))
            else:
                """ If not use dual SP, then we generate cuts by primal SP."""
    def Benders_Decomposition(self, eps=0):
        """ Initialize"""
        self.UB=1500
        self.LB=1000
        self.Gap=np.inf
        self.eps=0.001
        self.benders_iter=0
        max_no_change=2
        no_change_cnt=0
        y_bar_change=[]

        """build the initial MP"""
        self.build_MP()
        self.MP.setParam('OutputFlag',0)
        self.MP.optimize()

        """ get an initial y_var"""
        y_var=1000
        y_bar_change.append(y_var)

        """build Dual SP"""
        self.build_Dual_SP(y_var=y_var)
        self.Dual_SP.setParam('OutputFlag',0)

        """ Main loop of Benders Decomposition"""
        print('\n\n ===========================================================')
        print('                Benders Decomposition Starts                   ')
        print(' ==========================================================')
        while(self.UB-self.LB>self.eps):
            self.benders_iter+=1
            """update SP by y_bar"""
            self.update_Dual_SP(y_bar=y_var)
            """ solve Dual SP"""
            self.Dual_SP.optimize()

            """ update global LB"""
            if(self.Dual_SP.status==2):
                self.LB=max(self.LB, self.MP_y_sol*1.045+self.Dual_SP.ObjVal)

            """generate Cuts"""
            self.add_benders_cuts(use_Dual_SP=True, y_var=y_var, benders_iter=self.benders_iter)

            """solve updated MP"""
            self.MP.optimize()
            self.MP_y_sol=self.MP.getVarByName('y').x

            """update the global UB"""
            self.UB=min(self.UB, self.MP.ObjVal)

            """update optimality Gap"""
            self.Gap=round(100*(self.UB-self.LB)/self.LB, 4)

            """ update y_bar"""
            y_var=self.MP.getVarByName('y').x
            y_bar_change.append(y_var)

            """ if y_bar do not change, then give an different value"""
            if (y_bar_change[-1]==y_bar_change[-2]):
                no_change_cnt+=1
            else:
                no_change_cnt=0
            if(no_change_cnt>max_no_change):
                y_var=random.randint(0,1000)
                no_change_cnt=0

            print('    %7.2f   '%self.UB,end='')
            print('    %7.2f   '%self.LB,end='')
            print('  %8.4f   '%self.Gap, end='%')
            print()
            print('\n\n =================Optimal Solution Found!===========')
            self.print_optimal_sol()


if __name__ == '__main__':
    bender_solver = Benders_Decomposition()
    bender_solver.Benders_Decomposition(eps=0)
