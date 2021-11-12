"""
Begin	
	Set the client nodes "C" (Patients), candidate depot nodes "CD" (Field Hospitals) and their coordinates,
	Calculate distance matrix "CostN"
	Set max depot count MaxD(Max Field Hospital cout to set up)
	Set the objective function (RichBoss)
		Get depot and client coordinates with distance matrix
		Set vehicle number in depots (ambulance number)
		Set objective function 

	Set objective function (Rich Boss) for genetic algorithm
	Set the genetic operator functions (crodssover, motation) with initial rates,	
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
		"Select" S individual in IPop with Tournement Selection (??? sorted pop with tournament selection is fair?) Binary tournement selection kullanılacak
			Initialize 
			Get random individual from Pop [1,2,*3*,4,*5*,6,-7-,-8-,9...50]
			Get 1..(10)k-1 random number sized Indivudual Set from Pop 
			Select the Individual with best Scores
		
		For every "Pair" in Select(4 birey) Loop
			"ChildPair" = crossover(Pair)
			For "child" in ChildPair Loop
				mutation(child)
				repair(child)
				add child to "Children"
			End Loop
		End Loop
		Calculate fitness (score) for Children
		Add Children to sorted IPop
		Pop S number of individual from sorted Ipop
	End Loop
	Return Best
End;
"""
from numpy.random import randint
from FH_Individual import Parent
from FH_RoutingCost import costCompare as cmp
from FH_Individual import getDecimalListFromBin as getDec
import bisect

class FH_geneticOperator:
    def __init__(self, n_iter, objective, pop):
        self.n_iter = n_iter
        self.objective = objective
        self.pop = pop
        self.pop_size = len(pop.parentList)
        self.best = 0
        #print(pop[0])
        self.best_eval, self.best_objValue, self.bestObjList = self.objective.value(pop.parentList[0].dec_rep)
        self.best, self.best_dec_rep = pop.parentList[0].binary_rep, pop.parentList[0].dec_rep
        for p in pop.parentList:
            print(">%d, initial f(%s)(%s)(%s) = %f" % (0,  p.binary_rep,p.dec_rep,p.objList, p.score))  
        
 
    # tournament selection for parent (k=2 binary selection)
    def selection(self, parentList, k=2):
        # first random selection
        selection_ix = randint(self.pop_size)
        for ix in randint(0, self.pop_size, k-1):
            # check if better (e.g. perform a tournament)
            if cmp(parentList[ix].score,parentList[selection_ix].score): #parentList[ix].score > parentList[selection_ix].score:
                selection_ix = ix
        return selection_ix 

    def runAlgorithm(self, stdc_op, stdm_op, stdr_op, steady_parent_count):
        
        # evaluate all candidates in the population
        #scores2 = [self.objective.value(p.dec_rep) for p in self.pop.parentList]
        # enumerate generations
        for gen in range(self.n_iter):                
            # check for new best solution
            if cmp(self.pop.parentList[0].score , self.best_eval): #self.pop.parentList[self.pop_size-1].score > self.best_eval:
                self.best, self.best_eval, self.best_objValue, self.best_dec_rep = self.pop.parentList[0].binary_rep, self.pop.parentList[0].score, self.pop.parentList[0].objValue, self.pop.parentList[0].dec_rep                                
                self.bestObjList = self.pop.parentList[0].objList
                print(">%d, new best f(%s)(%s)(%s) = %f" % (gen,  self.pop.parentList[0].binary_rep,self.pop.parentList[0].dec_rep, self.bestObjList, self.pop.parentList[0].score))  

            # select parents (Steady state de 2 tane seçilecek)
            selected = [self.selection(self.pop.parentList) for _ in range(steady_parent_count)]
            # create the next generation (SSde sadece iki child oluşacak, list değil) 
            children = list()
            parent_indx = []
            for i in range(0, steady_parent_count, 2): #for i in range(0, self.pop_size, 2):
                for c in stdc_op.crossover(self.pop.parentList[selected[i]].binary_rep,self.pop.parentList[selected[i+1]].binary_rep):                
                    stdm_op.mutation(c)
                    #repair  repair  repair repair repair 
                    stdr_op.repair(c)
                    children.append(c)

            #steadyList = [Parent(c,self.objective.value(c)) for c in children]
            steadyList = [Parent(c,0) for c in children]
            for ste in steadyList:
                ste.score,ste.objValue, ste.objList  = self.objective.value(ste.dec_rep)
                self.pop.parentList.add(ste)
            # pop the worst
            for _ in range(steady_parent_count):
                self.pop.parentList.pop()
            print("gen:",gen)

        return self.best, self.best_eval, self.best_objValue, self.best_dec_rep,self.bestObjList






