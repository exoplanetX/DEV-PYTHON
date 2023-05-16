
import numpy as np
import networkx as nx
from time import *
import copy
#点包含时间窗属性
Nodes={'s':(0,0),
       '1':(6,14),
       '2':(9,12),
       '3':(8,12),
       't':(9,15)
       }
#弧Arcs的属性，包括travel_time和distance
Arcs={('s','1'):(8,3),
      ('s','2'):(5,5),
      ('s','3'):(12,2),
      ('1','t'):(4,7),
      ('2','t'):(2,6),
      ('3','t'): (4,3)
      }
#create the directed Graph
Graph=nx.DiGraph()
cnt=0
#add nodes into the graph
for name in Nodes.keys():
    cnt+=1
    Graph.add_node(name,
                   time_window=(Nodes[name][0],Nodes[name][1]),
                   min_dis=0
                   )
#add edges into the graph
for key in Arcs.keys():
    Graph.add_edge(key[0],key[1],
                   travel_time=Arcs[key][0],
                   length=Arcs[key][1]
                   )

#创建Lable类
class Label:
    paht=[]
    travel_time=0
    distance=0

#dominance rule
def dominate(Q,Path_set):
    QCopy=copy.deepcopy(Q)
    PathsCopy=copy.deepcopy(Path_set)

    for label in QCopy:
        for another_label in Q:
            if (label.path[-1]==another_label.path[-1] and
                label.time < another_label.time and label.dis<another_label.dis):
                Q.remove(another_label)
            print('dominated path(Q):',another_label.path)
    #dominance paths
    for key_1 in PathsCopy.keys():
        for key_2 in PathsCopy.keys():
            if (PathsCopy[key_1].path[-1] == PathsCopy[key_2].path[-1]
                    and PathsCopy[key_1].travel_time < PathsCopy[key_2].travel_time
                    and PathsCopy[key_1].length < PathsCopy[key_2].length
                    and (key_2 in Path_set.keys())):
                Path_set.pop(key_2)
                print('dominated path (P) : ', PathsCopy[key_1].path)

    return Q, Path_set


# labeling algorithm
def Labeling_SPPRC(Graph, org, des):
    # initial Q
    Q = []
    Path_set = {}

    # creat initial label
    label = Label()
    label.path = [org]
    label.travel_time = 0
    label.distance = 0
    Q.append(label)

    count = 0

    while (len(Q) > 0):
        count += 1
        current_path = Q.pop()

        # extend the current label
        last_node = current_path.path[-1]
        for child in Graph.successors(last_node):
            extended_path = copy.deepcopy(current_path)
            arc = (last_node, child)

            # check the feasibility
            arrive_time = current_path.travel_time + Graph.edges[arc]['travel_time']
            time_window = Graph.nodes[child]['time_window']
            if (arrive_time >= time_window[0] and arrive_time <= time_window[1] and last_node != des):
                extended_path.path.append(child)
                extended_path.travel_time += Graph.edges[arc]['travel_time']
                extended_path.distance += Graph.edges[arc]['length']
                Q.append(extended_path)

    Path_set[count] = current_path
    # 调用dominance rule
    Q, Path_set = dominate(Q, Path_set)

    # filtering Paths, only keep feasible solutions
    Path_set_copy = copy.deepcopy(Path_set)
    for key in Path_set_copy.keys():
        if (Path_set[key].path[-1] != des):
            Path_set.pop(key)

    # choose optimal solution
    opt_path = {}
    min_dis = 1e6
    for key in Path_set.keys():
        if (Path_set[key].distance < min_dis):
            min_dis = Path_set[key].distance
            opt_path[1] = Path_set[key]

    return Graph, Q, Path_set, opt_path

#调用labeling 算法计算
org = 's'
des = 't'
begin_time = time()
Graph, Q, Path_set, opt_path = Labeling_SPPRC(Graph, org, des)
end_time = time()
print("计算时间： ", end_time - begin_time)
print('optimal path : ', opt_path[1].path )
print('optimal path (distance): ', opt_path[1].distance)
print('optimal path (time): ', opt_path[1].travel_time)