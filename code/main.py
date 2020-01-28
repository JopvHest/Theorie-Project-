from classes.protein import Protein

from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search
from algorithms.DepthSearchLookahead import depth_search_lookahead
from algorithms.BreadthSearch import breadth_search
from algorithms.BeamSearch import beam_search
from algorithms.DepthSearchIterative import depth_search_iterative
from algorithms.BrandAndBound import branch_and_bound
from algorithms.HillClimbingCaterpillar import hill_climbing_2
from algorithms.BranchAndBoundRandom import branch_and_bound_random
from algorithms.SimulatedAnnealing import simulated_annealing


if __name__ == "__main__":

    # Create a new protein.
    protein1 = Protein('HPPHPHPHPH', "2D")
    
    # Create the protein's chain and matrix by using the depth search algo.
    depth_search(protein1, 1)

    # Print the score.
    print("Final score: " + protein1.get_score())

    # Visualize the protein using MatPlotLib
    protein1.print_protein()

