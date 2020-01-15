from classes.amino import Amino

# Takes the chain and makes a 2d matrix out of it. Returns a matrix and a ofsetted chain
def get_matrix(chain):

    x_range = [0, 0]
    y_range = [0, 0]

    # Check if 3d mode
    if len(chain[0].coordinates) == 3:
        mode_3d = True
        z_range = [0, 0]

    else:
        mode_3d = False

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

        # Z-axis for 3d mode
        if mode_3d:
            if amino.coordinates[2] > z_range[1]:
                z_range[1] = amino.coordinates[2]
            elif amino.coordinates[2] < z_range[0]:
                z_range[0] = amino.coordinates[2]

    # Adjust amino coordinates so no negative values remain.
    for amino in chain:
        amino.coordinates[0] -= x_range[0]
        amino.coordinates[1] -= y_range[0]

        if mode_3d:
            amino.coordinates[2] -= z_range[0]

    matrix = []

    # Fill matrix with placeholder values. The array indexes are reversed, so: matrix[z][y][x]
    # 3D
    if mode_3d:
        for k in range(z_range[1] - z_range[0] + 1):
            layer = []
            for i in range(y_range[1] - y_range[0] + 1):
                row = []
                for j in range(x_range[1] - x_range[0] + 1):
                    row.append(" ")
                layer.append(row)
            matrix.append(layer)
    # 2D
    else:
        for i in range(y_range[1] - y_range[0] + 1):
            row = []
            for j in range(x_range[1] - x_range[0] + 1):
                row.append(" ")
            matrix.append(row)



    # Adds aminos to matrix.
    # 3D
    if mode_3d:
        for amino in chain:
            matrix[amino.coordinates[2]][amino.coordinates[1]][amino.coordinates[0]] = amino

    # 2D
    else:
        for amino in chain:
            matrix[amino.coordinates[1]][amino.coordinates[0]] = amino

    return matrix, chain

# Takes the chain and makes a 2d matrix out of it. Returns a matrix and xy_offset
# This function is used in searches so the original chain isnt changed.
def get_matrix_efficient(chain):

    x_range = [0, 0]
    y_range = [0, 0]

    # Check if 3d mode
    if len(chain[0].coordinates) == 3:
        mode_3d = True
        z_range = [0, 0]

    else:
        mode_3d = False

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

        # Z-axis for 3d mode
        if mode_3d:
            if amino.coordinates[2] > z_range[1]:
                z_range[1] = amino.coordinates[2]
            elif amino.coordinates[2] < z_range[0]:
                z_range[0] = amino.coordinates[2]

    matrix = []

    # Fill matrix with placeholder values. The array indexes are reversed, so: matrix[z][y][x]
    # 3D
    if mode_3d:
        for k in range(z_range[1] - z_range[0] + 1):
            layer = []
            for i in range(y_range[1] - y_range[0] + 1):
                row = []
                for j in range(x_range[1] - x_range[0] + 1):
                    row.append(" ")
                layer.append(row)
            matrix.append(layer)
    # 2D
    else:
        for i in range(y_range[1] - y_range[0] + 1):
            row = []
            for j in range(x_range[1] - x_range[0] + 1):
                row.append(" ")
            matrix.append(row)


    # Adds aminos to matrix.
    if mode_3d:
        for amino in chain:
            matrix[amino.coordinates[2] - z_range[0]][amino.coordinates[1] - y_range[0]][amino.coordinates[0] - x_range[0]] = amino
    # 2D
    else:
        for amino in chain:
            matrix[amino.coordinates[1] - y_range[0]][amino.coordinates[0] - x_range[0]] = amino

    if mode_3d:
        offset = [x_range[0], y_range[0], z_range[0]]

    else:
        offset = [x_range[0], y_range[0]]

    return matrix, offset

