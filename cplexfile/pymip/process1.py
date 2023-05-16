import docplex.mp
d1 = 25
d2 = 35
Costs = [[20,  15,  22,  27,  13,  4,  15,  6,  15,  22,  25,  13,  7,  28,  14,  5,  8,  1,  17,  3,  19,  17,  22,  12,  14],
   [2,  15,  16,  16,  10,  13,  4,  2,  6,  29,  10,  8,  20,  11,  8,  11,  28,  17,  10,  29,  3,  24,  12,  11,  11],
   [13,  14,  6,  17,  14,  13,  8,  29,  19,  26,  22,  0,  8,  29,  15,  20,  5,  20,  26,  17, 24, 10, 24, 9, 1],
   [7, 27, 24, 3, 4, 23, 11, 9, 18, 1, 29, 24, 16, 9, 8, 3, 18, 24, 10, 12, 1, 3, 15, 29, 3],
   [25, 26, 29, 6, 24, 8, 2, 10, 17, 0, 4, 7, 2, 17, 2, 27, 24, 20, 18, 5, 5, 2, 21, 26, 20],
   [29, 5, 15, 5, 4, 26, 18, 8, 2, 14, 13, 6, 14, 28, 16, 28, 23, 8, 5, 8, 10, 28, 17, 0, 23],
   [12, 16, 10, 16, 17, 10, 29, 11, 28, 22, 25, 8, 27, 12, 10, 28, 7, 5, 3, 9, 18, 10, 15, 16, 2],
   [12, 9, 14, 23, 26, 4, 3, 3, 22, 12, 11, 9, 19, 5, 6, 16, 1, 1, 9, 20, 23, 23, 27, 4, 11],
   [18, 13, 28, 29, 3, 28, 16, 11, 9, 2, 7, 20, 13, 23, 6, 10, 3, 16, 14, 2, 15, 17, 1, 19, 27],
   [29, 17, 17, 14, 21, 18, 8, 21, 9, 20, 14, 6, 29, 24, 24, 4, 18, 16, 21, 24, 26, 0, 26, 9, 5],
   [27, 24, 21, 28, 17, 18, 10, 10, 26, 25, 13, 18, 2, 9, 16, 26, 10, 22, 5, 17, 15, 0, 9, 0, 16],
   [13, 15, 17, 21, 25, 9, 22, 13, 20, 15, 1, 17, 18, 10, 2, 27, 19, 21, 14, 26, 29, 13, 28, 28, 15],
   [16, 12, 2, 2, 9, 27, 11, 14, 12, 2, 14, 29, 3, 12, 18, 6, 7, 9, 1, 5, 19, 14, 11, 29, 4],
   [1, 15, 27, 29, 16, 17, 10, 10, 17, 19, 6, 10, 20, 20, 19, 10, 19, 26, 15, 7, 20, 19, 13, 3, 22],
   [22, 14, 12, 3, 22, 6, 15, 3, 6, 10, 9, 13, 11, 21, 6, 19, 29, 4, 5, 21, 7, 12, 13, 11, 22],
   [9, 27, 22, 29, 11, 14, 1, 19, 21, 2, 4, 13, 17, 9, 10, 17, 13, 8, 24, 13, 26, 27, 23, 4, 21],
   [3, 14, 26, 18, 17, 3, 1, 11, 13, 8, 22, 3, 18, 26, 17, 15, 22, 10, 19, 23, 13, 14, 17, 18, 27],
   [21, 14, 1, 28, 28, 0, 0, 29, 12, 23, 22, 17, 19, 2, 10, 19, 4, 18, 28, 13, 27, 12, 9, 29, 22],
   [29, 3, 20, 5, 5, 23, 28, 16, 1, 8, 26, 23, 11, 11, 21, 17, 13, 21, 3, 8, 6, 15, 18, 6, 24],
   [14, 20, 26, 10, 17, 20, 5, 9, 25, 20, 14, 22, 5, 12, 0, 18, 7, 0, 8, 15, 21, 12, 26, 7, 21],
   [7, 7, 1, 9, 24, 29, 0, 3, 29, 24, 1, 6, 14, 0, 11, 5, 21, 12, 15, 1, 25, 4, 7, 17, 16],
   [8, 18, 15, 6, 1, 22, 26, 13, 19, 20, 12, 15, 19, 27, 13, 3, 22, 22, 22, 20, 0, 4, 24, 13, 25],
   [14, 6, 29, 23, 8, 5, 4, 18, 21, 29, 18, 2, 2, 3, 7, 13, 12, 9, 2, 18, 26, 3, 18, 7, 7],
   [5, 8, 4, 8, 25, 4, 6, 20, 14, 21, 18, 16, 15, 11, 7, 8, 20, 27, 22, 7, 5, 8, 24, 11, 8],
   [0, 8, 29, 25, 29, 0, 12, 25, 19, 9, 19, 25, 27, 21, 2, 23, 2, 25, 17, 6, 0, 6, 15, 2, 15],
   [23, 24, 10, 26, 7, 5, 5, 26, 1, 16, 22, 8, 24, 9, 16, 17, 1, 26, 20, 23, 18, 20, 23, 2, 19],
   [16, 3, 9, 21, 15, 29, 8, 26, 20, 12, 18, 27, 29, 15, 24, 9, 17, 24, 3, 5, 21, 28, 7, 1, 12],
   [1, 11, 21, 1, 13, 14, 16, 14, 17, 25, 18, 9, 19, 26, 1, 13, 15, 6, 14, 10, 12, 19, 0, 15, 7],
   [20, 14, 7, 5, 8, 16, 12, 0, 5, 14, 18, 16, 24, 27, 20, 7, 11, 3, 16, 8, 2, 2, 4, 0, 3],
   [26, 19, 27, 29, 8, 9, 8, 10, 18, 4, 6, 0, 5, 17, 12, 18, 17, 17, 13, 0, 16, 12, 18, 19, 16],
   [3, 12, 11, 28, 3, 2, 14, 14, 17, 29, 18, 14, 19, 24, 9, 27, 4, 19, 6, 24, 19, 3, 28, 20, 4],
   [2, 0, 21, 14, 21, 12, 27, 6, 20, 29, 13, 21, 23, 0, 20, 4, 11, 27, 3, 11, 21, 11, 21, 4, 17],
   [20, 26, 5, 8, 18, 14, 12, 12, 24, 3, 8, 0, 25, 16, 19, 21, 7, 4, 23, 21, 20, 28, 6, 21, 19],
   [16, 18, 9, 1, 9, 7, 14, 6, 28, 26, 3, 14, 27, 4, 9, 9, 1, 9, 24, 3, 14, 13, 18, 3, 27],
   [1, 19, 7, 20, 26, 27, 0, 7, 4, 0, 13, 8, 10, 17, 14, 19, 21, 21, 14, 15, 22, 14, 5, 27, 0]];
R1 = range(1,d1)
R2 = range(1,d2)
from docplex.mp.model import Model
m = Model(name='benders', log_output=True)
X = m.continuous_var_dict([(i,j) for i in R2 for j in R1])
Y = m.integer_var_dict(R1, 0, 1)
bendersPartition = {(i,j) : i for i in R2 for j in R1}
m.minimize( m.sum( Costs[i][j]*X[i,j] for i in R2 for j in R1) + sum(Y[i] for i in R1) )
m.add_constraints( m.sum( X[i,j] for j in R1) ==1 for i in R2)
m.add_constraints( X[i,j] - Y[j] <= 0 for i in R2 for j in R1)
m.parameters.benders.strategy = 3
msol = m.solve()
m.report()
m.parameters.benders.strategy = 1
for i in R2:
    for j in R1:
        X[i,j].benders_annotation =  i%2
msol = m.solve(clean_before_solve=True)
m.report()