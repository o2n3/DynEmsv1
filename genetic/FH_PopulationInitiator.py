import itertools
from datetime import datetime
import numpy as np
from FH_Individual import Parent
from FH_Population import Population



class PopulationGenerator:
    
    def __init__ (self, candidate_locations_size, FH_count, FH_generation_population_size):
        self.candidate_locations_size = candidate_locations_size
        self.FH_count = FH_count
        self.FH_generation_population_size = FH_generation_population_size

    def getInitPop(self):
        np.random.seed()
        data = set()
        i=0
        while len(data) < self.FH_generation_population_size:   
            i += 1
            self.random_candidate_set= set(np.random.randint(1, self.candidate_locations_size+1, self.FH_count))
            #print(self.random_candidate_set)
            if len(self.random_candidate_set) == self.FH_count:
                #print('add to set',candidate_set)
                data.add(frozenset(self.random_candidate_set))            
            if i > self.FH_generation_population_size * 10:
                print('oopppps infinite while loop!!')
                break
            #print(data)
        #ek kontrol
        if len(data) != self.FH_generation_population_size:
            print ("smthg Wrong!")
            raise ValueError
            
        # frozen set to list and sosted also   
        self.FH_population = [set(sorted(item)) for item in data]
        # change it to bit representation, 1 for chosen
        #candidate_location_bits = np.full((self.FH_generation_population_size, self.candidate_locations_size), 0, dtype=int)
        #candidate_location_bits2 = [[0]*self.candidate_locations_size]*self.FH_generation_population_size 
        candidate_location_bits2 = []        
        for _ in range(self.FH_generation_population_size):
            c = []
            for _ in range(self.candidate_locations_size):
                c.append(0)
            candidate_location_bits2.append(c)
    

        positions = [(i,x-1)  for i,pos in enumerate(self.FH_population) for x in pos]  

        #rows,cols = zip(*positions)
        #candidate_location_bits[rows,cols]=1

        for i in positions:            
            candidate_location_bits2[i[0]][i[1]] = 1            
        
        return candidate_location_bits2

    def getInitPop2(self, objective):
        np.random.seed()
        data = set()
        i=0
        while len(data) < self.FH_generation_population_size:   
            i += 1
            FH_count = np.random.randint(1,self.FH_count+1)
            self.random_candidate_set= set(np.random.randint(1, self.candidate_locations_size+1, FH_count))
            #print(self.random_candidate_set)
            #if len(self.random_candidate_set) == self.FH_count: # closed because max count is FH_count. 
                #print('add to set',candidate_set)
            data.add(frozenset(self.random_candidate_set))            
            if i > self.FH_generation_population_size * 10:
                print('oopppps infinite while loop!!')
                break
            #print(data)
        #ek kontrol
        if len(data) != self.FH_generation_population_size:
            print ("smthg Wrong!")
            raise ValueError

        # frozen set to list and sosted also   
        self.FH_population = [set(sorted(item)) for item in data]
        # change it to bit representation, 1 for chosen
        candidate_location_bits2 = []        
        for _ in range(self.FH_generation_population_size):
            c = []
            for _ in range(self.candidate_locations_size):
                c.append(0)
            candidate_location_bits2.append(c)

        positions = [(i,x-1)  for i,pos in enumerate(self.FH_population) for x in pos]  
        for i in positions:                        
            candidate_location_bits2[i[0]][i[1]] = 1                    
        #candidate_location_parents = [Parent(b,objective.value(b)) for b in candidate_location_bits2]
        candidate_location_parents = [Parent(b,0) for b in candidate_location_bits2]
        for c in candidate_location_parents:            
            c.score, c.objValue, c.objList = objective.value(c.dec_rep)
        return Population(candidate_location_parents)

    def getInitPop3(self, allDepotList, objective):
        np.random.seed()
        data = set()
        i=0
        while len(data) < self.FH_generation_population_size:   
            i += 1
            FH_count = np.random.randint(1,self.FH_count+1)
            self.random_candidate_set= set(np.random.randint(1, self.candidate_locations_size+1, FH_count))
            #print(self.random_candidate_set)
            #if len(self.random_candidate_set) == self.FH_count: # closed because max count is FH_count. 
                #print('add to set',candidate_set)
            data.add(frozenset(self.random_candidate_set))            
            if i > self.FH_generation_population_size * 10:
                print('oopppps infinite while loop!!')
                break
            #print(data)
        #ek kontrol
        if len(data) != self.FH_generation_population_size:
            print ("smthg Wrong!")
            raise ValueError

        # frozen set to list and sosted also   
        self.FH_population = [set(sorted(item)) for item in data]
        # change it to bit representation, 1 for chosen
        candidate_location_bits2 = []        
        for _ in range(self.FH_generation_population_size):
            c = []
            for _ in range(self.candidate_locations_size):
                c.append(0)
            candidate_location_bits2.append(c)

        positions = [(i,x-1)  for i,pos in enumerate(self.FH_population) for x in pos]  
        for i in positions:                        
            candidate_location_bits2[i[0]][i[1]] = 1                    
        #candidate_location_parents = [Parent(b,objective.value(b)) for b in candidate_location_bits2]
        candidate_location_parents = [Parent(b,0) for b in candidate_location_bits2]
        for c in candidate_location_parents:            
            c.score, c.objValue = objective.value(c.dec_rep)
        return Population(candidate_location_parents)

#test
if __name__ == "__main__":        
    pop = PopulationGenerator(10, 2, 20).getInitPop2()    
    for o in pop.parentList:
        print(o.binary_rep)