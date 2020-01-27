from classes.amino import Amino
from functions.IsChain3d import is_chain_3d



# This function calculates and returns the score of the chain.
def get_score(chain, matrix):

        # Check if 3d mode.
        mode_3d = is_chain_3d(chain)

        total_score = 0

        # Iterate over all aminos and add the score of all of them.
        for index, amino in enumerate(chain):

            # P has no effect on stability
            if amino.atype == "P":
                continue

            # Creates a list with all coordinates that need to be checked.
            xy_tocheck = []

            # 3D
            if mode_3d:
                amino_x, amino_y, amino_z = amino.coordinates
                xy_tocheck.append([amino_x + 1, amino_y, amino_z])
                xy_tocheck.append([amino_x, amino_y + 1, amino_z])
                xy_tocheck.append([amino_x - 1, amino_y, amino_z])
                xy_tocheck.append([amino_x, amino_y - 1, amino_z])
                xy_tocheck.append([amino_x, amino_y, amino_z - 1])
                xy_tocheck.append([amino_x, amino_y, amino_z + 1])

            # 2D
            else:
                amino_x, amino_y = amino.coordinates
                xy_tocheck.append([amino_x + 1, amino_y])
                xy_tocheck.append([amino_x, amino_y + 1])
                xy_tocheck.append([amino_x - 1, amino_y])
                xy_tocheck.append([amino_x, amino_y - 1])


            # Aminos to and from that amino dont add to the score so remove them.
            # Amino the amino folds to.
            if amino.get_fold_coordinates() in xy_tocheck:
                xy_tocheck.remove(amino.get_fold_coordinates())

            if not index == 0:
                # Amino the amino GOT folded from.
                if chain[index - 1].coordinates in xy_tocheck:
                    xy_tocheck.remove(chain[index - 1].coordinates)

            # Check all coordinates around it and adjust score if a H is next to it.
            for coordinates in xy_tocheck:

                if mode_3d:
                    x, y, z = coordinates
                else:
                    x, y = coordinates

                if mode_3d == True:
                    column = matrix[0]
                    row = matrix[0][0]
                    # Check if in correct z range.
                    if z >= len(matrix) or z < 0:
                        continue
                # 2D
                else:
                    column = matrix
                    row = matrix[0]

                # Check if in correct y range
                if y < len(column) and y >= 0:
                    # Check if in correct x range
                    if  x < len(row) and x >= 0:

                        if mode_3d:
                            # Empty matrix spots are empty strings and shouldnt be considered


                            # If it isnt an Amino, dont need to check
                            if isinstance(matrix[z][y][x], Amino):

                                # Subtract ch_score for C/H bonds
                                if (matrix[z][y][x].atype in ["H", "C"] and amino.atype in ["H", "C"]) and (matrix[z][y][x].atype != amino.atype):
                                    total_score -= 1
                                # Subtract 5 for C/C bonds
                                elif amino.atype == "C" and matrix[z][y][x].atype == "C":
                                    total_score -= 5
                                # Subtract 1 for H/H bonds
                                elif amino.atype == "H" and matrix[z][y][x].atype == "H":
                                    total_score -= 1

                        # 2D
                        else:
                            # Empty matrix spots are empty strings and shouldnt be considered
                            if isinstance(matrix[y][x], Amino):

                                # Subtract ch_score for C/H bonds
                                if (matrix[y][x].atype in ["H", "C"] and amino.atype in ["H", "C"]) and (matrix[y][x].atype != amino.atype):
                                    total_score -= 1
                                # Subtract 5 for C/C bonds
                                elif amino.atype == "C" and matrix[y][x].atype == "C":
                                    total_score -= 5
                                # Subtract 1 for H/H bonds
                                elif amino.atype == "H" and matrix[y][x].atype == "H":
                                    total_score -= 1

        total_score = total_score // 2
        return total_score


