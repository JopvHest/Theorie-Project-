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
    }

    return function_parameters[input_string]

def execute_search(algo_string, parameter_list, protein):
    if protein_string == "depth_search":
        depth_search(protein, *parameter_list)

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


if __name__ == "__main__":

    dimension_dict = {
        "1": "2D",
        "2": "3D"
    }

    dimension_mode = False
    while not dimension_mode:
        print("Please enter the number of the desired dimension mode")
        print_question_dict(dimension_dict)
        string_input = input()
        if string_input in dimension_dict:
            dimension_mode = dimension_dict[string_input]
    
    protein_dict = {
        "1": "HHPHPHH",
        "2": "Custom",
        }
    protein_string = False
    while not protein_string:
        print("Please enter the number of your desired protein string.")
        print_question_dict(protein_dict)
        string_input = input()

        if string_input in protein_dict:
            if protein_dict[string_input] == "Custom":
                print("Please enter your custom protein string. (Using 'P', 'H', 'C')")
                protein_string = input()
            else:
                protein_string = protein_dict[string_input]
    
    protein = Protein(protein_string, dimension_mode)
    
    algo_dict = {
        "1": "depth_search",
        
        }

    protein_string = False
    while not protein_string:
        print("Please enter the number of your desired search algorithm.")
        print_question_dict(algo_dict)
        string_input = input()
        if string_input in algo_dict:
            protein_string = algo_dict[string_input]
        
    arguments_to_ask = get_arguments(protein_string)

    parameter_list = []
    for argument in arguments_to_ask:
        print("Please specify the value for the parameter: " + argument)
        parameter_list.append(input())
    
    execute_search(protein_string, parameter_list, protein)
    print("Final score: " + str(protein.get_score()))
    vis_dict = {
        "1": "Interactive protein visualisation",
        "2": "Standard output list",
        "3": "Final score"}

    leave = False
    while not leave:
        print("Please enter the number of you desired visualization")
        print_question_dict(vis_dict)
        visualization = input()

        if visualization in vis_dict:
            if vis_dict[visualization] == "Exit":
                leave = True
            else:
                execute_visualisation(vis_dict[visualization], protein)