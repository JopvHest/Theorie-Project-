
from timeit import default_timer as timer

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

from functions.UIDicts import protein_dict, algo_dict, dimension_dict, vis_dict, function_parameters


# Get which arguments are required for a function.
def get_arguments(input_string):
    return function_parameters[input_string]

# Execute the correct search algo.
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
    
    if protein_string == "branch_and_bound_random":
        branch_and_bound_random(protein, *parameter_list)
    
    if protein_string == "random_search":
        random_search(protein)

    if protein_string == "beam_search":
        beam_search(protein, *parameter_list)

# Execute the correct visualisation type.
def execute_visualisation(vis_type, protein):
    if vis_type == "Standard output list":
        protein.get_output_list()
    if vis_type == "Interactive protein visualisation":
        protein.print_protein()
    if vis_type == "Final score":
        print("Final score: " + str(protein.get_score()))

# Print all the user choices to the user from a dict
def print_question_dict(dict):
    for key, value in dict.items():
        print(key + ": " + value)

# This function contains the user interface for the hp protein folding app
def start_user_interface():

    # Get the dimension mode from the user
    dimension_mode = False
    while not dimension_mode:
        print()
        print("Please enter the number of the desired dimension mode")
        
        # Prints all possible options.
        print_question_dict(dimension_dict)
        string_input = input()
        print()

        if string_input in dimension_dict:
            dimension_mode = dimension_dict[string_input]

    # Get the protein_string from the user.
    protein_string = False
    while not protein_string:
        print("Please enter the number of your desired protein string.")
        print_question_dict(protein_dict)
        string_input = input()
        print()

        if string_input in protein_dict:

            # User wants a custom, non preset, string.
            if protein_dict[string_input] == "Custom":
                print("Please enter your custom protein string. (Using 'P', 'H', 'C')")
                protein_string = input()
            else:
                protein_string = protein_dict[string_input]
    
    # Try to create the protein.
    protein = Protein(protein_string, dimension_mode)

    # Get the desired algo from the user.
    protein_string = False
    while not protein_string:
        print("Please enter the number of your desired search algorithm.")
        print_question_dict(algo_dict)
        string_input = input()
        print()
        if string_input in algo_dict:
            protein_string = algo_dict[string_input]

    # Get the arguments that are needed for this particular search.
    arguments_to_ask = get_arguments(protein_string)

    # Question the user one by one for all the paramters and add them to the list.
    parameter_list = []
    for argument in arguments_to_ask:
        print("Please specify the value for the parameter: " + argument)
        parameter_list.append(float(input()))
        print()
    
    start = timer()
    # Execute the actual search algo.
    execute_search(protein_string, parameter_list, protein)
    end = timer()
    
    print()
    print("Final score: " + str(protein.get_score()))
    print("Time elapsed: " + str(end - start) + " sec")
    print()

    # Loops untill user choses "Exit".
    leave = False
    while not leave:
        print("Please enter the number of your desired visualization")
        print_question_dict(vis_dict)
        visualization = input()
        print()

        if visualization in vis_dict:
            if vis_dict[visualization] == "Exit":
                leave = True

            # Execute the correct visualisation.
            else:
                execute_visualisation(vis_dict[visualization], protein)