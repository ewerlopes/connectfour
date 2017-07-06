import numpy as np

from c4.board import Board, PLAYER1, PLAYER2, DRAW

INF = 1000


class Evaluator(object):
    def __init__(self, weights=[0, 0, 1, 4, 0]):
        self._weights = np.asarray(weights)

    def evaluate(self, board):
        scores = {PLAYER1: np.zeros(5, dtype=int),
                  PLAYER2: np.zeros(5, dtype=int)}

        if board.end is not None:
            if board.end == DRAW:
                return 0
            elif board.end == board.get_next_to_move:
                return INF
            else:
                return -INF

        segments = Board.segments(board)
        filtered_segments = segments[segments.any(1)]

        for s in filtered_segments:
            c = np.bincount(s, minlength=3)

            c1 = c[PLAYER1]
            c2 = c[PLAYER2]

            if c2 == 0:
                scores[PLAYER1][c1] += 1
            elif c1 == 0:
                scores[PLAYER2][c2] += 1

        s1 = (self._weights * scores[PLAYER1]).sum()
        s2 = (self._weights * scores[PLAYER2]).sum()

        score = s1 - s2
        if board.get_next_to_move == PLAYER1:
            return score
        else:
            return -score
