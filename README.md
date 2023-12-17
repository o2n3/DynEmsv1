# Rich Boss
The New Proposed Heuristic “Rich Boss”:
Rich Boss is the new algorithm we proposed in this progress for VRP problem.
Intuition of the algorithm; The VRP Company have a "Rich" boss. And the boss can assign a vehicle for
every clients on depots in the first time. Then things are starting to go bad by one by one and our boss
isn’t "Rich" anymore. In every iteration "Rich" boss loses one vehicle. Sacrificed vehicle's route remove
from network and other (nearest) expand itself. Iteration goes until boss have a real vehicle number. Rich
Boss Time: Beginning of algorithm. In the first iteration, "Rich" boss have vehicles = number of clients in
that time.
Algorithm;
a- Let Number of clients is "C"
b- Let the number of Depot is 1 and label is "D"
c- Total number of nodes is "N" = C + 1 (1 Depot)
d- Let we have "V" vehicle and we want obtain same number of routes for optimum routing
e- Let "r" is a node list for a route, and r(n) is a route list.
f- Let sacrifices matrix "Rsac" contains access times for every active routes when they sacrifice their
selves for each other..
g- Let "Rsac+" matrix is additional access times when routes sacrifices itself. Obtained from rsac
begin
Create a two-dimentional cost matrix CostN(N+1) that contains travel costs between nodes
Set number of Routes routes R = C
Initialize the first routes r(n) for every clients c(n) in Routes matrix. r(n): D -> c(n) -> D
While V < R do: /*while number of Route is more than n.o. vehicle decrease number of route by 1*/
/*calculating Rsac*/
for every index x in R:
sac = x /*ith route is sacrifice itself*/
for every index y in R:
newRouting = addToRoute(r(y),r(sac)) /*join r(sac) to r(y) */

newAccessTime = calculateNewAccess(newRouting,r(sac)) /*objectiveValue =
calculateObjForNewRoutin(newRouting) */
Rsac[y][sac] = newAccessTime, newRouting /*Rsac[y][sac] = objectiveValue*/
end for sacrifice column
end for sacrifice row
y,sac,newRouting = selectSacrificeRoute(Rsac) /*select min access time from Rsac matrix*/
removeFromRoutes(r(sac)) /*sacrifice route removing*/
r(y) = newRouting /*expanding route*/
R = R-1 /*now we have R-1 routes after sacrifice removing*/
End While;
return r for vehicles (R=V)
end RichBoss.

Example:
We have a graph with single depot and three nodes (Figure 3).

CostN Nodes 1 2 3 4 D
1 0 7 15 3 5
2 7 0 12 11 8
3 15 12 0 9 10
4 3 11 9 0 3
D 5 8 10 3 0

Figure 3: Single depot (D1) with three nodes.
In Rich Boss algorithm initial routes r1, r1, r3, r4 are sets as shown in figure 4.

1. 2. 3.

Objective = Access
time

Routes(t
0) r1 D 1 D 5
r2 D 2 D 8
r3 D 3 D 10
r4 D 4 D 3

Figure 4: Rich boss initial routes at t(0)
Rich boss calculates costs (access time) for every pair of routes (r1,r2), (r1,3)... (r2,r1),(r2,r3)... and store
them in the sacrifice matrix (Table 1). Then select the minimum cost in matrix (r1-r4:6 in example) to find
the sacrifice route which will be merge and deleted in the route list for the next iteration.

Merge
from-to 1. 2. 3. 4
New
objective
value
r1-r1 X X X X X
r1-r2 D 2 1 D 15
r1-r3 D 3 1 D 25
r1-r4 D 4 1 D 6
r2-r1 D 1 2 D 12
r2-r2 X X X X X
r2-r3 D 3 2 D 22
r2-r4 D 4 2 D 14
r3-r1 D 1 3 D 20
r3-r2 D 2 3 D 20
r3-r3 X X X X X
r3-r4 D 4 3 D 12
r4-r1 D 1 4 D 8
r4-r2 D 2 4 D 19
r4-r3 D 3 4 D 19
r4-r4 X X X X X
Table 1: Sacrifice matrix.

In the second iteration updated routes shown table 2. Sacrificed r1 was deleted in list because it is merged
with r4* (figure 5). Iterations continue until route number equal to expected vehicle number.

1. 2. 3.

Cost(t1) =
Access
time
r1 DELETED X
Routes(t1) r2 D 2 D 8
r3 D 3 D 10
r4* D 4 1 D 6

Table 2: Route list after iteration

Figure 5: Route 4* after iteration
Multi-depot Rich Boss:
In multi-depot version of the algorithm is similar with single depot. Every depot has “Rich” boss to access
clients. So in the beginning of algorithm clients are accessed with multiple vehicles. Depots have its own
sacrifice matrix like in figures 6.

Figure 6: In multidepot rich boss ever depot has its own sacrifice matrix.
The algorithm select minimum cost route(s) from sacrifice matrixes of depots (Figure 7). If best route is
selected (example in D1) then other depots’ routes associated with these clients are deleted (Figure 8).

