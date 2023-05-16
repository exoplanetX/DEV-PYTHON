import numpy as np
import geatpy as ea

AIM_M=__import__('aimfunc')

x1=[-3,12.1]
x2=[4.1,5.8]
b1=[1,1]
b2=[1,1]
codes=[0,0]
precisions=[4,4]

scales=[0,0]
ranges=np.vstack([x1,x2]).T
borders=np.vstack([b1,b2]).T
FieldD=ea.crtfld(ranges,borders,precisions,codes,scales)

[pop_trace,var_trace,times]=ea.sga_new_code_templet(AIM_M,'aimfunc',None,None,FieldD,problem='R',maxormin=-1,
                                                    MAXGEN=10000,MIND=100,SUBPOP=1,GGAP=0.8,selectStyle='sus',
                                                    recombinStyle='xovdp',recopt=None,pm=None,distribute=True,
                                                    drawing=0)