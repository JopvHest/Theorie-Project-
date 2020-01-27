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
from algorithms.BranchAndBoundRandom import branch_and_bound_random
from algorithms.HillClimbing import hill_climbing
from algorithms.HillClimbingAnnealing import hill_climbing_annealing

if __name__ == "__main__":


    
    protein1 = Protein("HHHPHHPH", "2D")
   
    
    protein1 = Protein('HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH', "2D")

    hill_climbing_annealing(protein1, 100000)                                           

    print(protein1.get_score())
    for amino in protein1.chain.chain_list:
        print(amino)
