
"""
RichBoss v1 pseudo code (onini 13.05.2021)

Rich Boss aproach
intuition: VRP Company have a "Rich" boss. And boss buy a vehicle for every clients on every <depots>. 
            Then things are starting to go bad by one by one and our boss isnt "Rich" anymore. 
           In every iteration "Rich" boss loses one vehicle (sacrificing a vehicle itself in evry iteration). Sacrificed vehicle's route remove from network and other (nearest) expand itself.
           Iteration goes until boss have an optimum vehicle number.
           Rich Boss Time: Beginning of algorithm. In the first iteration, "Rich" boss have vehicles = number of clients in that time.
a- Let Number of clients is "C"
b- Let the number of  Depot is d and label is "Dd"
c- Total number of nodes is "N" = C + d (d Depots)
d- Let we have "V*d" vehicle and we want obtain same number of routes
for optimum routing
e- Let "r" is a node list for a route, and r(n) is a route list.
e- Let sacrifices matrix "Rsac" contains access times for every active routes
when they sacrifice theirselfes for each other.
f- Let "Rsac+" matrix is additional access times when routes sacrifices itself. obtained from rsac
**g** - If we chose a sacrificed route to join others we also choose a sacrificed depot.

In Future..
    For capacitated VRP in the first phase richBoss run the above steps and clients have a routes.
    Then max capacitated route clients searchs the RSac for alternati ve routes for lower capacity.
    Insertion heuristics can be used.
    This steps for the balance.  


begin
    Create a two-dimentional cost matrix CostN(N+1) that contains travel costs between nodes
    Initialize number of Routes routes R = C
    Initialize  the first routes r(n) for every clients c(n)  
    in Routes matrix. r(n): D -> c(n) -> D 

    While V < R do: /*while number of Route is more than n.o. vehicle decrease number of route by 1*/
        /*calculating Rsac*/
        for every index x in  R: 
            sac = x /*ith route is sacrifice itself*/
            for every index y in R:
                newRouting = addToRoot(r(y),r(sac))  /*join r(sac) to r(y) */
                newAccessTime = calculateNewAccess(newRouting,r(sac)) /*objectiveValue = calculateObjForNewRoutin(newRouting) */
                Rsac[y][sac] = newAccessTime, newRouting /*Rsac[y][sac] = objectiveValue*/
            end for sacrifice column
        end for sacrifice row 
        y,sac,newRouting = selectSacrificeRoute(Rsac)   /*select min access time from Rsac matrix*/
        removeFromRoutes(r(sac)) /*sacrifice route removing*/     
        r(y) = newRouting /*expanding route*/
        R = R-1 /*now we have R-1 routes after sacrifice removing*/
    End While;
    return r for vehicles (R=V)
end RichBoss.
"""
from typing import Dict, List, NoReturn
from problemPlotter import routePlotter,changeListToTour
import cvrp_io

def nodesAccessTimeSacrificeObjective(costn, route:List)->int:
    accessTime=0
    sacrificedLastIndex = len(route)-1-1
    for nodeInd in range(1,sacrificedLastIndex,1):  #range(len(route)):
        node1, node2 = route[nodeInd], route[nodeInd+1]
        if node1 > 0 :                
            accessTime += costn[node1][node2]        
    return accessTime

def depotAccessTimeSacrificeObjective(costn, route:List)->int:
    accessTime=0
    sacrificedLastIndex = len(route)-1-1
    for nodeInd in range(sacrificedLastIndex):  #range(len(route)):
        node1, node2 = route[nodeInd], route[nodeInd+1]
        accessTime += costn[node1][node2]
    return accessTime

def totalTimeSacrificeObjective(costn,route:List)->int:
    accessTime=0
    for nodeInd in range(len(route)-1):  #range(len(route)):
        node1, node2 = route[nodeInd], route[nodeInd+1]
        accessTime += costn[node1][node2]
    return accessTime

def costCompare(value1, value2)->bool:
    if value1 > value2:
        return True
    else:
        return False

