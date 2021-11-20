import sys
import datetime
from FH_Operator import stdCrossover as stdc, stdMutation as stdm, stdRepairChromosome as stdr
from FH_LocationProblem import FH_geneticOperator as genetic
from FH_RoutingCost import BinaryValueObjective as obj, IndexDifferenceObjective as obji
from FH_PopulationInitiator import PopulationGenerator
from readvrplib import read_vrplib_file
import cvrp_io
#from RichBoss import RichBoss
from RichBossMultiDepotv3 import RichBoss as MDRichBoss,assignmentObjective as assignObj,assignmentAvgObjective as assignAvgObj,distanceOfEveryNodeFromDepot as distObj
from RichBossMultiDepot import totalTimeSacrificeObjective as totalDistObj
from problemPlotter import routePlotter, changeListToTour2

#setting initial values 
total_candidate_locations_size , FH_count_for_set_up, FH_generation_population_size, FH_steady_parent_count = 30,5,50,2
# crossover rate, mutation rate, generation time
r_cross,r_mut, n_iter = 0.8, 0.033, 100 # mutation 1 / total_candidate_locations_size
# crossocer and mutarion operators
stdc_op,stdm_op,stdr_op = stdc(r_cross),stdm(r_mut),stdr(FH_count_for_set_up)
 
#objective function (richBossMultidepotV2) ..
file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n101-k10.vrp"
#file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n101-k10 copy.vrp"
#file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n121-k7.vrp"
#file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\E-n51-k5.mdvrp"
problem = cvrp_io.read_TSPLIB_CVRP(file_name)
costn = problem.distance_matrix.tolist()
demands = problem.customer_demands
#capacity = problem.capacity_constraint
capacity = 99999 # no_capacity
selectedListMinRatio = 1.2
vehicle_num_in_depot = 1 
sacObj = assignAvgObj#nodeTotal#routeTotal #nodeTotal #routeTotal # routeTotal  #nodeTotal #routeTotal #nodeTotal #routeTotal # depotTotal #nodeTotal
mergeObj,fitnessObj = totalDistObj, distObj #nodeTotal#routeTotal #nodeTotal #routeTotal # routeTotal  #nodeTotal #routeTotal #nodeTotal #routeTotal # depotTotal #nodeTotal
reservedDList = [32,35,39,  13,15,12,    30,25,23,   5,4,9,  40,46,52,  60,54,59,   72,66,63,   80,71,81,   82,85,90,  98,100,92]
objective = MDRichBoss(costn, vehicle_num_in_depot, demands, capacity, sacObj, problem.coordinate_points,reservedDList,mergeObj,selectedListMinRatio,fitnessObj)

#pop = PopulationGenerator(total_candidate_locations_size , FH_count_for_set_up, FH_generation_population_size).getInitPop3(reservedDList, objective)
pop = PopulationGenerator(total_candidate_locations_size , FH_count_for_set_up, FH_generation_population_size).getInitPop2(objective)
best, best_eval, best_routes, best_depot_list, best_List = genetic(n_iter, objective, pop).runAlgorithm(stdc_op, stdm_op, stdr_op, FH_steady_parent_count)
objective.printPlotSolution2(problem.coordinate_points, best_routes,best_List)
