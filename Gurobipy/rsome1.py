from rsome import ro
from rsome import grb_solver

model=ro.Model('LP model')
x=model.dvar()
y=model.dvar()
model.max(3*x+4*y)
model.st(2.5*x+y<=20)
model.st(5*x+3*y<=30)
model.st(x+2*y<=16)
model.st(abs(y)<=2)
model.solve(grb_solver)

print('x:',x.get())
print('y:',y.get())
print('Objective:',model.get())