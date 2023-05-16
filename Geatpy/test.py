#!/usr/bin/env python3
import numpy as np
import geatpy as ea
x1=[-1.5,4]
x2=[-3,4]
b1=[1,1]
b2=[1,1]
ranges=np.vstack([x1,x2]).T
borders=np.vstack([b1,b2]).T
varTypes=np.array([0,0])

Encoding='BG'
codes=[1,1]
precisions=[6,6]
scales=[0,0]
FieldD=ea.crtfld(Encoding,varTypes,ranges,borders,precisions,codes,scales)
