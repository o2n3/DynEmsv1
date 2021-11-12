from typing import List
from FH_Individual import Parent,getDecimalListFromBin
from numpy.random import randint
from numpy.random import rand
from FH_Individual import getDecimalListFromBin as getDec

class stdCrossover:
    def __init__(self, r_cross):
        self.r_cross = r_cross

    def crossover(self,p1, p2):
        # children are copies of parents by default
        c1, c2 = p1.copy(), p2.copy()
        #print('before',c1,c2)
        # check for recombination
        if rand() < self.r_cross:
            # select crossover point that is not on the end of the string
            pt = randint(1, len(p1)-2)
            #print(pt)
            # perform crossover
            c1 = p1[:pt] + p2[pt:]
            c2 = p2[:pt] + p1[pt:]
            #print ('cross at:',pt)
        #print('after',c1,c2)
        #validate genes     
        return [c1, c2]

class stdMutation:
    def __init__(self, r_mut):
        self.r_mut = r_mut
    # mutation operator
    def mutation(self, bitstring:List):
        #print(bitstring)        
        for i in range(len(bitstring)):
            # check for a mutation
            #print(rand())
            if rand() < self.r_mut:
                # flip the bit
                bitstring[i] = 1 - bitstring[i]
                #print('1',bitstring)
        #print('2',bitstring)

class stdRepairParent:
    def __init__(self,max_size:int):
        self.max_size = max_size
    def repair(self, parent:Parent):
        if len(parent.dec_rep)==0:
            None
        else:                              
            while self.max_size < len(parent.dec_rep):
                toZero = parent.dec_rep[randint(len(parent.dec_rep))]
                b = parent.getBinaryRep()
                b[toZero] = 0            
                parent.setBinaryRep(b)

class stdRepairChromosome:
    def __init__(self,max_size:int):
        self.max_size = max_size
    def repair(self, binary_rep:List):   
        dec_rep = getDecimalListFromBin(binary_rep)                   
        if len(dec_rep)==0:
            None
        else:
            while self.max_size < len(dec_rep):
                toZero = dec_rep[randint(len(dec_rep))]
                binary_rep[toZero] = 0
                dec_rep.remove(toZero)

        #print('2',bitstring)

if __name__ == '__main__':

    r = stdRepairChromosome(4)
    #a = [1,1,0,0,1,0,1,0,1,1]
    a = [0,0,0,0,0,0,0,0,0,0]
    print(a)
    r.repair(a)
    print(a)

    """
    c = stdCrossover(1)
    m = stdMutation(0.5)
    a = [1,1,1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0]
    b = [0,0,0,1,0,1,0,0,0,0,1,1,1,0,0,0,1,1,0,0]    
    m.mutation(a)    
    x,y = c.crossover(a,b)
    print('3',x,y)
    """
    #print(randint(3))
    """
    r = stdRepairParent(4)
    a = [1,1,0,0,1,0,1,0,1,1]
    print(a)
    p=Parent(a,0)
    r.repair(p)
    print(p.binary_rep)
    """

