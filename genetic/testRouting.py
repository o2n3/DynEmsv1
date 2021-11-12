from numpy import append
from readvrplib import read_vrplib_file
import cvrp_io
#from RichBoss import RichBoss
from RichBossMultiDepot import RichBoss as MDRichBoss,nodesAccessTimeSacrificeObjective as nodeTotal, depotAccessTimeSacrificeObjective as depotTotal
from RichBossMultiDepot import totalTimeSacrificeObjective as routeTotal
from problemPlotter import routePlotter, changeListToTour


def decodeCostnForRichBoss(costn, route, depot_node):
    map=[]
    costx =[]
    map.append(depot_node)
    
    costx.append([])
    costx[0].append([])
    costx[0][0] = 0
    i=0
    for i,node in enumerate(route):        
        map.append(node)
        costx[0].append(costn[map[0]][map[i+1]])
    
    for i,node in enumerate(route):
        costx.append([])
        for nodey in route:
            None #costx[map]
            
    None

def encodeRoutesForPlotting(routes, map):
    None

if __name__ == '__main__':

    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\A-n32-k5.vrp"
    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n101-k10.vrp"
    file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n101-k10 copy.vrp"
    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n121-k7.vrp"
    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\E-n51-k5.mdvrp"
    problem = cvrp_io.read_TSPLIB_CVRP(file_name)
    costn = problem.distance_matrix.tolist()
    demands = problem.customer_demands
    capacity = problem.capacity_constraint
    # capacity = 250 #10000
    capacity = 1500
    depotList = [0] #[12,40, 74, 80, 100]
    route_num = 3 #len(depotList)    
    # print(costn)
    # for c in costn:
    #    print(c)
    sacObj = depotTotal #nodeTotal #routeTotal # routeTotal  #nodeTotal #routeTotal #nodeTotal #routeTotal # depotTotal #nodeTotal
    rich = MDRichBoss(costn, route_num, demands, capacity, depotList, sacObj, problem.coordinate_points)
    routes = rich.run()
    rich.printPlotSolution(problem.coordinate_points, routes,depotList)

    depod_node = 20
    r1 =[23, 26, 28, 30, 20, 21, 22, 25, 24, 27, 29, 32, 33, 31, 35, 37, 38, 34, 36, 39]
    costnx,map = decodeCostnForRichBoss(costn.copy(),r1,depod_node)



    r2 = [0, 67, 65, 63, 62, 74, 72, 61, 64, 66, 69, 68, 40, 41, 44, 42, 43, 47, 49, 52, 50, 51, 46, 45, 48, 59, 57, 55, 54, 53, 60, 58, 56, 0] 
    r3 = [0, 85, 88, 91, 89, 90, 87, 86, 84, 83, 82, 71, 76, 78, 81, 80, 79, 77, 73, 70, 0] 
    r4 = [0, 10, 11, 8, 9, 7, 5, 3, 4, 6, 75, 1, 2, 98, 96, 95, 94, 93, 92, 99, 100, 97, 0] 

        

    """
    vhicle_num = 3
    for r in routes:
        costnx,map = decodeCostnForRichBoss(costn.copy(),r,depotList)
        rich = MDRichBoss(costnx, vhicle_num, demands, capacity, depotList, sacObj, problem.coordinate_points)
        mdRoutes = rich.run()
        mdRoutes2 =  encodeRoutesForPlotting(mdRoutes.copy(),map)
    """
    
    totalDist = 0
    tours = []
    for r in routes:
        totalDist += rich.depotTotal(costn, r)
        print(r, "-> total distance -access time:", rich.calculateNewAccessTime(r, len(r)-1), "-", rich.calculateNewAccessTime(r, len(r)-2),
              ' total demands:', rich.calculateTotalDemands(r)
              )
        tours.append(changeListToTour(r))
    
    """
    print('totalDist', totalDist, 'totalDist/route:', totalDist/len(routes)+1)
    rp = routePlotter(problem.coordinate_points, len(routes))
    #route1 = [[(0,27), (27, 29),(29, 15), (15, 22), (22, 9), (9, 0)]]
    rp.plotRoute(tours)
    """