# This function calculates and returns the score of the chain.
# This functions is used in searches and uses a non-offsetted chain + xy offfset instead of a offsetted chain.
def get_score_efficient(chain, matrix, xy_offset, ch_score):

        # Check if 3d mode.
        mode_3d = is_chain_3d(chain)

        total_score = 0

        if mode_3d:
            x_offset, y_offset, z_offset = xy_offset
        else:
            x_offset, y_offset = xy_offset

        # Iterate over all aminos and add the score of all of them.
        for index, amino in enumerate(chain):

            # P has no effect on stability
            if amino.atype == "P":
                continue

            # Creates a list with all coordinates that need to be checked.
            xy_tocheck = []
            # amino_x = amino.coordinates[0] - x_offset
            # amino_y = amino.coordinates[1] - y_offset

            amino_x = amino.coordinates[0]
            amino_y = amino.coordinates[1]

            if mode_3d:
                amino_z = amino.coordinates[2]

            if mode_3d:
                xy_tocheck.append([amino_x + 1, amino_y, amino_z])
                xy_tocheck.append([amino_x, amino_y + 1, amino_z])
                xy_tocheck.append([amino_x, amino_y, amino_z + 1])

            else:
                xy_tocheck.append([amino_x + 1, amino_y])
                xy_tocheck.append([amino_x, amino_y + 1])
                xy_tocheck.append([amino_x - 1, amino_y])
                xy_tocheck.append([amino_x, amino_y - 1])

            # Aminos to and from that amino dont add to the score so remove them.
            if amino.get_fold_coordinates() in xy_tocheck:
                xy_tocheck.remove(amino.get_fold_coordinates())

            if not index == 0:
                if chain[index - 1].coordinates in xy_tocheck:
                    xy_tocheck.remove(chain[index - 1].coordinates)

            for xy in xy_tocheck:
                xy[0] -= x_offset
                xy[1] -= y_offset
                if mode_3d:
                    xy[2] -= z_offset

            # Check all coordinates around it and adjust score if a H is next to it.
            for coordinates in xy_tocheck:

                if mode_3d:
                    x, y, z = coordinates
                else:
                    x, y = coordinates

                if mode_3d == True:
                    column = matrix[0]
                    row = matrix[0][0]
                    # Check if in correct z range.
                    if z >= len(matrix) or z < 0:
                        continue
                # 2D
                else:
                    column = matrix
                    row = matrix[0]

                # Only check if in correct y range
                if y < len(column) and y >= 0:
                    # Dito for the y range
                    if  x < len(row) and x >= 0:
                        # Empty matrix spots are empty strings and shouldnt be considered

                        if mode_3d:
                            matrix_amino = matrix[z][y][x]

                        else:
                            matrix_amino = matrix[y][x]

                        if isinstance(matrix_amino, Amino):

                            # Subtract ch_score for C/H bonds
                            if (matrix_amino.atype in ["H", "C"] and amino.atype in ["H", "C"]) and (matrix_amino.atype != amino.atype):
                                total_score -= ch_score
                            # Subtract 5 for C/C bonds
                            elif amino.atype == "H" and matrix_amino.atype == "H":
                                total_score -= 1
                            # Subtract 1 for H/H bonds
                            elif amino.atype == "C" and matrix_amino.atype == "C":
                                total_score -= 5
        total_score = total_score // 2
        return total_score


