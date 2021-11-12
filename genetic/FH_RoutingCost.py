import itertools

def costCompare(value1, value2)->bool:
    if value1 < value2:
        return True
    else:
        return False

class BinaryValueObjective:
    def __init__ (self):
        None
    def value(self, binary_list):
        binary_str = ''.join([str (item) for item in binary_list])
        return int(binary_str,2) #return decimal from binary


# 1 olan değerlerin indexleri arasındaki farkları toplar
class IndexDifferenceObjective:
    def __init__ (self):
        None
    def value(self, binary_list):        
        c1_index_list = [b1 for b1,b2  in enumerate(binary_list) if b2 == 1]                 
        return sum([e-i for i,e in itertools.combinations(c1_index_list,2)])        

#test
if __name__ == "__main__":    
    #o = BinaryValueObjective()
    o = IndexDifferenceObjective()
    a = [1,0,0,0,1,0,0,0,1,1]
    b = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    print(o.value(b))


"""
class RichBo:
    def __init__(self):
        None
"""    