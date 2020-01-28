# Authors: Brent van Dodewaard, Jop van Hest, Luitzen de Vries.
# Heuristics programming project: Protein pow(d)er.

def get_fold_number(chain):

        folds = 0

        # Iterate over all aminos and count the amount of folds.
        for index, amino in enumerate(chain):

            amino_before = chain[index-1]
            
            if abs(amino_before.fold) != 0:
                if abs(amino.fold) != 0:
                    if abs(amino.fold) != abs(amino_before.fold):
                        if amino.fold != 0:
                            folds += 1
        return(folds)
