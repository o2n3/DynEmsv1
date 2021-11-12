from FH_RoutingCost import costCompare as cmp

def getDecimalListFromBin(binary_rep):
    decList = [i for i,x in enumerate(binary_rep) if x == 1]
    return decList

def getBinaryListFromDecimal(decimal_rep,bin_len):
    #binList = [(lambda x:1 if decimal_rep.index(x)>=0) for x in range(bin_len) ]
    binList = [1 if x in decimal_rep else 0 for x in range(bin_len)]
    #obj = ["Even" if i%2==0 else "Odd" for i in range(10)]
    return binList    

class Parent:
    def __init__(self,binary_rep, score, objValue=None, objList=None):
        self.binary_rep = binary_rep
        self.dec_rep = getDecimalListFromBin(binary_rep)
        if score is None:
            self.score = 0
        else:
            self.score = score        
        self.objValue = objValue   
        self.objList = objList
    def getBinaryRep(self):
        return self.binary_rep
    def getDecRep(self):
        return self.binary_rep
    def setBinaryRep(self, binary_rep)->None:
        self.binary_rep = binary_rep
        self.dec_rep = getDecimalListFromBin(binary_rep)    
    def setScore(self, score):
        self.score = score
    def getObjValue(self):
        return self.objValue
    def setObjValue(self, objValue):
        self.objValue = objValue

    def __lt__(self, other): # for sorted list
         return cmp(self.score,other.score) #self.score < other.score


if __name__ == "__main__":    
    a = [0,0,0,1,0,0,1,1,1,1,0,1]
    #print(a.index(2))
    exit
    par = Parent(a, 5)
    if 2 in a:
        print('var')
    else:
        print("yok")
    print(a)
    b = getDecimalListFromBin(a)
    print(b)
    c = getBinaryListFromDecimal(b,len(a))
    print(c)