import numpy as np
def aimfunc(Phen,LegV):
    x=Phen[:,[0]]
    y=Phen[:,[1]]
    f=np.sin(x+y)+(x+y)**2-1.5*+2.5*y+1
    return [f,LegV]