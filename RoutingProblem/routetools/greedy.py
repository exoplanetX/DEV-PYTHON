def greedy(route_list):
    route=[]
    for i in range(city_size):
        route.append(route_list.find(i))
    #route.append([0])
    return route