# This function calculates and returns the score of the chain.
# It takes the score of the chain before the last amino was added and only adds the score of the last amino
def get_score_iterative(chain, matrix, last_score):

    # Check if 3d mode.
    mode_3d = is_chain_3d(chain)

    # We start with the old score and add to it.
    total_score = last_score

    # Only the last amino has to be considered
    amino = chain[-1]

    # P has no effect on stability
    if amino.atype == "P":
        return total_score

    # Creates a list with all coordinates that need to be checked.
    xy_tocheck = []

    # 3D
    if mode_3d:
        amino_x, amino_y, amino_z = amino.coordinates
        xy_tocheck.append([amino_x + 1, amino_y, amino_z])
        xy_tocheck.append([amino_x, amino_y + 1, amino_z])
        xy_tocheck.append([amino_x - 1, amino_y, amino_z])
        xy_tocheck.append([amino_x, amino_y - 1, amino_z])
        xy_tocheck.append([amino_x, amino_y, amino_z - 1])
        xy_tocheck.append([amino_x, amino_y, amino_z + 1])

    # 2D
    else:
        amino_x, amino_y = amino.coordinates
        xy_tocheck.append([amino_x + 1, amino_y])
        xy_tocheck.append([amino_x, amino_y + 1])
        xy_tocheck.append([amino_x - 1, amino_y])
        xy_tocheck.append([amino_x, amino_y - 1])


    # Aminos to and from that amino dont add to the score so remove them.
    # Amino the amino folds to.
    if amino.get_fold_coordinates() in xy_tocheck:
        xy_tocheck.remove(amino.get_fold_coordinates())

    if not len(chain) == 1:
        # Amino the amino GOT folded from.
        if chain[-2].coordinates in xy_tocheck:
            xy_tocheck.remove(chain[-2].coordinates)

    # Check all coordinates around it and adjust score if a H is next to it.
    for coordinates in xy_tocheck:

        if mode_3d:
            x, y, z = coordinates
        else:
            x, y = coordinates


        if mode_3d == True:
            column = matrix[0]
            row = matrix[0][0]
            # Check if in correct z range.
            if z >= len(matrix) or z < 0:
                continue
        # 2D
        else:
            column = matrix
            row = matrix[0]

        # Check if in correct y range
        if y < len(column) and y >= 0:
            # Check if in correct x range
            if  x < len(row) and x >= 0:

                if mode_3d:
                    # Empty matrix spots are empty strings and shouldnt be considered

                    # If it isnt an Amino, dont need to check
                    if isinstance(matrix[z][y][x], Amino):

                        # Subtract ch_score for C/H bonds
                        if (matrix[z][y][x].atype in ["H", "C"] and amino.atype in ["H", "C"]) and (matrix[z][y][x].atype != amino.atype):
                            total_score -= 1
                        # Subtract 5 for C/C bonds
                        elif amino.atype == "C" and matrix[z][y][x].atype == "C":
                            total_score -= 5
                        # Subtract 1 for H/H bonds
                        elif amino.atype == "H" and matrix[z][y][x].atype == "H":
                            total_score -= 1

                # 2D
                else:
                    # Empty matrix spots are empty strings and shouldnt be considered
                    if isinstance(matrix[y][x], Amino):

                        # Subtract ch_score for C/H bonds
                        if (matrix[y][x].atype in ["H", "C"] and amino.atype in ["H", "C"]) and (matrix[y][x].atype != amino.atype):
                            total_score -= 1
                        # Subtract 5 for C/C bonds
                        elif amino.atype == "C" and matrix[y][x].atype == "C":
                            total_score -= 5
                        # Subtract 1 for H/H bonds
                        elif amino.atype == "H" and matrix[y][x].atype == "H":
                            total_score -= 1

    return total_score


