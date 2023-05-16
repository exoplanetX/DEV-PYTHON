import geatpy as ea
from geatpy import crtfld
import numpy as np

#def aim(x):                    # 传入种群染色体矩阵解码后的基因表现型矩阵
#    return x * np.sin(10 * np.pi * x) + 2.0

def aim(Phen):
    x1=Phen[:,[0]]
    x2=Phen[:,[0]]
    return np.sin(x1+x2)+(x1-x2)**2-1.5*x1+2.5*x2+1

Encoding="BG"
varTypes=np.array([0,0])
ranges=np.vstack([[-10,10],[-8,8]]).T
borders=np.vstack([[1,1],[1,1]]).T
precisions=[5,5]
codes=[1,1]
scales=[0,0]
FieldD=crtfld(Encoding,varTypes,ranges,borders,precisions,codes,scales)
print(FieldD)

NIND=20
MAXGEN=100
maxormins=np.array([1])
selectStyle='sus'
recStyle="xovdp"
mutStyle="mutbin"
Lind=int(np.sum(FieldD[0,:]))
pc=0.9
pm=1/Lind
Chrom=ea.crtpc(Encoding,NIND,FieldD)
print(Chrom)

variable=ea.bs2real(Chrom,FieldD)
print(variable)
ObjV=aim(variable)
print(ObjV)
FitnV=ea.ranking(maxormins*ObjV)
SelCh=Chrom[ea.selecting(selectStyle,FitnV,NIND-1),:]
SelCh=ea.recombin(recStyle,SelCh,pm)
print("the SelCh list is :")
print(SelCh)