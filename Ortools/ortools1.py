from ortools.sat.Python import cp_model

model=cp_model.CpModel()

x1=model.NewIntVar(0,100,'x1')
x2=model.NewIntVar(0,100,'x2')
x3=model.NewIntVar(0,100,'x3')
x4=model.NewIntVar(0,100,'x4')
x5=model.NewIntVar(0,100,'x5')
x6=model.NewIntVar(0,100,'x6')
x7=model.NewIntVar(0,100,'x7')
x8=model.NewIntVar(0,100,'x8')

model.Add(2*x1+x2+x3+x4>=100)
model.Add(2*x2+x3+3*x5+2*x6+x7>=150)
model.Add(x1+x3+3*x4+2*x6+3*x7+5*x8>=100)

model.Minimize(5*x1+6*x2+23*x3+5*x4+24*x5+6*x6+23*x7+5*x8)
solver=cp_model.CpSolver()
solver.Solve(model)

print('目标函数值是：',solver.ObjectiveValue())
