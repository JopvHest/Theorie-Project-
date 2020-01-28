# Authors: Brent van Dodewaard, Jop van Hest, Luitzen de Vries.
# Heuristics programming project: Protein pow(d)er.

from classes.amino import Amino


# makes and returns a list of surrounding coordinates
def check_coordinates(amino, dimension):
    
    xy_tocheck = []

    # 3D
    if dimension is True:
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

    return xy_tocheck