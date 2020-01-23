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

    
    # start_time = time.clock()
    
    protein1 = Protein("HHHPHHPH", "2D")
    # protein

    # random_search(protein1)
    # print(protein1.get_score())
    # print("--- %s seconds ---" % (time.clock() - start_time))
    # protein1.print_protein()
    
    protein1 = Protein('CPPCHPPCHPP', "2D")

    breadth_search(protein1, 1)                                           

    print(protein1.get_score())
    for amino in protein1.chain.chain_list:
        print(amino)
    # protein1.print_protein()

    # matrix, offset = get_matrix_efficient(chain)







    # protein1 = Protein("HPPHHHPPHHPH", "2D")
    # depth_search(protein1, 0.5)


    # start_time = time.clock()
