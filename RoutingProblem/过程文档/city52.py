import copy
city = [
[ 565,575 ],[ 25,185 ],[ 345,750 ],[ 945,685 ],[ 845,655 ],
[ 880,660 ],[ 25,230 ],[ 525,1000 ],[ 580,1175 ],[ 650,1130 ],
[ 1605,620 ],[ 1220,580 ],[ 1465,200 ],[ 1530,5 ],
[ 845,680 ],[ 725,370 ],[ 145,665 ],
[ 415,635 ],[ 510,875 ],[ 560,365 ],[ 300,465 ],[ 520,585 ],[ 480,415 ],
[ 835,625 ],[ 975,580 ],[ 1215,245 ],[ 1320,315 ],[ 1250,400 ],[ 660,180 ],
[ 410,250 ],[ 420,555 ],[ 575,665 ],[ 1150,1160 ],[ 700,580 ],[ 685,595 ],
[ 685,610 ],[ 770,610 ],[ 795,645 ],[ 720,635 ],[ 760,650 ],[ 475,960 ],
[ 95,260 ],[ 875,920 ],[ 700,500 ],[ 555,815 ],[ 830,485 ],[ 1170,65 ],
[ 830,610 ],[ 605,625 ],[ 595,360 ],[ 1340,725 ],[ 1740,245 ]
	]


class Tuplelist:
    def __init__(self,data):
        self.data=data
        self.citysize=len(data)
        self.citylist=list(range(len(self.data)))
        self.dict=self.initDist(data) # dict of all paths
        self.pathsize=len(self.dict) #routesize ->pathsize
        self.tabu=self.initTabu()

    def initDist(self,data):
        tlist={}
        for i in range(self.citysize):
            for j in range(self.citysize):
                if i==j:
                    tlist.update({(i,j):0})
                else:
                    tlist.update({(i,j):self.distance(data[i],data[j])})
        return tlist

    def initTabu(self):
        #初始化tabu属性，生成self.tabu字典类型
        tlist={}
        for i in range(self.citysize):
            for j in range(self.citysize):
                if i==0:
                    tlist.update({(i,j):-1})
                elif i==j:
                    tlist.update({(i,j):-1})
                elif j==0:
                    tlist.update({(i, j): -1})
                else:
                    tlist.update({(i,j):0})
        return tlist

    def getDistance(self,start,end):
        return self.dict[(start,end)]

    def getNextnode(self,start,flist,findmax=False):
        #找到从start结点出发的最近路程结点
        best = flist[0]
        temp=self.dict[(start,flist[0])]
        for i in flist:
            if findmax==False:
                if self.dict[(start, i)] > temp :
                    best = i
            else:
                if self.dict[(start, i)] < temp :
                    best = i
        return best

    def distance(self,X,Y):
        #利用坐标计算两城市的距离
        r=((X[0]-Y[0])**2+(X[1]-Y[1])**2)**0.5
        return r

    def lock(self,i,j,length=15,opposite=True):
        self.tabu[(i,j)]=length
        if opposite==True:
            self.tabu[(j,i)]=length

    def feasibletabu(self,start=True):
        flist=list({k for k,v in self.tabu.items() if v==0})
        if 0 in flist:
            flist.remove(0)
        return flist

    def loosetabu(self):
        key=list(self.tabu.keys())
        value=list(self.tabu.values())
        for i in range(len(key)):
            if value[i]>0:
                self.tabu[key[i]]-=1

route_list=Tuplelist(city)

def check(solution):
    target=list(range(solution.atlas.citysize))
    test=copy.copy(solution.route)
    test.sort()
    indicator= target==test
    return indicator
