# Depth-search

## implemented:
- removes usage of deepcopy, x5 speedup
- Lookahead implemented, is awesome.

## to implement:


# Breadth-search

## Implemented:

itself

## to implement:
- beam-search


# Pruning methods

## Implemented:

## To implement:
- Check max score achievable, abort if lower than best.
- prune mirrored version, x2 speedup?

# Heuristics

## To implement
- Compactness / amount of folds/ uitgerektness.
- lost points by saturated aminos.


# Ideas.

- Return ALL best chains. to compare
- Instead of creating the matrix and score from scratch for every chain with a single new amino, take the score and matrix from the last chain, and append the new amino to the matrix and score.



# TODO
- Max achievable score function.
- Remoce c-h bondds from search functions so search doesnt sacrifice Adjecent C spots for kjust 01
- Add C-H bonds to get_score functions

https://www.geeksforgeeks.org/queue-in-python/  Queue.queue

amino.24 do we still use protein.index??
protein.46 is ideal chain still used?
protein.50 do we still use char_counter??



# errors:

Hv H> H> P^ H^ H< Pv H@ score-3
score after xy ofset: -2

Hv H> Hv P> H^ H^ P< H@ score-3
score after xy ofset: -2


-3 Hv Hv H> P^ H^ H> Pv H@
-3Hv Hv H> P^ H^ H^ P< H@
-3Hv Hv H< P^ H< H^ P> H@
-3Hv Hv H< P^ H^ H< Pv H@
-3Hv Hv H< P^ H^ H^ P> H@
