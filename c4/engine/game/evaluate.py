import numpy as np

from c4.engine.search.searchProblem import Connect4

INF = 1000


class Evaluator(object):
    def __init__(self, weights=[0, 0, 1, 4, 0]):
        self._weights = np.asarray(weights)

    def evaluate(self, board):
        scores = {Connect4.PLAYER1_ID: np.zeros(5, dtype=int),
                  Connect4.PLAYER2_ID: np.zeros(5, dtype=int)}

        if board.end is not None:
            if board.end == Connect4.DRAW_ID:
                return 0
            elif board.end == board.whose_turn_is_it:
                return INF
            else:
                return -INF

        segments = Connect4.segments(board)
        filtered_segments = segments[segments.any(1)]

        for s in filtered_segments:
            c = np.bincount(s, minlength=3)

            c1 = c[Connect4.PLAYER1_ID]
            c2 = c[Connect4.PLAYER2_ID]

            if c2 == 0:
                scores[Connect4.PLAYER1_ID][c1] += 1
            elif c1 == 0:
                scores[Connect4.PLAYER2_ID][c2] += 1

        s1 = (self._weights * scores[Connect4.PLAYER1_ID]).sum()
        s2 = (self._weights * scores[Connect4.PLAYER2_ID]).sum()

        score = s1 - s2
        if board.whose_turn_is_it == Connect4.PLAYER1_ID:
            return score
        else:
            return -score
