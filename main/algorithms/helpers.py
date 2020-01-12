from classes.amino import Amino

# Takes the chain and makes a 2d matrix out of it. Returns a matrix and a ofsetted chain
def get_matrix(chain):

    x_range = [0, 0]
    y_range = [0, 0]

    # Define min/max x and y values over all aminos.
    for amino in chain:
        if amino.coordinates[0] > x_range[1]:
            x_range[1] = amino.coordinates[0]
        elif amino.coordinates[0] < x_range[0]:
            x_range[0] = amino.coordinates[0]
        if amino.coordinates[1] > y_range[1]:
            y_range[1] = amino.coordinates[1]
        elif amino.coordinates[1] < y_range[0]:
            y_range[0] = amino.coordinates[1]

    # Adjust amino coordinates so no negative values remain.
    for amino in chain:
        amino.coordinates[0] -= x_range[0]
        amino.coordinates[1] -= y_range[0]

    matrix = []

    # Fill matrix with placeholder values.
    for i in range(y_range[1] - y_range[0] + 1):
        row = []
        for j in range(x_range[1] - x_range[0] + 1):
            row.append(" ")
        matrix.append(row)


    # Adds aminos to matrix.
    for amino in chain:
        matrix[amino.coordinates[1]][amino.coordinates[0]] = amino

    return matrix, chain

# Takes the chain and makes a 2d matrix out of it. Returns a matrix and xy_offset
# This function is used in searches so the original chain isnt changed.
def get_matrix_efficient(chain):

    x_range = [0, 0]
    y_range = [0, 0]

    # Define min/max x and y values over all aminos.
    for amino in chain:
        if amino.coordinates[0] > x_range[1]:
            x_range[1] = amino.coordinates[0]
        elif amino.coordinates[0] < x_range[0]:
            x_range[0] = amino.coordinates[0]
        if amino.coordinates[1] > y_range[1]:
            y_range[1] = amino.coordinates[1]
        elif amino.coordinates[1] < y_range[0]:
            y_range[0] = amino.coordinates[1]

    matrix = []

    # Fill matrix with placeholder values.
    for i in range(y_range[1] - y_range[0] + 1):
        row = []
        for j in range(x_range[1] - x_range[0] + 1):
            row.append(" ")
        matrix.append(row)


    # Adds aminos to matrix.
    for amino in chain:
        matrix[amino.coordinates[1] - y_range[0]][amino.coordinates[0] - x_range[0]] = amino

    return matrix, [x_range[0], y_range[0 ]]


# This function calculates and returns the score of the chain.
def get_score(chain, matrix):

        total_score = 0

        # Iterate over all aminos and add the score of all of them.
        for index, amino in enumerate(chain):

            # P has no effect on stability
            if amino.atype == "P":
                continue

            # Creates a list with all coordinates that need to be checked.
            xy_tocheck = []
            amino_x, amino_y = amino.coordinates
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
                # Only check if in correct y range
                if y < len(matrix) and y >= 0:
                    # Dito for x
                    if  x < len(matrix[0]) and x >= 0:
                        # Empty matrix spots are empty strings and shouldnt be considered
                        if isinstance(matrix[y][x], Amino):
                            
                            if matrix[y][x].atype == "H" and amino.atype == "H":
                                total_score -= 1
                            
                            elif amino.atype == "C" and matrix[y][x].atype == "C":
                                total_score -= 5
        total_score = total_score // 2
        return total_score


# This function calculates and returns the score of the chain.
# This functions is used in searches and uses a non-offsetted chain + xy offfset instead of a offsetted chain.
def get_score_efficient(chain, matrix, xy_offset):

        total_score = 0
        
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
            

            # Check all coordinates around it and adjust score if a H is next to it.
            for x, y in xy_tocheck:
                # Only check if in correct y range
                if y < len(matrix) and y >= 0:
                    # Dito for the y range
                    if  x < len(matrix[0]) and x >= 0:
                        # Empty matrix spots are empty strings and shouldnt be considered
                        if isinstance(matrix[y][x], Amino):
                            
                            
                            if matrix[y][x].atype == "H" and amino.atype == "H":
                                total_score -= 1
                            
                            elif amino.atype == "C" and matrix[y][x].atype == "C":
                                total_score -= 5
        return total_score

    