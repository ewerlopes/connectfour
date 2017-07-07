import math
import random
from collections import defaultdict

from c4.engine.search.searchProblem import Connect4
from c4.engine.ai.base import Engine
from c4.engine.ai.greedy import WeightedGreedyEngine


class MonteCarloTreeSearch(Engine):
    def __init__(self, simulations=1000, C=1/math.sqrt(2)):
        super(MonteCarloTreeSearch, self).__init__()
        self.simulations = int(simulations)
        self.C = float(C)
        self.simulation_engine = WeightedGreedyEngine(False)
        self._stats = defaultdict(lambda: [0, 0])

    def choose(self, board):
        stats, depth = self.search(board, self.simulations, self.C)
        return self.select_best_move(stats, depth, board)

    def search(self, board, simulations, C):
        stats = self._stats
        root = board
        max_depth = 0

        for i in range(simulations):
            node = root
            states = []

            # select leaf node
            depth = 0
            while node.end is None:
                depth += 1
                move, select = self.select_next_move(stats, node, C)
                node = node.move(move)
                states.append(node.hashkey()[0])

                if not select:
                    break

            max_depth = max(depth, max_depth)

            # run simulation if not at the end of the game tree
            if node.end is None:
                result = self.simulate(node)
            else:
                if node.end == 0:
                    result = 0.5
                else:
                    result = 0

            # propagate results
            for state in reversed(states):
                result = 1 - result
                stats[state][0] += 1
                stats[state][1] += result

        return stats, max_depth

    def simulate(self, board):
        engine = self.simulation_engine
        node = board
        while node.end is None:
            m = engine.choose(node)
            node = node.move(m)

        if node.end == Connect4.DRAW_ID:
            return 0.5
        elif node.end == board.whose_turn_is_it:
            return 1
        else:
            return 0

    def select_next_move(self, stats, board, C):
        """Select the next state and consider if it should be expanded"""

        bestscore = None
        bestmove = None

        children = [(m, stats[board.move(m).hashkey()[0]])
                    for m in board.moves()]
        total_n = sum(x[0] for (_, x) in children)

        for child_move, child_stat in children:
            n, w = child_stat
            if n == 0:
                return child_move, False
            else:
                score = (w / n) + C * math.sqrt(2 * math.log(total_n) / n)
                if bestscore is None or score > bestscore:
                    bestscore = score
                    bestmove = child_move

        assert bestmove is not None
        return bestmove, True

    def select_best_move(self, stats, depth, board):
        """Select the best move at the end of the Monte Carlo tree search"""

        bestscore = 0
        bestmove = None
        total_n = 0
        moves = board.moves()

        for m in moves:
            n, w = stats[board.move(m).hashkey()[0]]
            total_n += n
            print('Move %d score: %d/%d (%0.1f%%)' % (m+1, w, n, w/n*100))
            if n > bestscore or (n == bestscore and random.random() <= 0.5):
                bestmove = m
                bestscore = n
        assert bestmove is not None

        print('Maximum depth: %d, Total simulations: %d' % (depth, total_n))

        return bestmove

    def __str__(self):
        return 'MCTS(%s, %0.2f)' % (self.simulations, self.C)