Figure 7: The algorithm select minimum cost route(s) from sacrifice matrixes of depots.

Figure 8 : Elimination of associated depots’(D2) routes after selecting best depot (D1)
Difference with Saving and Rich Boss

Saving (classic version) Rich Boss

 Single depot
 Cannot be apply in dynamic environments
 Saving method cannot be changed

 Can be single or multi-depot
 Because of updatable cost matrix can be
used in dynamic environments
 Route based objective can be used.

Location Problem: Detail of Genetic Algorithms with Rich Boss
Rich Boss heuristic is used for our fitness function of genetic algorithms.
Inputs of genetic algorithm:

 All the nodes and their distance matrix (represent casualties and TMCs)
 Depot nodes (represent TMCs)
 Maximum TMCs number, vehicle number of depots.
 Fitness function (Rich Boss)
 Genetic operations implementation with possibility constants.
 Population size, iteration count
After setting input parameters genetic algorithm first initialize the initialize population randomly as
describe in pseudo code. Before going into iterations initial population’s individualset scores and converts
representations to binary. Because of performance issues algorithm hold population with ordered set.
Pseudo code of the genetic algorithm;

Begin
Set the client nodes "C" (Patients), candidate depot nodes "CD" (Field Hospitals) and their coordinates,
Calculate distance matrix "CostN"
Set max depot count MaxD(Max Field Hospital count to set up)
Set objective function (Rich Boss) for genetic algorithm
Set the genetic operator functions (crossover, mutation) with initial rates,
Set population size "P",
Generate initial population IPop
Initialize empty population set called IPop
While size(IPop) < P
produce random Depot Count "rD" between 1 and MaxD (Field Hospital Count) (Ex: rd=3)
produce random number set "rDSet" between 1 and size(CD) with size rD (Ex: rDSet = (2,5,9)
if IPop contains rDSet then continue
Add rDSet to IPop (Ex: IPop = ((1,3),(2,9,5),(1,3,9,8),(4),...) )
Convert IPop population to binary representation ( (1,3) --> (1,0,1,0,0,0)))
Set objective value "score" for every individuals in IPop
Sort IPop with score
Return sorted IPop
Set generation Iteration size "G"
Set steady count "S" -- 4 neden seçildi, default 1 olmalı
Set best solution "Best" with first individual in sorted IPop (because first is the best)
While G>0 Loop
If Best is changed update Best
Select S individual in IPop with Binary Tournement Selection
crossover(Pair)
mutation(child)
repair(child)
add child to "Children"

Calculate fitness (score) for Children
Add Children to sorted IPop
Pop S number of individual from sorted IPop
End Loop
Return Best
End;
Results;
We used values with few nodes and simple distances at the beginning of the development process. Going
step by step we were able to use values close to real simulation. We run algorithm several times with
several parameters while analyzing results.
Our solution representation in GA consists of a binary string that indicates whether the TMCs are at a
location as mentioned earlier. For example [001100] means there is a 6 candidate TMCs. In this solution
only two of them is setting up in index 3 and 4 because their value is 1 in binary. Also there is a maximum
number that the total number of TMCs cannot exceed.

The genetic algorithm uses the Rich Boss VRP algorithm to create the routes that will be used to calculate
the score determined for the ambulances. This score is the fitness value of individuals.

When we analyze the results of algorithm we noticed something important. In minimizing total distance
objective solutions always evolve to 1 TMC solutions like [0100000000, 0000010000]. Minimizing total
distance objective results this undesired solution because as the number of depots increases, so many
overheads occur between warehouse and node as seen in the figure below.

Figure 9: Best solution of total distance objective [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
The alternative objective was the minimizing max route distance of ambulances. It also suits out problem
instance. Our vehicle are ambulances and objectives can be minimizing maximum distance route of other
routes. When we change the objective genetic algorithms best solutions evolve good solutions with several
TMCs like in figure below.
While analyzing results after new objective we decided to add set up cost for TMCs because without the
cost algorithm will always evolve to maximum TMCs number solutions like [111111] to find minimum of
maximum route distance.

Figure 10: Best solution of min-max route distance objective [0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
0, 0, 1, 0, 0]
We continued to research the literature while analyzing the results of our algorithm with different
parameters. There are new and more realistic location models recently. Oksuz and Satoglu [11] proposed
a stochastic location model of TMCs. Their objective is minimizing set up cost and expected casualty
transportation cost with stochastic costs. Their works were applied to Istanbul Kartal district for expected
earthquake disaster. Their general framework are in figure below.

Figure 11: Design of Emergency Medical Center Response System for post disaster [11].
Their assumptions are:
 Casualties are classified like NATA triage standards as immediate T1, delayed T2, minimal T3.
 T1 casualties are only treated by Hospitals, other types are sent Hospitals or TMCs
 There are safety areas after disaster and triage of casualties are on this area by health personnel.
We decided to use this model for our problem. We will detail how to use the model in our next progress.