class RichBoss:

    def __init__(self, costn:List, V:int, demands:list, capacity, depotList:List, sacrificeObjective, coordinate_points) -> None:
        self.costn = costn
        self.V = V # number of vehicle and expected number of routes
        self.D = 1 # number of depot        
        self.C = len(costn)-self.D # Total number of nodes is "N" = C + 1 (1 Depot)        
        self.r = self.getRichBossTimeRoutes() # route list
        self.demands = demands
        self.capacity = capacity
        self.depotList = depotList
        self.sacrificeObjective = sacrificeObjective
        self.coordinate_points = coordinate_points

    # r(n): D -> c(n) -> D 
    def getRichBossTimeRoutes(self)->List:
        #return [[[0,x+1],[x+1,0]] for x in range(self.C)]
        return [[0,x+1,0] for x in range(self.C)]

    def run(self)->List:
        R = self.C #Initialize number of Routes routes R = C
        self.RsacList =[]
        while self.V < R: # while number of Route is more than number of vehicle decrease number of route by 1
            self.Rsac =[]
            #calculating Rsac; sacrificing costs matrix
            #for every index x in R calculate, 
            for sac in range(R):    
                self.Rsac.append([])                                                
                for y in range(R): #for every index y  in R:
                    self.Rsac[sac].append([])
                    if sac == y: # same route dont calculate
                        newAccessTime = self.sacrificeObjective(self.costn, self.r[sac]) #extra minus for depot
                        newTotalDemands = self.calculateTotalDemands(self.r[sac])
                        self.Rsac[sac][y] = {'newAccessTime':newAccessTime,'newRouting':self.r[y].copy(),'newTotalDemands':newTotalDemands} 
                    else:
                        newRouting = self.addToRoute(self.r[y].copy(),self.r[sac]) #find the route if sac.th route is sacrifice itself to route r[y]
                        #newAccessTime = self.calculateNewAccessTime(newRouting.get('newRoute'),int(newRouting.get('expandedIndex'))+int(newRouting.get('sacrifiedLastIndex'))-1) #objectiveValue = calculateObjForNewRoutin(newRouting)
                        newAccessTime = self.sacrificeObjective(self.costn, newRouting.get('newRoute')) 
                        newTotalDemands = self.calculateTotalDemands(newRouting.get('newRoute'))
                        depotNumInRoute = self.calculateDepotNum(newRouting.get('newRoute'))
                        #Rsac[y][sac] = newAccessTime, newRouting /*Rsac[y][sac] = objectiveValue*/
                        self.Rsac[sac][y] = {'newAccessTime':newAccessTime,'newRoute':newRouting.get('newRoute'), 'newTotalDemands':newTotalDemands, 'depotNumInRoute':depotNumInRoute}                                            
            select = self.selectSacrificeRoute(self.Rsac)   # #y,sac,newRouting = selectSacrificeRoute(Rsac), select min access time from Rsac matrix
            if select.get('minVal') == 99999: #no route alternative may be constraintcan be 
                print ('minval 99999 check constraint')                
                return self.r 
            self.updateWithExpandedRoute(select.get('expandInd'),select.get('sacInd')) # r(y) = newRouting /*expanding route*/
            self.removeFromRoutes(select.get('sacInd'))  #sacrifice route removing
            #self.printPlotSolution(self.coordinate_points, self.r,self.depotList)            

            R = R-1 #now we have R-1 routes after sacrifice removing
            if R < 5:
                print ("R:",R) ## debug için

            self.RsacList.append(self.Rsac.copy())
        #End While;
        return self.r #for vehicles (R=V)

    def findClosestNodeInRoute(self,route,clientFirstLastNodeID)->Dict:
        min = 9999999999
        for x in range(len(route)-1):
            #print (x,x+1,route[x],route[x+1], "costn->", self.costn[route[x]][route[x+1]])            
            if x != 0: # and self.costn[route[x]][clientFirstLastNodeID] < min: for know appent to end
                min = self.costn[route[x]][clientFirstLastNodeID]
                retDict = {'closestNodeIndex':x,'closestNode':route[x],'clientFirstIndex':clientFirstLastNodeID,'minimumEdgeValue':min}
        return retDict
    """
    def addToRoute(self,expanded:List, sacrificed:List)->Dict:
        #iki route u birbirlerine başından yada sonundan bağlıyoruz, hangisi yakın ise, şimdilik ortadan değil
        sacInd = self.getFirstAndLastNodeID(sacrificed)
        expandInd = self.getFirstAndLastNodeID(expanded)
        if sacInd.get('first') == sacInd.get('last'): # is sacrificed have one node
            closest = self.findClosestNodeInRoute(expanded,sacInd.get('first'))
        else:
            # find the closest edges 
            closestToFirst = self.findClosestNodeInRoute(expanded,sacInd.get('first'))
            #closestToLast = self.findClosestNodeInRoute(expanded,sacInd.get('last'))

            closest = closestToFirst # todo: first için de olabilir
        expanded[closest.get('closestNodeIndex')+1:] = sacrificed[1:]
        return {'newRoute':expanded,'expandedIndex':closest.get('closestNodeIndex')+1, 'sacrifiedFirstIndex':sacInd.get('first'), 'sacrifiedLastIndex':sacInd.get('last')}
    """
    def addToRoute(self,expanded:List, sacrificed:List)->Dict:
        #iki route u birbirine merge ediyoruz, fermuar gibi

        expanded = self.mergeRoutesWithNearestEdge(expanded, sacrificed)
        return {'newRoute':expanded}

    def getFirstAndLastNodeID(self, route:List)->Dict:
        return {'first':1,'last':len(route)-2} # why 2' : -1 is for depot node and -1 for List index Ex:[0,1,0] len = 3, 1 st index is 1
    
    def calculateNewAccessTime(self,route:List, sacrificedLastIndex:int)->int:
        accessTime=0
        for nodeInd in range(1,sacrificedLastIndex,1):  #range(len(route)):
            node1, node2 = route[nodeInd], route[nodeInd+1]
            #if node1 > 0 :
            accessTime += self.costn[node1][node2]        
        return accessTime

    def calculateNewAccessTimeTotal(self,route:List, sacrificedLastIndex:int)->int:
        accessTime=0
        for nodeInd in range(sacrificedLastIndex):  #range(len(route)):
            node1, node2 = route[nodeInd], route[nodeInd+1]
            accessTime += self.costn[node1][node2]
        return accessTime

    def calculateTotalDemands(self,route:List)->float:
        totalDemands=0
        for nodeInd in route:  #range(len(route)):
            totalDemands += self.demands[nodeInd]
        return totalDemands

    def calculateDepotNum(self,route:List)->int:
        depotNum=0
        for nodeInd in route:  
            if nodeInd in self.depotList:
                depotNum += 1
        return depotNum

    def selectSacrificeRoute(self,rsac)->Dict:
        rsacPlus = self.generateRsacPlus(rsac)
        return self.selectMinFromRsacPlus(rsacPlus)

    def generateRsacPlus(self,rsac)->List:
        rsacPlus = []        
        for x,sacList in enumerate(rsac):
            rsacPlus.append([])
            for y,newRouting  in enumerate(sacList):
                rsacPlus[x].append([])
                rsacPlus[x][y]= {#'plusAccessTime' : rsac[x][y].get('newAccessTime') -rsac[x][x].get('newAccessTime'),
                                 'plusAccessTime' : rsac[x][y].get('newAccessTime') ,
                                 'totalDemands' : newRouting.get('newTotalDemands'),
                                 'depotNumInRoute':newRouting.get('depotNumInRoute')
                }
        return rsacPlus

    def selectMinFromRsacPlus(self, rsacPlus:List)->Dict:
        minVal, minValx, minValy = 99999,0,0
        for indx,accessPlusList in enumerate(rsacPlus):
            for indy in range(len(accessPlusList)):                
                if indx != indy and rsacPlus[indx][indy].get('plusAccessTime') < minVal and rsacPlus[indx][indy].get('totalDemands')  <= self.capacity and rsacPlus[indx][indy].get('depotNumInRoute')  <= 1:
                    minVal, minValx, minValy, totalDemands = rsacPlus[indx][indy].get('plusAccessTime'),indx,indy, rsacPlus[indx][indy].get('totalDemands') 
        return {'minVal':minVal, 'sacInd':minValx, 'expandInd':minValy, 'totalDemands':totalDemands}

    def updateWithExpandedRoute(self, expandInd, sacId):
        self.r[expandInd] = self.Rsac[sacId][expandInd].get('newRoute')

    def removeFromRoutes(self,sacInd)->None:        
        self.r.pop(sacInd)

    def mergeRoutes(self,primaryList:List, primaryFirst, primaryLast, fromList:List, fromListFirst, fromLast)->List:
        primaryInd, primaryFinished = primaryFirst, primaryFirst==primaryLast # False
        fromInd, fromFinished = fromListFirst, False        
        while not primaryFinished or not fromFinished:

            if  fromFinished  and not primaryFinished:
                primaryInd += 1      
            elif not fromFinished  and  primaryFinished:
                primaryList.insert(primaryInd+1,fromList[fromInd])
                fromInd += 1
                primaryInd += 1
            else:
                primaryNode = primaryList[primaryInd]
                primaryNode2 = primaryList[primaryInd+1]
                fromNode =  fromList[fromInd]
                #print('self.costn[',primaryNode,'][',primaryNode2,']:',self.costn[primaryNode][primaryNode2])
                #print('self.costn[',primaryNode,'][',fromNode,']:',self.costn[primaryNode][fromNode])
                if  self.costn[primaryNode][primaryNode2] <= self.costn[primaryNode][fromNode]:
                    primaryInd += 1
                else:
                    primaryList.insert(primaryInd+1,fromList[fromInd])
                    fromInd += 1
                    primaryInd += 1

            if fromInd > fromLast:
                fromFinished = True
            if primaryInd == primaryLast :
                primaryFinished = True                

        return {'mergedRoute' :primaryList, 'totalAccess': self.calculateNewAccessTime(primaryList,len(primaryList)-1-1)}

    #merges routes with nearest
    def mergeRoutesWithNearestEdge(self, expanded:List, sacrificed:List)->List:
        # first 
        expandInd = self.getFirstAndLastNodeID(expanded)
        sacInd = self.getFirstAndLastNodeID(sacrificed)
        # there are four possibility for optimum merge because lists are sorted
        merge = []
        merge1 =self. mergeRoutes(expanded.copy(), expandInd.get('first'),expandInd.get('last'), sacrificed, sacInd.get('first'),sacInd.get('last'))
        merge.append(merge1)
        ex_rev = [ele for ele in reversed(expanded)]
        expandInd = self.getFirstAndLastNodeID(ex_rev)
        #rex = rex.copy()
        merge2 =self. mergeRoutes(ex_rev.copy(), expandInd.get('first'),expandInd.get('last'), sacrificed, sacInd.get('first'),sacInd.get('last'))
        merge.append(merge2)
        merge3 =self. mergeRoutes(sacrificed.copy(), sacInd.get('first'),sacInd.get('last'), expanded, expandInd.get('first'),expandInd.get('last'))
        merge.append(merge3)
        sac_rev = [ele for ele in reversed(sacrificed)]
        sacInd = self.getFirstAndLastNodeID(sac_rev)

        merge4 =self. mergeRoutes(sac_rev.copy(), sacInd.get('first'), sacInd.get('last'), expanded, expandInd.get('first'),expandInd.get('last'))
        merge.append(merge4)
        bestList=[]
        bestVal = 99999
        for mergeList in merge:
            if mergeList.get('totalAccess')<bestVal:
                bestList,bestVal = mergeList.get('mergedRoute'),mergeList.get('totalAccess')
        return bestList
    
    def printPlotSolution(self,coordinate_points, routes, depots):
        totalDist = 0
        tours =[]
        for r in routes:
            totalDist += self.calculateNewAccessTimeTotal(r,len(r)-1)
            print(r,"-> total distance -access time:",self.calculateNewAccessTimeTotal(r,len(r)-1),"-",self.calculateNewAccessTime(r,len(r)-2),
            ' total demands:',self.calculateTotalDemands(r)
            )
            tours.append(changeListToTour(r))
            
        print('totalDist',totalDist, 'totalDist/route:',totalDist/len(routes)+1)
        rp = routePlotter(coordinate_points,len(routes))
        #route1 = [[(0,27), (27, 29),(29, 15), (15, 22), (22, 9), (9, 0)]]
        rp.plotRoute(tours,depots)

