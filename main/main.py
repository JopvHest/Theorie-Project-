import sys, time

from classes.protein import Protein
from classes.amino import Amino
from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search
from algorithms.DepthSearchLookahead import depth_search_lookahead
from algorithms.BreadthSearch import breadth_search
from algorithms.BeamSearch import beam_search
from algorithms.DepthSearchIterative import depth_search_iterative
from algorithms.DepthSearchFoldSpots import depth_search_iterative_and_spots
from algorithms.IterativeAlgorithm import iterative_algorithm
from algorithms.BranchAndBoundLookahead import branch_and_bound_lookahead
from algorithms.BranchAndBoundRandom import branch_and_bound_random
from algorithms.HillClimbing import hill_climbing
from algorithms.HillClimbingAnnealing import hill_climbing_annealing


from functions.GetMatrix import get_matrix_efficient
from functions.GetScore import get_score_efficient


if __name__ == "__main__":

    
       
    start_time = time.clock()
    protein1 = Protein('HPHPPHHPHPPHPHHPPHPH', "3D")
    # depth_search_lookahead(protein1, 8, 1) 
    # branch_and_bound_random(protein1, 1, 0, 0.8, 0.5) 
    
    hill_climbing(protein1, 50000)  
    # branch_and_bound_random(protein1, 1, 0, 0.5, 0.1)
    print(protein1.get_score())
    
    print("--- %s seconds ---" % (time.clock() - start_time))
    # protein1.print_protein()
    