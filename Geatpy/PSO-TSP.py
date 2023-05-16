import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl

sns.set_style('whitegrid')
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

city_num=25
size = 50
r1 = 0.7
r2 = 0.8
iter_num = 1000
fitness_value_list = []

X = np.random.choice(list(range(1,100)),size=city_num,replace=False)
Y = np.random.choice(list(range(1,100)),size=city_num,replace=False)

#plt.scatter(X,Y,color='r')
#plt.title('城市坐标图')
#plt.show()

def calculate_distance(X,Y):
    """
    计算城市两地之间的欧式距离，结果用Numpy矩阵存储
    :param X: 城市的X坐标，np.array数据
    :param Y: 城市的Y坐标，np.array数据
    :return:
    """
    distance_matrix = np.zeros((city_num,city_num))
    for i in range(city_num):
        for j in range(city_num):
            if i==j:
                continue
            dis=np.sqrt((X[i]-X[j])**2+(Y[i]-Y[j])**2)
            distance_matrix[i][j]=dis
    return distance_matrix

def fitness_func(distance_matrix,xi):
    """
    适应度函数，计算目标函数值
    :param distance_matrix: 城市的距离矩阵
    :param xi: PSO的一个解
    :return: 目标函数值，即总距离
    """
    total_distance=0
    for i in range(1,city_num):
        start= xi[i-1]
        end=xi[i]
        total_distance+=distance_matrix[start][end]
    total_distance+=distance_matrix[end][xi[0]]
    return total_distance

def plot_tsp(gbest):
    plt.scatter(X,Y,color='r')
    for i in range(1,city_num):
        start_x,start_y=X[gbest[i-1]],Y[gbest[i-1]]
        end_x,end_y=X[gbest[i]],Y[gbest[i]]
        plt.plot([start_x,end_x],[start_y,end_y],color='b',alpha=0.8)
    start_x,start_y=X[gbest[0]],Y[gbest[0]]
    plt.plot([start_x,end_x],[start_y,end_y],color='b',alpha=0.8)
    plt.show()

def get_ss(xbest,xi,r):
    """
    计算交换序列，即x2经过交换序列ss得到x1，对应PSO速度更新公式的r1(pbest-xi)和r2(gbest-xi)
    :param xbest: pbest或 gbest
    :param xi: 粒子当前解
    :param r:
    :return:
    """
    velocity_ss=[]
    for i in range(len(xi)):
        if xi[i]!=xbest[i]:
            j=np.where(xi==xbest[i])[0][0]
            so=(i,j,r)
            velocity_ss.append(so)
            xi[i],xi[j]=xi[j],xi[i]
    return velocity_ss

def do_ss(xi,ss):
    """
    执行交换操作
    :param xi:
    :param ss:由交换算子组成的交换序列
    :return:
    """
    for i,j,r in ss:
        rand= np.random.random()
        if rand<=r:
            xi[i],xi[j]=xi[j],xi[i]
    return xi
# 主程序部分
distance_matrix=calculate_distance(X,Y)

XX=np.zeros((size,city_num),dtype=np.int)
for i in range(size):
    XX[i]=np.random.choice(list(range(city_num)),size=city_num,replace=False)
#计算每个粒子对应的适应度
pbest=XX
pbest_fitness=np.zeros((size,1))
for i in range(size):
    pbest_fitness[i]=fitness_func(distance_matrix,xi=XX[i])

#计算全局适应度和对应的解gbest
gbest=XX[pbest_fitness.argmin()]
gbest_fitness = pbest_fitness.min()

#记录算法迭代效果
fitness_value_list.append(gbest_fitness)

#开始迭代
for i in range(iter_num):
    for j in range(size):
        pbesti = pbest[j].copy()
        xi=XX[j].copy()
        #计算交换序列，即v=r1(pbest-xi)+r2(gbest-xi)
        ss1=get_ss(pbesti,xi,r1)
        ss2=get_ss(gbest,xi,r2)
        ss=ss1+ss2
        #执行交换操作，即x=x+v
        xi=do_ss(xi,ss)
        #判断是否更优
        fitness_new=fitness_func(distance_matrix,xi)
        fitness_old=pbest_fitness[j]
        if fitness_new<fitness_old:
            pbest_fitness[j]=fitness_new
            pbest[j]=xi
        #判断全局是否最优
        gbest_fitness_new=pbest_fitness.min()
        gbest_new=pbest[pbest_fitness.argmin()]
        if gbest_fitness_new<gbest_fitness:
            gbest_fitness=gbest_fitness_new
            gbest=gbest_new
        #加入到列表
        fitness_value_list.append(gbest_fitness)

#输出迭代的结果
print('迭代最优结果是：',gbest_fitness)
print('迭代最优变量是：',gbest)

plot_tsp(gbest)
plt.title('TSP路径规划结果')