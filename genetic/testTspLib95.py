from numpy import append
from readvrplib import read_vrplib_file
import cvrp_io
from RichBoss import RichBoss
from problemPlotter import routePlotter, changeListToTour
import tsplib95

if __name__ == '__main__':
    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n101-k10.vrp"
    #file_name = r"C:\Users\mete nini\Desktop\mete\tez\python\DynEms\data\M-n121-k7.vrp"
    file_name = r"C:/Users/mete nini/Desktop/mete/tez/python/DynEms/data/p01"
    problem = tsplib95.load(file_name)
    list(problem.get_nodes())
    print(problem)
