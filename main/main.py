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
from algorithms.IterativeAlgorithm2 import hill_climbing_2
from algorithms.IterativeAlgorithm import iterative_algorithm
from algorithms.BranchAndBoundLookahead import branch_and_bound_lookahead
from algorithms.BranchAndBoundRandom import branch_and_bound_random
# from algorithms.HillClimbing import hill_climbing
# cfrom algorithms.HillClimbingAnnealing import hill_climbing_annealing


from functions.GetMatrix import get_matrix_efficient
from functions.GetScore import get_score_efficient


if __name__ == "__main__":


    # # depth_search_lookahead(protein, max_lookahead, ch_score):
    
       
    # start_time = time.clock()
    # scores = []
    
    # # branch_and_bound_random(protein1, 1, 0, 0.8, 0.5) 
    # ch = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
    # for i in ch:
    protein1 = Protein('HPPHPHPHPH', "2D")
    #     depth_search_lookahead(protein1, 11 , i)

    hill_climbing_2(protein1, 4, 50)  
        # branch_and_bound_random(protein1, 1, 0, 0.5, 0.1)
        # print("ch_score: ", end="")
        # print(i)
        # score = protein1.get_score()
        # print(score)
        # scores.append(score)
    # protein1.print_protein()
    # print(scores)
    
    # print("--- %s seconds ---" % (time.clock() - start_time))
    # # protein1.print_protein()
    
