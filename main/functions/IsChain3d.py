# Authors: Brent van Dodewaard, Jop van Hest, Luitzen de Vries.
# Heuristics programming project: Protein pow(d)er.

# This function returns True if 3d mode, false in 2d_mode
def is_chain_3d(chain):
    if len(chain[0].coordinates) == 2:
        return False
    return True