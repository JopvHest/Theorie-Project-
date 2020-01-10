import time
import copy

class Amino(object):

    def __init__(self, atype, fold, coordinates):
        self.atype = atype
        self.fold = fold
        self.coordinates = coordinates

        # Contains illegal folds for this amino based on that the next location wouldnt have legal moves.
        self.illegal_folds = []

    def __str__(self):
        directions = {"0":"@", "2":"v", "-2":"^", "1":">", "-1":"<"}
        string = str(self.atype) + " " + directions[str(self.fold)]
        return string


if __name__ == "__main__":
    
    chain = []
    
    types = ["P", "H"]
    folds = [1, -1, 2, -1]
    coordinates = [[1,2],[2,1]]

    for atype in types:
        for fold in folds:
            for coordinate in coordinates:
                chain.append(Amino(atype, fold, coordinates))
    
for amino in chain:
    print(amino, end =' ')
print("")
print(len(chain))

del chain[-1]
for amino in chain:
    print(amino, end=" ")
print(len(chain))

'''
start_time = time.clock()
newchain = copy.deepcopy(chain)
amino1 = Amino("H", -2, [3,5])
newchain.append(amino1)
print("--- %s seconds ---" % (time.clock() - start_time))

start_time = time.clock()

amino2 = Amino("H", -2, [3,5])
chain.append(amino2)
del chain[-1]
print("--- %s seconds ---" % (time.clock() - start_time))
'''



