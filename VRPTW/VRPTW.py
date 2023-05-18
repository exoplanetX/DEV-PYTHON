"""
直接按照模型公式写入gurobi进行计算。
"""
import math
from gurobipy import *

class Data:
    customerNum = 0
    vehicleNum  = 0
    capacity    = 0
    cor_X       = []
    cor_Y       = []
    demand      = []
    serviceTime = []
    readyTime   = []
    dueTime     = []
    disMatrix   = [[]]


def readData(data, path, customerNum):
    data.customerNum = customerNum
    f = open(path, 'r')
    lines = f.readlines()
    count = 0

    line = lines[4];
    line = line[:-1].strip()
    str = re.split(r"\s{1,}", line)

    data.vehicleNum = int(str[0])
    data.capacity = float(str[1])

    for i in range(9, len(lines)):
        line = lines[i];
        count = count + 1

        line = line[:-1].strip()
        str = re.split(r"\s{1,}", line)
        data.cor_X.append(float(str[1]))
        data.cor_Y.append(float(str[2]))
        data.demand.append(float(str[3]))
        data.readyTime.append(float(str[4]))
        data.dueTime.append(float(str[5]))
        data.serviceTime.append(float(str[6]))

    data.cor_X.append(data.cor_X[0])
    data.cor_Y.append(data.cor_Y[0])
    data.demand.append(data.demand[0])
    data.readyTime.append(data.readyTime[0])
    data.dueTime.append(data.dueTime[0])
    data.serviceTime.append(data.serviceTime[0])

    data.disMatrix = [([0] * (data.customerNum + 2)) for p in range(data.customerNum + 2)]

    for i in range(0, data.customerNum + 2):
        for j in range(0, data.customerNum + 2):
            if (i != j):
                temp = (data.cor_X[i] - data.cor_X[j]) ** 2 + (data.cor_Y[i] - data.cor_Y[j]) ** 2
                data.disMatrix[i][j] = math.sqrt(temp)
                temp = 0
            else:
                data.disMatrix[i][j] = math.sqrt(100000.0)
    return data

#---读取数据
data = Data()
path = 'C:/Users/xuning/OneDrive/code/DEV-PYTHON/Gurobipy/c101.txt' #读取算例数据集
customerNum = 100  #设置客户数量
readData(data, path, customerNum)
BigM = 100000

x = {}  # 存放决策变量x_ijk
s = {}  # s_ik表示车辆k开始服务客户i的时间

model = Model()

# 定义决策变量，并加入模型当中：
for i in range(0, data.customerNum + 2):
    for k in range(0, data.vehicleNum):
        name = 's_' + str(i) + '_' + str(k)
        s[i, k] = model.addVar(0, 1500, vtype=GRB.CONTINUOUS, name=name)

        for j in range(0, data.customerNum + 2):
            if (i != j):
                name = 'x_' + str(i) + '_' + str(j) + '_' + str(k)
                x[i, j, k] = model.addVar(0, 1, vtype=GRB.BINARY, name=name)

            # 根据式(1)定义目标函数，并加入模型当中：
obj = LinExpr(0)
for i in range(data.customerNum + 2):
    for k in range(data.vehicleNum):
        for j in range(data.customerNum + 2):
            if (i != j):
                obj.addTerms(data.disMatrix[i][j], x[i, j, k])

model.setObjective(obj, GRB.MINIMIZE)

# 约束二：
for i in range(1, data.customerNum + 2 - 1):
    lhs = LinExpr(0)
    for k in range(data.vehicleNum):
        for j in range(1, data.customerNum + 2):
            if (i != j):
                lhs.addTerms(1, x[i, j, k])
    model.addConstr(lhs == 1, name='visit_' + str(i))

# 约束三：
for k in range(0, data.vehicleNum):
    lhs = LinExpr(0)
    for j in range(1, data.customerNum + 2):
        lhs.addTerms(1, x[0, j, k])
    model.addConstr(lhs == 1, name='vehicle_' + str(k))

# 约束四：
for k in range(data.vehicleNum):
    for h in range(1, data.customerNum + 2 - 1):
        expr1 = LinExpr(0)
        expr2 = LinExpr(0)
        for i in range(data.customerNum + 2 - 1):
            if (h != i):
                expr1.addTerms(1, x[i, h, k])

        for j in range(1, data.customerNum + 2):
            if (h != j):
                expr2.addTerms(1, x[h, j, k])

        model.addConstr(expr1 == expr2, name='flow_conservation_' + str(i))
        expr1.clear()
        expr2.clear()

# 约束五：
for k in range(data.vehicleNum):
    lhs = LinExpr(0)
    for j in range(data.customerNum + 2 - 1):
        lhs.addTerms(1, x[j, data.customerNum + 2 - 1, k])
    model.addConstr(lhs == 1, name='enter_' + str(k))

# 约束六
for k in range(data.vehicleNum):
    for i in range(data.customerNum + 2):
        for j in range(data.customerNum + 2):
            if (i != j):
                model.addConstr(
                    s[i, k] + data.disMatrix[i][j] + data.serviceTime[i] - s[j, k] - 2 * BigM + 2 * BigM * x[
                        i, j, k] <= 0, name='time_windows_')

# 约束七：
for k in range(data.vehicleNum):
    for i in range(1, data.customerNum + 2 - 1):
        lhs1 = LinExpr()
        lhs2 = LinExpr()
        for j in range(1, data.customerNum + 2):
            if (i != j):
                model.addConstr(data.readyTime[i] * x[i, j, k] <= s[i, k], name='ready_time_' + str(i))
                model.addConstr(data.dueTime[i] + (BigM - BigM * x[i, j, k]) >= s[i, k], name='due_time_' + str(i))

# 约束八：
for k in range(data.vehicleNum):
    model.addConstr(data.readyTime[0] <= s[0, k], name='ready_time_' + str(0))
    model.addConstr(data.dueTime[0] >= s[0, k], name='due_time_' + str(0))
    model.addConstr(data.readyTime[data.customerNum + 1] <= s[data.customerNum + 1, k],
                    name='ready_time_' + str(data.customerNum + 1))
    model.addConstr(data.dueTime[data.customerNum + 1] >= s[data.customerNum + 1, k],
                    name='due_time_' + str(data.customerNum + 1))

# 约束九
for k in range(data.vehicleNum):
    lhs = LinExpr(0)
    for i in range(1, data.customerNum + 2 - 1):
        for j in range(1, data.customerNum + 2):
            if (i != j):
                lhs.addTerms(data.demand[i], x[i, j, k])
    model.addConstr(lhs <= data.capacity, name='capacity_' + str(k))

model.optimize()
print("\n\n-----optimal value-----")
print(model.ObjVal)

print("routes = ")
for k in range(data.vehicleNum):
    sys.stdout.write("[")
    i = 0;
    while i <= customerNum + 2 - 1:
        if(i == customerNum + 1):
            sys.stdout.write(str(i))
            break
        for j in range(1,data.customerNum + 2):
            if(i != j and x[i,j,k].x > 0):
                sys.stdout.write(str(i) + ",")
                break;
        i = j
    sys.stdout.write("]")
    print("")
