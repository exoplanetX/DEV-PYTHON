from gurobipy import*
class Data:
    customerNum=0
    nodeNum=0
    vehicleNum=0
    capacity=0
    cor_X=[]
    cor_Y=[]
    demand=[]
    serviceTime=[]
    readyTime=[]
    dueTime=[]
    disMatrix=[[]]

def readData(data,path,customerNum):
    data.customerNum=customerNum
    data.nodeNum=customerNum+2
    f=open(path,'r')
    lines=f.readlines()
    count=0

    for line in lines:
        count= count+1
        if(count == 5):
            line = line[:-1].strip()
            str=re.splite(r" +",line)
            data.vehicleNum=int(str[0])
            data.capacity=float(str[1])
        elif(count>=10 and count<=10+customerNum):
            line=line[:-1]
            str=re.splite(r"+",line)
            data.cor_X.append(float(str[2])
            data.cor_Y.append(float(str[3])
            data.demand.append(float(str[4]))
            data.readyTime.append(float(str[5]))
            data.dueTime.append(float(str[6]))
            data.serviceTime.append(float(str[7]))
