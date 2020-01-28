from classes.protein import Protein
from algorithms.DepthSearchLookahead import depth_search_lookahead
from functions.InterfaceFunctions import get_arguments, execute_visualisation, execute_search, print_question_dict
from algorithms.BranchAndBoundRandom import branch_and_bound_random
from timeit import default_timer as timer

if __name__ == "__main__":
    
    # Contains the options the user has.
    dimension_dict = {
        "1": "2D",
        "2": "3D"
    }

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
    
    # Contains the options the user has.
    protein_dict = {
        "1": "HHPHHHPHPHHHPH",
        "2": "HPHPPHHPHPPHPHHPPHPH",
        "3": "PPPHHPPHHPPPPPHHHHHHHPPHHPPPPHHPPHPP",
        "4": "HHPHPHPHPHHHHPHPPPHPPPHPPPPHPPPHPPPHPHHHHPHPHPHPHH",
        "5": "PPCHHPPCHPPPPCHHHHCHHPPHHPPPPHHPPHPP",
        "6": "CPPCHPPCHPPCPPHHHHHHCCPCHPPCPCHPPHPC",
        "7": "HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH",
        "8": "HCPHPHPHCHHHHPCCPPHPPPHPPPPCPPPHPPPHPHHHHCHPHPHPHH",
        "9": "Custom"
        }
    
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

    # Contains the algos the user can chose from.
    algo_dict = {
        "1": "random_search",
        "2": "depth_search",
        "3": "depth_search_lookahead",
        "4": "breadth_search",
        "5": "beam_search",
        "6": "branch_and_bound",
        "7": "branch_and_bound_random",
        "8": "hill_climbing",
        "9": "hill_climbing_caterpillar",
        "10": "simulated_annealing"
        }

    protein_string = False
    while not protein_string:
        print("Please enter the number of your desired search algorithm.")
        print_question_dict(algo_dict)
        string_input = input()
        print()
        if string_input in algo_dict:
            protein_string = algo_dict[string_input]

    # Get the arguments that are needed for this particular search
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

    # Algo containing the to chose from visualisations
    vis_dict = {
        "1": "Interactive protein visualisation",
        "2": "Standard output list",
        "3": "Final score",
        "4": "Exit"}

    # Loops untill user choses "Exit"
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