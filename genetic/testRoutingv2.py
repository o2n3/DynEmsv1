from numpy import append
from readvrplib import read_vrplib_file
import cvrp_io
#from RichBoss import RichBoss
from RichBossMultiDepotv2 import RichBoss as MDRichBoss
from RichBossMultiDepot import totalTimeSacrificeObjective as routeTotal, nodesAccessTimeSacrificeObjective as nodeTotal, depotAccessTimeSacrificeObjective as depotTotal
from problemPlotter import routePlotter, changeListToTour




if __name__ == '__main__':
    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n101-k10.vrp"
    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n101-k10 copy.vrp"
    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n121-k7.vrp"
    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\E-n51-k5.mdvrp"
    file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\P-n16-k8.vrp"
    problem = cvrp_io.read_TSPLIB_CVRP(file_name)
    costn = problem.distance_matrix.tolist()
    demands = problem.customer_demands
    capacity = problem.capacity_constraint
    capacity = 99999
    vehicle_num_in_depot =4
    sacObj = routeTotal#routeTotal#nodeTotal#routeTotal #nodeTotal #routeTotal # routeTotal  #nodeTotal #routeTotal #nodeTotal #routeTotal # depotTotal #nodeTotal

    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n101-k10.vrp"
    #reservedDList = [32,35,39,  13,15,12,    30,25,23,   5,4,9,  40,46,52,  60,54,59,   72,66,63,   80,71,81,   82,85,90,  98,100,92]    

    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\E-n51-k5.mdvrp"
    #reservedDList =[0]
    #d = [0]

    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n101-k10 copy.vrp"
    reservedDList =[0]
    d = [0]

    rich = MDRichBoss(costn, vehicle_num_in_depot, demands, capacity, sacObj, problem.coordinate_points,reservedDList)
    #a = rich.value([0, 5])
    #print("a1:",a)
    #d = [35, 13, 25, 23, 60, 59, 63, 71, 90, 100]
    #d = [2, 3, 9, 10, 14, 16, 20, 23, 25, 27]

    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\E-n51-k5.mdvrp"
    reservedDList =[0]
    d = [0]
    

    #>2177, new best f([0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0])([1, 3, 7, 10, 17, 19, 20, 23, 25, 28])([35, 13, 25, 4, 59, 66, 63, 81, 85, 100])  = 48.000000
    a,r,dl = rich.value(d)
    print("a4:",a)
    print("dl:",dl)
    rich.printPlotSolution(problem.coordinate_points,r,dl)
    
    #routes = rich.run(depotList)
    #rich.printPlotSolution(problem.coordinate_points, routes,depotList)
    """
    depod_node = 20
    r1 =[23, 26, 28, 30, 20, 21, 22, 25, 24, 27, 29, 32, 33, 31, 35, 37, 38, 34, 36, 39]
    costnx,map = decodeCostnForRichBoss(costn.copy(),r1,depod_node)
    r2 = [0, 67, 65, 63, 62, 74, 72, 61, 64, 66, 69, 68, 40, 41, 44, 42, 43, 47, 49, 52, 50, 51, 46, 45, 48, 59, 57, 55, 54, 53, 60, 58, 56, 0] 
    r3 = [0, 85, 88, 91, 89, 90, 87, 86, 84, 83, 82, 71, 76, 78, 81, 80, 79, 77, 73, 70, 0] 
    r4 = [0, 10, 11, 8, 9, 7, 5, 3, 4, 6, 75, 1, 2, 98, 96, 95, 94, 93, 92, 99, 100, 97, 0]   
    vhicle_num = 3
    for r in routes:
        costnx,map = decodeCostnForRichBoss(costn.copy(),r,depotList)
        rich = MDRichBoss(costnx, vhicle_num, demands, capacity, depotList, sacObj, problem.coordinate_points)
        mdRoutes = rich.run()
        mdRoutes2 =  encodeRoutesForPlotting(mdRoutes.copy(),map)
    """
    """
    totalDist = 0
    tours = []
    for r in routes:
        #totalDist += rich.depotTotal(costn, r)
        print(r, "-> total distance -access time:", rich.calculateNewAccessTime(r, len(r)-1), "-", rich.calculateNewAccessTime(r, len(r)-2)              
              )
        tours.append(changeListToTour(r))
    """
    """
    print('totalDist', totalDist, 'totalDist/route:', totalDist/len(routes)+1)
    rp = routePlotter(problem.coordinate_points, len(routes))
    #route1 = [[(0,27), (27, 29),(29, 15), (15, 22), (22, 9), (9, 0)]]
    rp.plotRoute(tours)
    """