if __name__ == '__main__':
    """
    costn = [[0, 5, 8, 10, 3],
             [5, 0, 7, 15, 3],
             [8, 7, 0, 12,11],
             [10,15,12, 0, 9],
             [3, 3, 11, 9, 0]
            ]    
    demands = [0, 1.1, 0.7, 0.8, 0.4,2.1, 0.4, 0.8, 0.1,0.5,0.6] #customer demands
    capacity = 3.5
    """
    #The life and times of the Savings Method for Vehicle Routing Problems makalesindeki örnek
    
    #           0       1     2       3     4     5      6       7      8      9      10
    costn = [[ 0.00, 14.04, 14.21, 20.40, 22.09, 13.34,  5.66, 13.60, 13.60, 19.10, 18.11], #0
             [14.04,  0.00,  8.54, 23.26, 25.94, 20.81, 18.68, 24.17, 26.57, 30.46, 32.14], #1   
             [14.21,  8.54, 00.00, 29.83, 32.28, 14.56, 19.85, 19.10, 27.80, 25.32, 31.02], #2
             [20.40, 23.26, 29.83, 00.00,  2.83, 33.73, 17.89, 33.24, 19.21, 37.59, 28.43], #3
             [22.09, 25.94, 32.28,  2.83, 00.00, 35.36, 18.97, 34.48, 19.10, 38.48, 28.28], #4
             [13.34, 20.81, 14.56, 33.73, 35.36, 00.00, 17.03,  5.39, 22.47, 11.00, 21.21], #5
             [ 5.66, 18.68, 19.85, 17.89, 18.97, 17.03, 00.00, 15.52,  8.06, 19.72, 14.14], #6
             [13.60, 24.17, 19.10, 33.24, 34.48,  5.39, 15.52, 00.00, 19.24,  6.32, 16.40], #7
             [13.60, 26.57, 27.80, 19.21, 19.10, 22.47,  8.06, 19.24, 00.00, 21.21,  9.22], #8
             [19.10, 30.46, 25.32, 37.59, 38.48, 11.00, 19.72,  6.32, 21.21, 00.00, 15.52], #9
             [18.11, 32.14, 31.02, 28.43, 28.28, 21.21, 14.14, 16.40,  9.22, 15.52, 00.00] #10
            ]    
    demands = [0, 1.1, 0.7, 0.8, 0.4,2.1, 0.4, 0.8, 0.1,0.5,0.6] #customer demands
    capacity = 3.5    
    route_num = 3
    
    #https://web.mit.edu/urban_or_book/www/book/chapter6/6.4.12.html örneği, 2. route için bulamadı capacityden dolayı, 3 route için daha iyi buluyor
    """
    costn = [[ 0.00, 25, 43, 57, 43, 61,  29, 41, 48, 71], #0
             [25,  0.00,  29, 34, 43, 68, 49, 66, 72, 91], #1   
             [43,  29, 00.00, 52, 72, 96, 72, 81, 89, 114], #2
             [57, 34, 52, 00.00,  45, 71, 71, 95, 99, 108], #3
             [43, 43, 72,  45, 00.00, 27, 36, 65, 65, 65], #4
             [61, 68, 96, 71, 27, 00.00, 40,  66, 62, 46], #5
             [29, 49, 72, 71, 36, 40, 00.00, 31,  31, 43], #6
             [41, 66, 81, 95, 65,  66, 31, 00.00, 11,  46], #7
             [48, 72, 89, 99, 65, 62,  31, 11, 00.00, 36], #8
             [71, 91, 114, 108, 65, 46, 43,  46, 36, 00.00] #9             
            ]    
    demands = [0, 4, 6, 5, 4,7,3, 5, 4,4] #customer demands    
    capacity = 16
    route_num = 3
    """

    file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n101-k10.vrp"
    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n121-k7.vrp"
    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\E-n51-k5.mdvrp"
    problem = cvrp_io.read_TSPLIB_CVRP(file_name)
    costn = problem.distance_matrix.tolist()
    demands = problem.customer_demands
    capacity = problem.capacity_constraint
    # capacity = 250 #10000
    capacity = 10000
    route_num = 4
    depotList =[22,15]
    # print(costn)
    # for c in costn:
    #    print(c)
    sacObj = nodesAccessTimeSacrificeObjective # routeTotal  #nodeTotal #routeTotal #nodeTotal #routeTotal # depotTotal #nodeTotal
    rich = RichBoss(costn, route_num, demands, capacity, depotList, sacObj)
    num = rich.calculateDepotNum([0,1,15,22,2,3])
    print("num:",num)
    #routes = rich.run()
    #rich.printPlotSolution(problem.coordinate_points, routes)



    
    """
    #rich.addToRoute(rich.r[2-1],rich.r[1-1])
    #rich.findClosestNodeInRoute(rich.r[2-1],1)
    #rich.findClosestNodeInRoute(rich.r[3-1],1)
    #rich.findClosestNodeInRoute(rich.r[4-1],1)

    # a[3:3] = ['a','b'] 
    """