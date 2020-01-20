# Depth-search

## implemented:
- removes usage of deepcopy, x5 speedup
- Lookahead implemented, is awesome.

## to implement:


# Breadth-search

## Implemented:


## to implement:
- Lookahead
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
protein.50 do we still use char_counter??



# errors:

Hv H> H> P^ H^ H< Pv H@ score-3
score after xy ofset: -2

Hv H> Hv P> H^ H^ P< H@ score-3
score after xy ofset: -2

Hv Hv H> P^ H> H^ P< H@
-3 Hv Hv H> P^ H^ H> Pv H@
-3Hv Hv H> P^ H^ H^ P< H@
-3Hv Hv H< P^ H< H^ P> H@
-3Hv Hv H< P^ H^ H< Pv H@
-3Hv Hv H< P^ H^ H^ P> H@

# Wasted score'
Score = normal_score - wasted_score

Total-wasted = 0

For every amino:
    for every amino that is adjacent:
        if not connected(from or to amino):
            total-wasted += wasted_x

wasted_x should be between 0 and 1 for H

for c? idk. Maybe between 0-5. But that wouldnt make sense if there is for example only 1 C in a protein.

Wat te doen?
-   Branch and bound - lookahead.
-   Branch and bound - as in paper with random throwaway.
-   iterative -> hill cimbing
-   heuristics -> compactness
-   Branch and bound 3d mweh..
