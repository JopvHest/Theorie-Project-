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
from algorithms.IterativeAlgorithm2 import hill_climbing
from algorithms.IterativeAlgorithm import iterative_algorithm
from algorithms.BranchAndBoundLookahead import branch_and_bound_lookahead
from algorithms.BranchAndBoundRandom import branch_and_bound_random
# from algorithms.HillClimbing import hill_climbing
# cfrom algorithms.HillClimbingAnnealing import hill_climbing_annealing


from functions.GetMatrix import get_matrix_efficient
from functions.GetScore import get_score_efficient


if __name__ == "__main__":

    # chain = [Amino("0", 1, [0, 0]), Amino("1", 1, [1, 0]), Amino("2", 1, [2, 0]), Amino("3", 1, [3, 0]), Amino('4', 1, [4, 0]), Amino("5", 1, [5, 0]), Amino("6", 1, [6, 0]), Amino("7", 2, [6, 1])]
    # start_time = time.clock()
    
    protein1 = Protein("HHHPHHPH", "2D")
    # protein1.chain.chain_list = chain
    # for amino in protein1.chain.chain_list:
    #     print(amino)
    # protein

    # random_search(protein1)
    # print(protein1.get_score())
    # print("--- %s seconds ---" % (time.clock() - start_time))
    # protein1.print_protein()
    


    # pato, chain2 = iterative_algorithm(protein1.chain, 1)
    # protein1.chain.chain_list = pato

    hill_climbing(protein1, 100, 50)
    
    # protein1 = Protein('HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH', "2D")

    # hill_climbing_annealing(protein1, 100000)                                           

    # print(protein1.get_score())
    # for amino in protein1.chain.chain_list:
    #     print(amino)
    
    
    
    # protein1.print_protein()
    
    
    
    # # protein1.print_protein()
    # protein1.chain.chain_list = chain2

    # for amino in protein1.chain.chain_list:
        # print(amino)

    # matrix, offset = get_matrix_efficient(chain)







    # protein1 = Protein("HPPHHHPPHHPH", "2D")
    # depth_search(protein1, 0.5)


    # start_time = time.clock()
