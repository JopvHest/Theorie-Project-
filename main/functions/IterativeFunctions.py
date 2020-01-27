
# This function builds a straight protein which only has folds of 2 (up)
def build_straight_protein(protein):
    mode_3d = protein.mode_3d

    if mode_3d:
        protein.chain.chain_list[0].coordinates = [0, 0, 0]
    else:
        protein.chain.chain_list[0].coordinates = [0, 0]
    
    # Build a chain with all folds at 2
    for index, char in enumerate(protein.amino_string):
        
        # The first amino is already there
        if index == 0:
            continue
        
        new_amino = Amino(char, 2, protein.chain.chain_list[index - 1].get_fold_coordinates())
        protein.chain.chain_list.append(new_amino)

    protein.matrix, protein.chain.chain_list = get_matrix(protein.chain.chain_list)


# Rebuilds chain with 1 new fold, returns False if illegal chain
def rebuild_chain(protein, index_to_start_from):

    index = 0
    coordinates_list = []

    # Get all coordinates before the amino with the new fold
    while index < index_to_start_from:
        coordinates_list.append(protein.chain.chain_list[index].coordinates)
        index += 1

    # Give all aminos after the amino with the new fold new coordinates.
    # If one of these coordinates already exist, chain is illegal.
    while index < len(protein.amino_string):
        old_amino = protein.chain.chain_list[index]
        new_coordinates = protein.chain.chain_list[index - 1].get_fold_coordinates()
        
        if new_coordinates in coordinates_list:
            return False
        
        old_amino.coordinates = new_coordinates
        index += 1
    
    return True
