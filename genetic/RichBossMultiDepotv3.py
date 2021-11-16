
"""
MultiDepotRichBoss v2 pseudo code (onini 29.09.2021)

Rich Boss aproach
intuition: VRP Company have a "Rich" boss. And boss assign a vehicle (ambulance) for every clients on every <depots> (hospitals). 
           Then things are starting to go bad by one by one and our boss isnt "Rich" anymore. 
           In every iteration "Rich" boss loses one vehicle (sacrificing a vehicle itself in evry iteration). Sacrificed vehicle's route remove from network and other (nearest) expand itself.
           Iteration goes until boss have an real vehicle number.
           Rich Boss Time: Beginning of algorithm. In the first iteration, "Rich" boss have vehicles = number of clients in that time.

Route means the set of nodes that assign to depot ****
a- Let Number of clients is "C"
b- Let the number of  Depot is D and label is "Dd"
c- Total number of nodes is "N" = C + D (D Depots)
d- Let we have "V*D" vehicle and we want obtain same number of routes
for optimum routing
e- Let "R" is a node list for a route, and r(d)(n) is a route list for dth depot.
e- Let sacrifices matrix "Rsac(d)" contains access times for every active routes for depots
when they sacrifice theirselfes for each other.
f- Let "Rsac+(d)" matrix is used for selection according to objective. For ex: Additional access time.
g- If we chose a sacrificed route to join others we also choose a sacrificed depot. So if a R(d) selected for node(x) other 
Rsac matrix update itself
i- Depots have equal chances every depot take a route for every iteration
 


begin
    Create a two-dimentional cost matrix CostN(N+1) that contains travel costs between nodes
    Initialize number of Routes routes R = C
    Initialize  the first routes r(n) for every clients c(n)  
    in Routes matrix. r(n): D(i) -> c(n) -> D(i) 

    While V < R do: /*while number of Route is more than n.o. vehicle decrease number of route by 1*/      
        /*calculating Rsac*/
        for depot d in depotList: 
            for every index x in  R: 
                sac = x /*ith route is sacrifice itself*/
                for every index y in R:
                    newRouting(d) = addToRoute(d, r(y),r(sac))  /*join r(sac) to r(y) */
                    newObjValue(d) = calculateObjForNewRouting(newRouting(d)) /*objectiveValue = calculateObjForNewRoutin(newRouting) */
                    Rsac[d][y][sac] = newObjValue(d), newRouting(d)  /*Rsac[y][sac] = objectiveValue*/            
                end for sacrifice column
            end for sacrifice row 
        end for depot                
        y[],sac[],newRouting[] = selectSacrificeRoutes(Rsac)   /*select min access time from Rsac matrix for every depot NEW NEW */
        for d,sac in SacrificeList: 
            removeFromRoutes(sac) /*sacrifice route removing*/             
            r(d)(y) = newRouting(d) /*expanding route*/        
        R = R-1 /*now we have R-1 routes after sacrifice removing*/
    End While;
    return r for vehicles (R=V)
end RichBoss.
"""
from typing import Dict, List, NoReturn
from problemPlotter import routePlotter,changeListToTour
import cvrp_io
from operator import itemgetter

# every node in list visits and then vehicles came to depot. 010 + 020 + 030 + .. 
# plus add the nodes distance with each other
# TODO minus calculate the difference from average others distance from yours TODO..

def assignmentObjective(costn,nodeList:List, routes:List, sacrificedNodes:List, thisDepot=[], depotList:List=[])->int:
    depotNode=nodeList[0]    
    a = sum([costn[depotNode][n] for n in nodeList])    
    b = nodesAccessTimeSacrificeObjective(costn,nodeList)
    if sacrificedNodes is None:
        c = 0
    else:
        c = differenceFromAverageObjective(costn, sacrificedNodes, thisDepot, routes, depotList)        
    return a + b - c
#TODO
def differenceFromAverageObjective(costn, nodes, thisDepot, routes, depotList)->int:
    totalAvg = 0
    for node in nodes:
        if node not in depotList:
            depots = findNodeDepotsFromRoutes(node,routes)
            if thisDepot in depots:
                depots.remove(thisDepot)
            if len(depots)>0:
                avgDist = findAverageDistance(costn,node, depots, depotList)
                totalAvg += avgDist - costn[thisDepot][node]
    return totalAvg

#TODO
def findNodeDepotsFromRoutes(node, routes:List)->List:
    ret = []
    for depotID,rlist in enumerate(routes):
        for r in rlist:
            if node in r:
                ret.append(depotID)
    return ret
    #return [depotID for depotID in enumerate(routes) if node in routes[depotID]]    