# This function calculates and returns the score of the chain.
# It takes the score of the chain before the last amino was added and only adds the score of the last amino.
# Its also returns the available spots to add and delelte
def get_score_iterative_and_spots(chain, matrix, last_score):

    # Check if 3d mode.
    mode_3d = is_chain_3d(chain.chain_list)

    total_score = last_score
    available_spots_to_add = []
    available_spots_to_remove = []
    available_spots_to_add_C = []
    available_spots_to_remove_C = []
    
    # Onlt consider last amino
    amino = chain.chain_list[-1]

    # Creates a list with all coordinates that need to be checked.
    xy_tocheck = []

    # 3D
    if mode_3d:
        amino_x, amino_y, amino_z = amino.coordinates
        xy_tocheck.append([amino_x + 1, amino_y, amino_z])
        xy_tocheck.append([amino_x, amino_y + 1, amino_z])
        xy_tocheck.append([amino_x - 1, amino_y, amino_z])
        xy_tocheck.append([amino_x, amino_y - 1, amino_z])
        xy_tocheck.append([amino_x, amino_y, amino_z - 1])
        xy_tocheck.append([amino_x, amino_y, amino_z + 1])

    # 2D
    else:
        amino_x, amino_y = amino.coordinates
        xy_tocheck.append([amino_x + 1, amino_y])
        xy_tocheck.append([amino_x, amino_y + 1])
        xy_tocheck.append([amino_x - 1, amino_y])
        xy_tocheck.append([amino_x, amino_y - 1])


    # Aminos to and from that amino dont add to the score so remove them.
    # Amino the amino folds to.
    if amino.get_fold_coordinates() in xy_tocheck:
        xy_tocheck.remove(amino.get_fold_coordinates())

    if not len(chain.chain_list) == 1:
        # Amino the amino GOT folded from.
        if chain.chain_list[-2].coordinates in xy_tocheck:
            xy_tocheck.remove(chain.chain_list[-2].coordinates)

    # Check all coordinates around it and adjust score if a H is next to it.
    for coordinates in xy_tocheck:

        if mode_3d:
            x, y, z = coordinates
        else:
            x, y = coordinates

        if mode_3d == True:
            column = matrix[0]
            row = matrix[0][0]
            # Check if in correct z range.
            if z >= len(matrix) or z < 0:
                continue
        # 2D
        else:
            column = matrix
            row = matrix[0]

        # Check if in correct y range
        if y < len(column) and y >= 0:
            # Check if in correct x range
            if  x < len(row) and x >= 0:

                if mode_3d:
                    # Empty matrix spots are empty strings and shouldnt be considered

                    # If it isnt an Amino, dont need to check
                    if isinstance(matrix[z][y][x], Amino):

                        # Subtract ch_score for C/H bonds
                        if (matrix[z][y][x].atype in ["H", "C"] and amino.atype in ["H", "C"]) and (matrix[z][y][x].atype != amino.atype):
                            total_score -= 1
                            if amino.atype == "H":
                                available_spots_to_remove_C.append(amino.coordinates)

                            if amino.atype == "C":
                                 available_spots_to_remove.append(amino.coordinates)
                            continue

                        # Subtract 5 for C/C bonds
                        elif amino.atype == "C" and matrix[z][y][x].atype == "C":
                            total_score -= 5
                            available_spots_to_remove_C.append(amino.coordinates)
                            continue

                        # Subtract 1 for H/H bonds
                        elif amino.atype == "H" and matrix[z][y][x].atype == "H":
                            total_score -= 1
                            available_spots_to_remove.append(amino.coordinates)
                            continue

                        elif amino.atype == "P" and matrix[z][y][x].atype == "H":
                            available_spots_to_remove.append(amino.coordinates)
                            continue
                    
                    elif amino.atype == "H":
                        available_spots_to_add.append([x, y, z])
                    
                    elif amino.atype == "C":
                        available_spots_to_add_C.append([x, y, z])

                # 2D
                else:
                    # Empty matrix spots are empty strings and shouldnt be considered
                    if isinstance(matrix[y][x], Amino):

                        # Subtract ch_score for C/H bonds
                        if (matrix[y][x].atype in ["H", "C"] and amino.atype in ["H", "C"]) and (matrix[y][x].atype != amino.atype):
                            total_score -= 1
                            if amino.atype == "H":
                                available_spots_to_remove_C.append(amino.coordinates)

                            if amino.atype == "C":
                                 available_spots_to_remove.append(amino.coordinates)
                            
                            continue

                        # Subtract 5 for C/C bonds
                        elif amino.atype == "C" and matrix[y][x].atype == "C":
                            total_score -= 5
                            available_spots_to_remove_C.append(amino.coordinates)
                            continue

                        # Subtract 1 for H/H bonds
                        elif amino.atype == "H" and matrix[y][x].atype == "H":
                            total_score -= 1
                            available_spots_to_remove.append(amino.coordinates)
                            continue

                        elif amino.atype == "P" and matrix[y][x].atype == "H":
                            available_spots_to_remove.append(amino.coordinates)
                            continue
                        
                    elif amino.atype == "H":
                        available_spots_to_add.append([x, y])
                    
                    elif amino.atype == "C":
                        available_spots_to_add_C.append([x, y])

    return total_score, available_spots_to_add, available_spots_to_remove, available_spots_to_add_C, available_spots_to_remove_C
