# Authors: Brent van Dodewaard, Jop van Hest, Luitzen de Vries.
# Heuristics programming project: Protein pow(d)er.

def get_fold_number(chain):

        folds = 0

        # Iterate over all aminos and add the score of all of them.
        for index, amino in enumerate(chain):
            print(amino)

            amino_before = chain[index-1]
            print(abs(amino.fold))
            print(abs(amino_before.fold))
            if abs(amino_before.fold) != 0:
                if abs(amino.fold) != 0:
                    if abs(amino.fold) != abs(amino_before.fold):
                        if amino.fold != 0:
                            folds += 1
                            print("folds" + str(folds))
        print("folds" + str(folds))
        return(folds)
