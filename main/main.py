import sys, time

from classes.protein import Protein
from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search
from algorithms.DepthSearchLookahead import depth_search_lookahead
from algorithms.BreadthSearch import breadth_search


if __name__ == "__main__":

    # protein1 = Protein("HhhpHhpH", "2D")
    protein1 = Protein("HppH", "3D")
    depth_search(protein1, 1)
    protein1.print_protein()
    # start_time = time.clock()


    # protein1 = Protein("HPPHHHPPHHPH", "2D")
    # depth_search(protein1, 0.5)
    # print("--- %s seconds ---" % (time.clock() - start_time))

    # start_time = time.clock()
