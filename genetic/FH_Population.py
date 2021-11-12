from FH_Individual import Parent
from sortedcontainers import SortedList

class Population:
    def __init__(self,parentList):
        self.parentList = SortedList()
        for p in parentList:
            self.parentList.add(p)
    def setScores(self, scores):
        for i,s in enumerate(scores): self.parentList[i].setScore(s)
        
    def calculateAndSetScores(self,pop,objective):
        self.setScores([objective.value(p.binary_list) for p in pop])
        
if __name__ == '__main__':
    a = [0,0,0,1,0,0,1,1,1,1,0,1]
    par1 = Parent(a, 5)
    a = [0,0,2,1,0,0,0,0,0,1,0,1]
    par2 = Parent(a, 4)
    a = [1,1,2,1,0,0,0,0,0,1,0,1]
    par3 = Parent(a, 6)
    parentList = [par1,par2,par3]
    pop = Population(parentList)
    print("önce")
    for p in pop.parentList:
        print(p.score)  
    print("sonra")
    pop.parentList.remove(par2)
    for p in pop.parentList:
        print(p.score) 
