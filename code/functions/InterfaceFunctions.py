
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

def get_arguments(input_string):
    function_parameters = {
        "beam_search" : ["c-h score", "selection_levels"],
        "depth_search" : ["c-h score"],
        "breadth_search" : ["c-h score"],
        "depth_search_lookahead" : ["c-h score", "max_lookahead"],
        "hill_climbing" : ["iterations", "max non improve turns"],
        "hill_climbing_caterpillar" : ["iterations", "max non improve turns"],
        "simulated_annealing" : ["iterations", "start temp", "end temp"],
        "branch_and_bound" : ["c-h score", "best score import"],
        "branch_and_bound_random" : ["c-h score", "best score import", "p1", "p2"],
        "random_search" : []
    }

    return function_parameters[input_string]

def execute_search(protein_string, parameter_list, protein):
    if protein_string == "depth_search":
        depth_search(protein, *parameter_list)
    
    if protein_string == "depth_search_lookahead":
        print(*parameter_list)
        depth_search_lookahead(protein, *parameter_list)
    
    if protein_string == "breadth_search":
        breadth_search(protein, *parameter_list)
    
    if protein_string == "hill_climbing":
        hill_climbing(protein, *parameter_list)

    if protein_string == "hill_climbing_caterpillar":
        hill_climbing_caterpillar(protein, *parameter_list)
    
    if protein_string == "simulated_annealing":
        simulated_annealing(protein, *parameter_list)
    
    if protein_string == "branch_and_bound":
        branch_and_bound(protein, *parameter_list)
    
    if protein_string == "brand_and_bound_random":
        branch_and_bound_random(protein, *parameter_list)
    
    if protein_string == "random_search":
        random_search(protein)

def execute_visualisation(vis_type, protein):
    if vis_type == "Standard output list":
        protein.get_output_list()
    if vis_type == "Interactive protein visualisation":
        protein.print_protein()
    if vis_type == "Final score":
        print("Final score: " + str(protein.get_score()))

def print_question_dict(dict):
    for key, value in dict.items():
        print(key + ": " + value)