
# Determines if a remaining chain can reach a particular spot of an available fold based on the manhatten distance.
def chain_can_reach_spot(amino_coordinates, spot_coordinates, remaining_aminos):

    # Calculates the manhatten distance between the two spots
    manhatten_distance = 0
    for index, coordinate in enumerate(amino_coordinates):
        manhatten_distance += abs(coordinate - spot_coordinates[index])
    
    # Cant reach if manhatten distance is greater than the remaining aminos.
    if remaining_aminos < manhatten_distance:
        return False
    
    return True