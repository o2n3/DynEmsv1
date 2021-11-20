from numpy import append
from readvrplib import read_vrplib_file
import cvrp_io
#from RichBoss import RichBoss
from RichBossMultiDepotv3 import RichBoss as MDRichBoss,assignmentObjective as assignObj, assignmentAvgObjective as assignAvgObj,assignmentObjective2 as assignObj2,distanceOfEveryNodeFromDepot as distObj
from RichBossMultiDepot import totalTimeSacrificeObjective as totalDistObj
from problemPlotter import routePlotter, changeListToTour


if __name__ == '__main__':

    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\A-n32-k5.vrp"
    file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n101-k10.vrp"
    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n101-k10 copy.vrp"
    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n121-k7.vrp"
    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\E-n51-k5.mdvrp"
    problem = cvrp_io.read_TSPLIB_CVRP(file_name)
    costn = problem.distance_matrix.tolist()
    demands = problem.customer_demands
    capacity = problem.capacity_constraint
    # capacity = 250 #10000
    capacity = 99999
    selectedListMinRatio = 1.5
    #depotList = [4,8] #
    depotList = [12,40, 74, 80, 100]
    #depotList = [12,37, 40,27,9, 74, 80,82,56, 100]
    route_num = 1 #len(depotList)    
    # print(costn)
    # for c in costn:
    #    print(c)
    sacObj = assignAvgObj #assignObj2 #nodeTotal #routeTotal # routeTotal  #nodeTotal #routeTotal #nodeTotal #routeTotal # depotTotal #nodeTotal
    mergeObj = totalDistObj
    fitnessObj = distObj
    reserved = []
    rich = MDRichBoss(costn, route_num, demands, capacity, sacObj, problem.coordinate_points,reserved,mergeObj,selectedListMinRatio,fitnessObj)
    routes = rich.run(depotList)
    rich.printPlotSolution2(problem.coordinate_points, routes,depotList)

    
