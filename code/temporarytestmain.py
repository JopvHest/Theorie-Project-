from classes.protein import Protein

from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search
from algorithms.DepthSearchLookahead import depth_search_lookahead
from algorithms.BreadthSearch import breadth_search

from algorithms.BeamSearch import beam_search
# from algorithms.BeamSearch2 import beam_search

from algorithms.DepthSearchIterative import depth_search_iterative
from algorithms.BranchAndBound import branch_and_bound
from algorithms.HillClimbingCaterpillar import hill_climbing_caterpillar
from algorithms.HillClimbing import hill_climbing
from algorithms.BranchAndBoundRandom import branch_and_bound_random
from algorithms.SimulatedAnnealing import simulated_annealing
 
 
if __name__ == "__main__":

 # Create a new protein.
    protein1 = Protein('HPHHPPHHPHPHPHPPHPH', "2D")
    
    # Create the protein's chain and matrix by using the depth search algo.
    beam_search(protein1, 1, [3, 5, 7, 9, 11, 13, 15, 17, 19])


    # Visualize the protein using MatPlotLib
    protein1.print_protein()

    protein1.get_output_list()