#TODO
def findAverageDistance(costn,node, depots:List, depotList)->int:
    ret = [costn[node][depotList[depot]] for depot in depots]
    return sum(ret)/len(ret)


def nodesAccessTimeSacrificeObjective(costn, route:List)->int:
    accessTime=0
    sacrificedLastIndex = len(route)-1-1
    for nodeInd in range(1,sacrificedLastIndex,1):  #range(len(route)):
        node1, node2 = route[nodeInd], route[nodeInd+1]
        if node1 > 0 :                
            accessTime += costn[node1][node2]        
    return accessTime

def costCompare(value1, value2)->bool:
    if value1 > value2:
        return True
    else:
        return False

class RichBoss:

    def __init__(self, costn:List, V:int, demands:list, capacity, sacrificeObjective, coordinate_points,reservedDList) -> None:
        self.costn = costn
        self.V = V # number of vehicle and expected number of routes
        self.demands = demands
        self.capacity = capacity
        self.sacrificeObjective = sacrificeObjective
        self.coordinate_points = coordinate_points    
        self.reservedDList = reservedDList         
    # r(n): D -> c(n) -> D 
    def getRichBossTimeRoutes(self,d)->List:
        #return [[[0,x+1],[x+1,0]] for x in range(self.C)]
        return [[d,x,d] for x in range(self.C+self.D) if x not in self.depotList and x not in self.reservedDList]
        """
        ret =[]
        for x in range(self.C):
            if x+1 not in self.depotList:
                ret.append([d,x+1,d])
        return ret
        """
    def value(self, unMapDepotList:List):
        #print("depotList:",depotList)
        depotList = [self.reservedDList[i] for i in unMapDepotList]
        if len(depotList) == 0:
            return 9999999999,[],[]
        routes = self.run(depotList)
        totalDist = 0
        #routeDistList = []
        maxRouteDist = 0
        for di,d in enumerate(depotList):
            for r in routes[di]:
                routeDist = self.sacrificeObjective(self.costn,r,routes,None, di)
                if maxRouteDist < routeDist:
                    maxRouteDist = routeDist
                #routeDistList.append(routeDist)
                totalDist += routeDist
                #print(r,"-> total distance -access time:",routeDist)            
        """
        total_time = 0
        sortedMinList = sorted(routeDistList) 
        for i,distance in enumerate(sortedMinList):
            if i == 0:
                total_time = distance * len(sortedMinList)
            else: 
                total_time += distance - lastDistance
            lastDistance = distance
        """
        # max ile total farkı için
        return maxRouteDist,routes,depotList 
        #return totalDist,routes,depotList


    def run(self,depotList)->List:
        self.D = len(depotList)        
        self.R = self.V * self.D #number of total routes = # of vehicles
        self.C = len(self.costn)-self.D # Total number of nodes is "N" = C + 1 (1 Depot)           
        self.depotList = depotList        
        self.r = []
        for d in depotList:
            self.r.append(self.getRichBossTimeRoutes(d))    
            
        R = self.C #Initialize number of Routes routes R = C
        self.RsacList =[]
        while self.R < R: # while number of Route is more than number of vehicle decrease number of route by 1
            self.Rsac =[]
            for di, d in enumerate(self.depotList):
                self.Rsac.append([])
                if len(self.r[di])>self.V:                    
                    #calculating Rsac; sacrificing costs matrix
                    #for every index x in R calculate, 
                    for sac in range(len(self.r[di])):   
                        self.Rsac[di].append([])
                        for y in range(len(self.r[di])): #for every index y  in R:
                            self.Rsac[di][sac].append([])
                            if sac == y: # same route dont calculate
                                #1 newAccessTime = self.sacrificeObjective(self.costn, self.r[di][sac]) #itself
                                newAccessTime = 9999 #self.sacrificeObjective(self.costn, self.r[di][sac]) #itself
                                newTotalDemands = self.calculateTotalDemands(self.r[di][sac])
                                self.Rsac[di][sac][y] = {'newAccessTime':newAccessTime,'newRouting':self.r[di][y].copy(),'newTotalDemands':newTotalDemands} 
                            else:
                                newRouting = self.addToRoute(self.r[di][y].copy(),self.r[di][sac]) #find the route if sac.th route is sacrifice itself to route r[y]
                                #newAccessTime = self.calculateNewAccessTime(newRouting.get('newRoute'),int(newRouting.get('expandedIndex'))+int(newRouting.get('sacrifiedLastIndex'))-1) #objectiveValue = calculateObjForNewRoutin(newRouting)            
                                #newAccessTime1 = -1 * (self.sacrificeObjective(self.costn, self.r[di][y]) + self.sacrificeObjective(self.costn, self.r[di][sac]) - self.sacrificeObjective(self.costn, newRouting.get('newRoute')) )
                                newAccessTime = self.sacrificeObjective(self.costn, newRouting.get('newRoute'),self.r,self.r[di][sac],di, self.depotList) 
                                newTotalDemands = self.calculateTotalDemands(newRouting.get('newRoute'))
                                depotNumInRoute = self.calculateDepotNum(newRouting.get('newRoute'))
                                #Rsac[y][sac] = newAccessTime, newRouting /*Rsac[y][sac] = objectiveValue*/
                                self.Rsac[di][sac][y] = {'newAccessTime':newAccessTime,'newRoute':newRouting.get('newRoute'), 'newTotalDemands':newTotalDemands, 'depotNumInRoute':depotNumInRoute}
                #end if 
                    #end node list
                #end sacrifice node list
             #end depot list
            selectList = self.selectSacrificeRoute(self.Rsac)   # #y,sac,newRouting = selectSacrificeRoute(Rsac), select min access time from Rsac matrix

            for di,select in enumerate(selectList):
                if select.get('minVal') == 99999: #no route alternative may be constraintcan be 
                    print ('minval 99999 check constraint')                
                    #return self.r 
                if self.removeFromOtherRoutesCheck(select,selectList):
                    self.updateWithExpandedRoute(select.get('depotID'), select.get('expandInd'),select.get('sacInd')) # r(y) = newRouting /*expanding route*/                                
                    self.removeFromRoute(select.get('depotID'), select.get('sacInd'))  #sacrifice route removing                
            #TODO: 27062021 romove ederken diğer depotlardan da çıkarmalı, ama index thlikeli olur, node değerini arayarak çıkarmalı
            for select in selectList:
                # for itself now             
                #self.removeFromRoute(select.get('depotID'), select.get('sacInd'))  #sacrifice route removing                
                None
            for select in selectList:                
                removeNum = self.removeFromOtherRoutes(select)  #sacrifice route removing                

            R = sum(len(self.r[di]) for di,dv in enumerate(self.depotList)) # R-self.D #now we have R-1 routes after sacrifice removing
            #if R < 7: print ("R:",R) ## debug için
            #self.RsacList.append(self.Rsac.copy())
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

    def selectSacrificeRoute(self,rsac)->List:
        rsacPlus = self.generateRsacPlus(rsac)
        depotMinList = self.selectMinFromDepots(rsacPlus)
        return depotMinList

    def generateRsacPlus(self,rsac)->List:
        rsacPlus = [] 
        for d,sacMatrix in enumerate(rsac):       
            rsacPlus.append([])
            for x,sacList in enumerate(sacMatrix):
                rsacPlus[d].append([])
                for y,newRouting  in enumerate(sacList):
                    rsacPlus[d][x].append([])
                    rsacPlus[d][x][y]= {#'plusAccessTime' : rsac[x][y].get('newAccessTime') -rsac[x][x].get('newAccessTime'),
                                    'plusAccessTime' : rsac[d][x][y].get('newAccessTime') ,
                                    'totalDemands' : newRouting.get('newTotalDemands'),
                                    'depotNumInRoute':newRouting.get('depotNumInRoute'),
                                    'newRoute':newRouting.get('newRoute')
                    }
        return rsacPlus

    def selectMinFromDepots(self, rsacPlus:List)->List:
        minList = []
        for indd,accessPlusMatrix in enumerate(rsacPlus):
            a = self.selectMinFromRsacPlus(accessPlusMatrix)
            if a.get('minVal') != 99999:
                a['depotID']=indd
                minList.append(a)
            
        #sort with min value
        sortedMinList = sorted(minList, key=itemgetter('minVal')) 

        #check for dublicate selected nodes
        dublicateNodes = [] 
        rejectedList = []       
        for i,minValues in enumerate(sortedMinList):
            if i == 0:
                # first depot has min for all
                dublicateNodes.extend(minValues.get('newRoute'))               
            else:
                if len(set(minValues.get('newRoute')) & set(dublicateNodes))>0:
                    #opps we must change min node values
                    newMinValues = self.selectMinFromRsacPlus(rsacPlus[minValues.get('depotID')],dublicateNodes)
                    if newMinValues.get('minVal') != 99999:
                        newMinValues['depotID']=minValues.get('depotID')
                        #change 
                        sortedMinList[i] = newMinValues
                        dublicateNodes.extend(newMinValues.get('newRoute'))                    
                    else:
                        rejectedList.append(i)                        
                else:
                    dublicateNodes.extend(minValues.get('newRoute'))            
        for deli in reversed(rejectedList):
            sortedMinList.pop(deli)        
        return sortedMinList

    def selectMinFromRsacPlus(self, rsacPlus:List, dublicateNodes:List=[])->Dict:
        minVal, minValx, minValy,totalDemands,minRoute = 99999,0,0,0,[]
        
        if dublicateNodes == None:
            dublicateNodes = []
        for indx,accessPlusList in enumerate(rsacPlus):
            for indy in range(len(accessPlusList)):                
                if (indx != indy and rsacPlus[indx][indy].get('plusAccessTime') < minVal and 
                    rsacPlus[indx][indy].get('totalDemands')  <= self.capacity and 
                    len(set(rsacPlus[indx][indy].get('newRoute')) & set(dublicateNodes)) == 0):
                    minVal, minValx, minValy, totalDemands = rsacPlus[indx][indy].get('plusAccessTime'),indx,indy, rsacPlus[indx][indy].get('totalDemands') 
                    minRoute = rsacPlus[indx][indy].get('newRoute')
        return {'minVal':minVal, 'sacInd':minValx, 'expandInd':minValy, 'totalDemands':totalDemands, 'depotID':None, 'newRoute':minRoute}

    def updateWithExpandedRoute(self, di, expandInd, sacId):
        self.r[di][expandInd] = self.Rsac[di][sacId][expandInd].get('newRoute')

    def removeFromRoute(self,di, sacInd)->None:        
        self.r[di].pop(sacInd)
    

    def removeFromOtherRoutes(self,select)->int:
        removeNum = 0          
        for i,route in enumerate(self.r):
            removeList=[]
            if i != select.get('depotID'):
                for removeId, r in enumerate(route):
                    for selectedNode in select.get('newRoute'):
                        if selectedNode in r:
                            removeList.append(removeId)
            for ID in reversed(removeList):
                self.removeFromRoute(i,ID)
                removeNum +=1
        return removeNum

    def removeFromOtherRoutesCheck(self,select,selectList):
        removeNum = 0     
        removeList=[]
        for otherSelect in selectList:
            if select.get('depotID') != otherSelect.get('depotID'):
                for removeId, r in enumerate(self.r[select.get('depotID')]):
                    if len(set(r) & set(otherSelect.get('newRoute')))>0:           
                        removeList.append(removeId)                
            if len(self.r[select.get('depotID')]) - len(removeList) - 1  < self.V: # minus one for after merge case
                return False
        return True
        
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

        #return {'mergedRoute' :primaryList, 'totalAccess': self.calculateNewAccessTime(primaryList,len(primaryList)-1-1)}
        return {'mergedRoute' :primaryList, 'totalAccess': self.sacrificeObjective(self.costn,primaryList,self.r,None,None)}

    #merges routes with nearest
    def mergeRoutesWithNearestEdge(self, expanded:List, sacrificed:List)->List:
        # first 
        expandInd = self.getFirstAndLastNodeID(expanded)
        sacInd = self.getFirstAndLastNodeID(sacrificed)
        # try  four possibility for optimum merge because lists are sorted. 
        merge = []
        merge1 =self.mergeRoutes(expanded.copy(), expandInd.get('first'),expandInd.get('last'), sacrificed, sacInd.get('first'),sacInd.get('last'))
        merge.append(merge1)

         
        # ex_rev = [ele for ele in reversed(expanded)]
        # expandInd = self.getFirstAndLastNodeID(ex_rev)
        # #rex = rex.copy()
        # merge2 =self. mergeRoutes(ex_rev.copy(), expandInd.get('first'),expandInd.get('last'), sacrificed, sacInd.get('first'),sacInd.get('last'))
        # merge.append(merge2)
        # merge3 =self. mergeRoutes(sacrificed.copy(), sacInd.get('first'),sacInd.get('last'), expanded, expandInd.get('first'),expandInd.get('last'))
        # merge.append(merge3)
        # sac_rev = [ele for ele in reversed(sacrificed)]
        # sacInd = self.getFirstAndLastNodeID(sac_rev)
        # merge4 =self. mergeRoutes(sac_rev.copy(), sacInd.get('first'), sacInd.get('last'), expanded, expandInd.get('first'),expandInd.get('last'))
        # merge.append(merge4) 


        bestList=[]
        bestVal = 99999
        for mergeList in merge:
            if mergeList.get('totalAccess')<bestVal:
                bestList,bestVal = mergeList.get('mergedRoute'),mergeList.get('totalAccess')
        return bestList
    
    def printPlotSolution(self,coordinate_points, routes, depots):
        totalDist = 0
        tours =[]
        for di,d in enumerate(depots):
            for r in routes[di]:
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
    print("yanlış çalıştırdınnn Test scriptini çalıştırmalısın")