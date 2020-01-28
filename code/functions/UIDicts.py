# This file contains all the dictionairies used by the user interface

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
# Contains the options the user has.
dimension_dict = {
    "1": "2D",
    "2": "3D"
}

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
    
# Contains the parameters required for each function
function_parameters = {
    "beam_search" : ["c-h score"],
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

# Algo containing the to chose from visualisations.
vis_dict = {
    "1": "Interactive protein visualisation",
    "2": "Standard output list",
    "3": "Final score",
    "4": "Exit"}