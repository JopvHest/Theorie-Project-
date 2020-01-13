# pseudocode

# stack = list with all current chains.
# Only has 1 chain at the start. a chain with the start move.

# While True:
#   for chain in stack:
#       remove chain from stack
#       for move in legal_moves(chain):
#           add chain+move to the chain. At the place of the original chain (That got removed)
# When every chain in the stack arrived at the end of the amino_string. Compare the scores of ALL chains. 

# For beam search we compare all the chains every x turns and remove the worst x procent.

