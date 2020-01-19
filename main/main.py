import sys, time

from classes.protein import Protein
from classes.amino import Amino
from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search
from algorithms.DepthSearchLookahead import depth_search_lookahead
from algorithms.BreadthSearch import breadth_search
from algorithms.DepthSearchIterative import depth_search_iterative
from algorithms.DepthSearchFoldSpots import depth_search_iterative_and_spots

from functions.GetMatrix import get_matrix_efficient
from functions.GetScore import get_score_efficient


if __name__ == "__main__":

    # chain = [Amino("H", 2, [0,0]), Amino("H", 2, [0,1]), Amino("H", 1, [0,2]), Amino("P", -2, [1,2]), Amino('H', -2, [1,1]), Amino("H", 1, [1, 0]), Amino("P", 2, [2, 0]), Amino("H", 0, [2,1])]
    start_time = time.clock()
    
    protein1 = Protein("HHPPHHPPHHPPPPHHPPPHHHH", "2D")

    depth_search_iterative_and_spots(protein1, 1, 0)
    print(protein1.get_score())
    print("--- %s seconds ---" % (time.clock() - start_time))
    

    # matrix, offset = get_matrix_efficient(chain)


    
   
    

    
    # protein1 = Protein("HPPHHHPPHHPH", "2D")
    # depth_search(protein1, 0.5)
    

    # start_time = time.clock()
    


