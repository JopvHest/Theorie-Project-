# pseudo code
# take all chains
# go trough the chains
# make dictionary in a dictionary and store move per amino with int
from classes.amino import Amino
from classes.chain import Chain


# takes a list of chains
def compare_chains(chains):


    for chain in chains:
        for index, amino in enumerate(chain.chain_list):
            fold = amino.fold
            setdefault
            dictionary = {index: {fold: int}, index: {fold: int}}

            coordinates = amino.coordinates
            dictionary2 = {index: {coordinates: int}  }
            
            