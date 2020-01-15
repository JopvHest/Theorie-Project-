from classes.amino import Amino

# This function calculates and returns the score of the chain.
def get_score(chain, matrix):

        # Check if 3d mode.
        if len(chain[0].coordinates) == 3:
            mode_3d = True

        else:
            mode_3d = False

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

                                # If they are both H, score -= 1
                                if matrix[z][y][x].atype == "H" and amino.atype == "H":
                                    total_score -= 1

                                # If they are both C, score -= 5
                                elif amino.atype == "C" and matrix[z][y][x].atype == "C":
                                    total_score -= 5
                        # 2D
                        else:
                            # Empty matrix spots are empty strings and shouldnt be considered
                            if isinstance(matrix[y][x], Amino):

                                # If they are both H, score -= 1
                                if matrix[y][x].atype == "H" and amino.atype == "H":
                                    total_score -= 1

                                # If they are both C, score -= 5
                                elif amino.atype == "C" and matrix[y][x].atype == "C":
                                    total_score -= 5
        total_score = total_score // 2
        return total_score


# This function calculates and returns the score of the chain.
# This functions is used in searches and uses a non-offsetted chain + xy offfset instead of a offsetted chain.
def get_score_efficient(chain, matrix, xy_offset):

        # Check if 3d mode.
        if len(chain[0].coordinates) == 3:
            mode_3d = True

        else:
            mode_3d = False

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


            # Aminos to and from that amino dont add to the score so remove them.
            if amino.get_fold_coordinates() in xy_tocheck:
                xy_tocheck.remove(amino.get_fold_coordinates())

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


                            if matrix_amino.atype == "H" and amino.atype == "H":
                                total_score -= 1

                            elif amino.atype == "C" and matrix_amino.atype == "C":
                                total_score -= 5
        return total_score


def get_score_efficient_and_compactness(chain, matrix, xy_offset):

        total_score = 0
        compactness = 0

        x_offset, y_offset = xy_offset

        # Iterate over all aminos and add the score of all of them.
        for index, amino in enumerate(chain):



            # Creates a list with all coordinates that need to be checked.
            xy_tocheck = []
            amino_x = amino.coordinates[0] - x_offset
            amino_y = amino.coordinates[1] - y_offset

            xy_tocheck.append([amino_x + 1, amino_y])
            xy_tocheck.append([amino_x, amino_y + 1])
            xy_tocheck.append([amino_x - 1, amino_y])
            xy_tocheck.append([amino_x, amino_y - 1])

            # Aminos to and from that amino dont add to the score so remove them.
            if amino.get_fold_coordinates() in xy_tocheck:
                xy_tocheck.remove(amino.get_fold_coordinates())

            if chain[index - 1].coordinates in xy_tocheck:
                xy_tocheck.remove(chain[index - 1].coordinates)

            # Check all coordinates around it and adjust score if a H is next to it.
            for x, y in xy_tocheck:
                if y < len(matrix) and y >= 0:
                    if  x < len(matrix[0]) and x >= 0:
                        if isinstance(matrix[y][x], Amino):
                            compactness += 1
                            # P has no effect on stability
                            if amino.atype != "P":
                                if matrix[y][x].atype == "H":
                                    total_score -= 1
        total_score = total_score // 2
        compactness = compactness // 2
        return total_score
