
from ortools.linear_solver import pywraplp

solver= pywraplp.Solver.CreateSolver('SCIP')
status=solver.Solver()
infinity=solver.infinity()
x=solver.IntVar(0.0,infinity,'x')
y=solver.IntVar(0.0,infinity,'y')
print('Number of variable=',solver.NumVariables())
solver.Add(x+7*y<=17.5)
solver.Add(x<=3.5)
solver.Maximize(x+10*y)
status=solver.Solver()
if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Objective value=',solver.Objective().Value())
    print('x=',x.solution_value())
    print('y=',y.solution_value())
else:
    print('The problem does not have an optimal solution.')
