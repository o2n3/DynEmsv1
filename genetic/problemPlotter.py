import matplotlib.pyplot as plt
import numpy as np
from typing import List

def changeListToTour(alist):
    tour=[]
    for nodeInd in range(len(alist)-1):  #range(len(route)):
        tour.append((alist[nodeInd], alist[nodeInd+1]))
    return tour


def changeListToTour2(alist,depotNode):
    tour=[]
    for nodeInd in range(len(alist)):  #range(len(route)):
        tour.append((depotNode, alist[nodeInd]))
    return tour

class routePlotter:
    def __init__(self,positions,v):
        self.positions=positions
        self.V = v

    def visualizeRoute(self,route):
        # x axis values
        x = [1,2,3,4,5,6]
        # corresponding y axis values
        y = [2,4,1,5,2,6]
        
        # plotting the points 
        plt.plot(x, y, color='green', linestyle='dashed', linewidth = 3,
                marker='o', markerfacecolor='blue', markersize=12)
        
        # setting x and y axis range
        plt.ylim(1,8)
        plt.xlim(1,8)
        
        # naming the x axis
        plt.xlabel('x - axis')
        # naming the y axis
        plt.ylabel('y - axis')
        
        # giving a title to my graph
        plt.title('Some cool customizations!')
        
        # function to show the plot
        plt.show()

    def positionProtter(positions):
        for s in positions:
            p = positions[s]
            plt.plot(p[0],p[1],'o')
            plt.text(p[0]+.01,p[1],s,horizontalalignment='left',verticalalignment='center')
            plt.gca().axis('off')


    def plotRoute(self, tours, depots:List=[]):
        colors = [np.random.rand(3) for i in range(len(tours))]
        for t,c in zip(tours,colors):
            for a,b in t:
                p1,p2 = self.positions[a], self.positions[b]
                #if b in depots : c = 'black'
                plt.plot([p1[0],p2[0]],[p1[1],p2[1]], color=c)

        #draw the map again
        for s in range(len(self.positions)):
            p = self.positions[s]
            
            plt.plot(p[0],p[1],'o')
            flag = s            
            if s in depots:flag = '(*'+str(s)+'*)'
            plt.text(p[0]+.01,p[1],flag,horizontalalignment='left',verticalalignment='center')
            
        plt.title('%d '%self.V + 'routes' if self.V > 1 else 'route')
        plt.xlabel('latitude')
        plt.ylabel('longitude')
        # plt.gca().axis('off')
        plt.show()

if __name__ == "__main__":
    a=[0, 27, 29, 15, 22, 9, 0]
    b=changeListToTour(a)
    #    route1 = [[(0,27), (27, 29),(29, 15), (15, 22), (22, 9), (9, 0)]]
    print(b)
    #pl = routePlotter(None,5)
    #pl.visualizeRoute(None)
    