# def get_score_efficient_and_wasted_points(chain, matrix, xy_offset, ch_score, wasted_score):
def get_score_efficient_and_wasted_points(chain, matrix, xy_offset, ch_score):

        # Check if 3d mode.
        mode_3d = is_chain_3d(chain)

        total_score = 0
        points_wasted = 0

        if mode_3d:
            x_offset, y_offset, z_offset = xy_offset

        else:
            x_offset, y_offset = xy_offset

        # Iterate over all aminos and add the score of all of them.
        for index, amino in enumerate(chain):

            # P has no effect on stability
            if amino.atype == "P":
                continue

            # Creates a list with all coordinates that need to be checked.
            xy_tocheck = []
            # amino_x = amino.coordinates[0] - x_offset
            # amino_y = amino.coordinates[1] - y_offset

            amino_x = amino.coordinates[0]
            amino_y = amino.coordinates[1]

            if mode_3d:
                amino_z = amino.coordinates[2]


            if mode_3d:
                xy_tocheck.append([amino_x + 1, amino_y, amino_z])
                xy_tocheck.append([amino_x, amino_y + 1, amino_z])
                xy_tocheck.append([amino_x, amino_y, amino_z + 1])

            else:
                xy_tocheck.append([amino_x + 1, amino_y])
                xy_tocheck.append([amino_x, amino_y + 1])


            # Aminos to and from that amino dont add to the score so remove them.
            if amino.get_fold_coordinates() in xy_tocheck:
                xy_tocheck.remove(amino.get_fold_coordinates())

            if not index == 0:
                if chain[index - 1].coordinates in xy_tocheck:
                    xy_tocheck.remove(chain[index - 1].coordinates)

            for xy in xy_tocheck:
                xy[0] -= x_offset
                xy[1] -= y_offset
                if mode_3d:
                    xy[2] -= z_offset


            # Check all coordinates around it and adjust score if a H is next to it.
            for coordinates in xy_tocheck:

                if mode_3d:
                    x, y, z = coordinates
                else:
                    x, y = coordinates

                if mode_3d == True:
                    column = matrix[0]
                    row = matrix[0][0]
                    # Check if in correct z range.
                    if z >= len(matrix) or z < 0:
                        continue
                # 2D
                else:
                    column = matrix
                    row = matrix[0]

                # Only check if in correct y range
                if y < len(column) and y >= 0:
                    # Dito for the y range
                    if  x < len(row) and x >= 0:
                        # Empty matrix spots are empty strings and shouldnt be considered

                        if mode_3d:
                            matrix_amino = matrix[z][y][x]

                        else:
                            matrix_amino = matrix[y][x]

                        if isinstance(matrix_amino, Amino):

                            # Subtract ch_score for C/H bonds
                            if (matrix_amino.atype in ["H", "C"] and amino.atype in ["H", "C"]) and (matrix_amino.atype != amino.atype):
                                total_score -= ch_score
                            # Subtract 5 for C/C bonds
                            elif amino.atype == "H" and matrix_amino.atype == "H":
                                total_score -= 1
                            # Subtract 1 for H/H bonds
                            elif amino.atype == "C" and matrix_amino.atype == "C":
                                total_score -= 5


                            # look at wasted points
                            if matrix_amino.atype == "P" and amino.atype == "H":
                                # points_wasted += wasted_score
                                points_wasted += 1
                            elif matrix_amino.atype == "P" and amino.atype == "C":
                                # points_wasted += (wasted_score * 5)
                                points_wasted += 5

        # you could combine the scores inmediatly 
        total_score = total_score - points_wasted                        

        return total_score
