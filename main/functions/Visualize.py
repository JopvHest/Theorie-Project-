from classes.amino import Amino
from functions.IsChain3d import is_chain_3d

def get_connections(chain, matrix):

        # Check if 3d mode.
        mode_3d = is_chain_3d(chain)

        connections = []

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
                            # If it isnt an Amino, dont need to check
                            if isinstance(matrix[z][y][x], Amino):

                                # If they are both H, score -= 1
                                if (matrix[z][y][x].atype in ["H", "C"] and amino.atype in ["H", "C"]) and (matrix[z][y][x].atype != amino.atype):
                                    connections.append([1, [x, y, z], amino.coordinates])
                                # If they are both C, score -= 5
                                elif amino.atype == "H" and matrix[z][y][x].atype == "H":
                                    connections.append([1, [x, y, z], amino.coordinates])
                                # If they are both C, score -= 5
                                elif amino.atype == "C" and matrix[z][y][x].atype == "C":
                                    connections.append([5, [x, y, z], amino.coordinates])

                        # 2D
                        else:
                            # Empty matrix spots are empty strings and shouldnt be considered
                            if isinstance(matrix[y][x], Amino):

                                # If they are both H, score -= 1
                                if (matrix[y][x].atype in ["H", "C"] and amino.atype in ["H", "C"]) and (matrix[y][x].atype != amino.atype):
                                    connections.append([1, [x, y], amino.coordinates])
                                # If they are both C, score -= 5
                                elif amino.atype == "H" and matrix[y][x].atype == "H":
                                    connections.append([1, [x, y], amino.coordinates])
                                # If they are both C, score -= 5
                                elif amino.atype == "C" and matrix[y][x].atype == "C":
                                    connections.append([5, [x, y], amino.coordinates])
        return connections

