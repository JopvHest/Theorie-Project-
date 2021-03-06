# Authors: Brent van Dodewaard, Jop van Hest, Luitzen de Vries.
# Heuristics programming project: Protein pow(d)er.

from classes.amino import Amino
from functions.GetMatrix import get_matrix


# This function builds a straight protein which only has folds of 2 (up)
def build_straight_protein(protein):
    mode_3d = protein.mode_3d

    if mode_3d:
        protein.chain.chain_list[0].coordinates = [0, 0, 0]


    else:
        protein.chain.chain_list[0].coordinates = [0, 0]
    
    
    for index, char in enumerate(protein.amino_string):
        if index == 0:
            continue
        
        new_amino = Amino(char, 2, protein.chain.chain_list[index - 1].get_fold_coordinates())


        protein.chain.chain_list.append(new_amino)

    protein.matrix, protein.chain.chain_list = get_matrix(protein.chain.chain_list)

# Rebuilds chain with 1 new fold, returns False if illegal chain
def rebuild_chain(protein, index_to_start_from):

    index = 0
    coordinates_list = []

    while index < index_to_start_from:
        coordinates_list.append(protein.chain.chain_list[index].coordinates)
        index += 1

    while index < len(protein.amino_string):
        old_amino = protein.chain.chain_list[index]
        new_coordinates = protein.chain.chain_list[index - 1].get_fold_coordinates()
        
        if new_coordinates in coordinates_list:
            return False
        
        coordinates_list.append(new_coordinates)
        
        old_amino.coordinates = new_coordinates
        index += 1
    
    return True