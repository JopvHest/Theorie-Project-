from classes.protein import Protein

from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search
from algorithms.DepthSearchLookahead import depth_search_lookahead
from algorithms.BreadthSearch import breadth_search
from algorithms.BeamSearch import beam_search
from algorithms.DepthSearchIterative import depth_search_iterative
from algorithms.BranchAndBound import branch_and_bound
from algorithms.HillClimbingCaterpillar import hill_climbing_caterpillar
from algorithms.HillClimbing import hill_climbing
from algorithms.BranchAndBoundRandom import branch_and_bound_random
from algorithms.SimulatedAnnealing import simulated_annealing


if __name__ == "__main__":

    # Create a new protein.
    protein1 = Protein('HPHHPP', "2D")
    
    # Create the protein's chain and matrix by using the depth search algo.
    beam_search(protein1, 10, 5)

    # Print the score.
    print("Final score: " + str(protein1.get_score()))


    # Visualize the protein using MatPlotLib
    protein1.print_protein()

    protein1.get_output_list()