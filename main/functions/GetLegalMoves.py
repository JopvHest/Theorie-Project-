from functions.IsChain3d import is_chain_3d


# Finds all the legal moves that can be made from the current position.
# Returns False for no ideal chain found.
def get_legal_moves(xy, chain):

    mode_3d = is_chain_3d(chain)

    # These are lists of tuples with 1: the move, 2: the coordinates delta that cant exist yet.
    if mode_3d:
        moves_xydelta = [[1, (1, 0, 0)], [-1, (-1, 0, 0)], [2, (0, 1, 0)], [-2, (0, -1, 0)], [3, (0, 0, 1)], [-3, (0, 0, -1)]]
    else:
        moves_xydelta = [[1, (1, 0)], [-1, (-1, 0)], [2, (0, 1)], [-2, (0, -1)]]

    # Check if the legal moves interfere with any of the current amino coordinates.
    # Note: we iterate over a COPY of the list because you cant delete items from a list while iterating over it.
    for amino in list(chain):
        # Check for every legal move left.
        for move in moves_xydelta:

           # If the move delta plus current xy is equal to another amino's xy remove it from the legal moves list.
            if mode_3d:
                coordinates_sum = []
                coordinates_sum.append(move[1][0] + xy[0])
                coordinates_sum.append(move[1][1] + xy[1])
                coordinates_sum.append(move[1][2] + xy[2])

            else:
                coordinates_sum = []
                coordinates_sum.append(move[1][0] + xy[0])
                coordinates_sum.append(move[1][1] + xy[1])

            if coordinates_sum == list(amino.coordinates):
                moves_xydelta.remove(move)

    # Only return the move int of the legal moves remaining.
    legal_moves = []
    for moves in moves_xydelta:
        legal_moves.append(moves[0])

    return legal_moves

# This is a version of the legal moves which removes the moves which lead to a mirror version.
def get_legal_moves_nomirror(xy, chain):

    mode_3d = is_chain_3d(chain.chain_list)

    # This is a list of tuples with 1: the move, 2: the coordinates delta that cant exist yet.
    if mode_3d:
        moves_xydelta = [[1, (1, 0, 0)], [-1, (-1, 0, 0)], [2, (0, 1, 0)], [-2, (0, -1, 0)], [3, (0, 0, 1)], [-3, (0, 0, -1)]]
    else:
        if chain.can_still_mirror:
            moves_xydelta = [[1, (1, 0)], [2, (0, 1)], [-2, (0, -1)]]
        else:
            moves_xydelta = [[1, (1, 0)], [-1, (-1, 0)], [2, (0, 1)], [-2, (0, -1)]]

    # Check if the legal moves interfere with any of the current amino coordinates.
    # Note: we iterate over a COPY of the list because you cant delete items from a list while iterating over it.
    for amino in list(chain.chain_list):
        # Check for every legal move left.
        for move in moves_xydelta:

           # If the move delta plus current xy is equal to another amino's xy remove it from the legal moves list.
            if mode_3d:
                coordinates_sum = []
                coordinates_sum.append(move[1][0] + xy[0])
                coordinates_sum.append(move[1][1] + xy[1])
                coordinates_sum.append(move[1][2] + xy[2])

            else:
                coordinates_sum = []
                coordinates_sum.append(move[1][0] + xy[0])
                coordinates_sum.append(move[1][1] + xy[1])

            if coordinates_sum == list(amino.coordinates):
                moves_xydelta.remove(move)

    # Only return the move int of the legal moves remaining.
    legal_moves = []
    for moves in moves_xydelta:
        legal_moves.append(moves[0])

    return legal_moves