import random

from classes.protein import Protein
from algorithms.RandomSearch import random_search
from algorithms.DepthSearch import depth_search
from algorithms.helpers import get_fold_number
from algorithms.breadth_first import breadth_search


if __name__ == "__main__":

    protein1 = Protein("HPPHPCPPHPPHPHCH", "2D")
    breadth_search(protein1)
