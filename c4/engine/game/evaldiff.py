import numpy as np

from c4.engine.search.searchProblem import Connect4
from c4.engine.game.evaluate import INF
from c4.engine.search.utils import evaldiff_lookup, evaldiff_threat_lookup


def evaldiff(board, m, weights=np.array([1, 3, 9, 27], dtype=int)):
    r = board.freerow(m)
    stm = board.whose_turn_is_it
    indices = np.dot(Connect4.segments_around(board, r, m),
                     weights)
    partial_scores = evaldiff_lookup[stm][indices]

    if (partial_scores == 4**2).any():
        return INF

    if evaldiff_threat_lookup[stm][indices].any():
        return INF - 1

    return partial_scores.sum()
