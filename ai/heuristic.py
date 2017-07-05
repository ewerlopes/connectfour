from utils import *
from random import randint


def compute_utility(state):
    x = 0
    if state.utility != 0:
        return state.utility * infinity
    for move in state.moves:
        x -= (calculateValue(state.board, move, state.to_move, (0, 1)) +
              calculateValue(state.board, move, state.to_move, (1, 0)) +
              calculateValue(state.board, move, state.to_move, (1, -1)) +
              calculateValue(state.board, move, state.to_move, (1, 1)))
        player = if_(state.to_move == 'X', 'O', 'X')
        x += (calculateValue(state.board, move, player, (0, 1)) +
              calculateValue(state.board, move, player, (1, 0)) +
              calculateValue(state.board, move, player, (1, -1)) +
              calculateValue(state.board, move, player, (1, 1)))
    return x


def calculateValue(board, move, player, (delta_x, delta_y)):
    x, y = move
    distancia = 1
    h = 0
    print "x,y", x, y
    while x <= 7 and y <= 6:
        if board.get((x, y)) == player:
            h += 50 / distancia
        elif board.get((x, y)) is None:
            if board.get((x, y + 1)) is not None and board.get((x, y + 1)) != player:
                if board.get((x, y - 1)) is not None and board.get((x, y - 1)) != player:
                    h += 50000000
            h += 10
        else:
            h += 25 / distancia
        distancia += 5
        x, y = x + delta_x, y + delta_y
    return h


#############################################################################

def random_heuristic(state):
    if state.utility != 0:
        return state.utility * infinity
    return randint(-200, 200)


#############################################################################
def calculate_max_in_row_heuristic(state):
    x = 0
    if state.utility != 0:
        return state.utility * infinity
    for move in state.moves:
        x -= (max_in_row_heuristic(state.board, move, state.to_move, (0, 1), 2999) +
              max_in_row_heuristic(state.board, move, state.to_move, (1, 0), 2999) +
              max_in_row_heuristic(state.board, move, state.to_move, (1, -1), 2999) +
              max_in_row_heuristic(state.board, move, state.to_move, (1, 1), 2999))
        player = if_(state.to_move == 'X', 'O', 'X')
        x += (max_in_row_heuristic(state.board, move, player, (0, 1), 3000) +
              max_in_row_heuristic(state.board, move, player, (1, 0), 3000) +
              max_in_row_heuristic(state.board, move, player, (1, -1), 3000) +
              max_in_row_heuristic(state.board, move, player, (1, 1), 3000))
    print x
    return x


def max_in_row_heuristic(board, move, player, (delta_x, delta_y), best_value):
    h = 0
    max = 0
    x, y = move
    # print move
    distance = 1
    print board
    print x, y
    while x <= 7 and y <= 6:
        if board.get((x, y)) == player:
            max += 1
            if max >= 4:
                max = 0
                h += best_value / distance
            h += 50 / distance
        elif board.get((x, y)) is None:
            if max >= 4:
                max = 0
                h += best_value / distance
            if board.get((x, y + 1)) is not None and board.get((x, y + 1)) != player:
                if board.get((x, y - 1)) is not None and board.get((x, y - 1)) != player:
                    h += 5000000000
            h += 10
        else:
            max = 0
            h += 25 / distance
        x, y = x + delta_x, y + delta_y
        distance += 1

    return h


##############################################################################

def best_move_heuristic(state):
    if state.utility != 0:
        return state.utility * infinity
    ally = 0
    h = 0
    enemy = 0
    for move in state.moves:
        ally += calculate_best(state.board, move, state.to_move, (0,1))
        ally += calculate_best(state.board, move, state.to_move, (1,0))
        ally += calculate_best(state.board, move, state.to_move, (1,-1))
        ally += calculate_best(state.board, move, state.to_move, (1,1))
        ally += calculate_best(state.board, move, state.to_move, (-1,0))

        player = if_(state.to_move == 'X', 'O', 'X')

        enemy += calculate_best(state.board, move, player, (0,1))
        enemy += calculate_best(state.board, move, player, (1,0))
        enemy += calculate_best(state.board, move, player, (1,-1))
        enemy += calculate_best(state.board, move, player, (1,1))
        enemy += calculate_best(state.board, move, player, (-1,0))
        if ally >= enemy:
            if ally > 3:
                h+= 50000
            else:
                h+= 400
        else:
            h+= -350
    return h


def calculate_best(board, move, player, (delta_x, delta_y)):
    h = 0
    x, y = move
    while 0 < x < 8 and 0 < y < 7:
        if board.get((x, y)) == player or board.get((x, y)) is None:
            h += 1
            if h == 4:
                return 1
        else:
            return 0
        x += delta_x
        y += delta_y
    return 0

def legal_moves(state):
    "Legal moves are any square not yet taken."
    return [(x, y) for (x, y) in state.moves
            if y == 1 or (x, y-1) in state.board]

###############################################################################
def best_move_heuristic2(state):
    if state.utility != 0:
        # return if_(state.to_move == 'X',state.utility * infinity, state.utility*(-infinity))
        return state.utility * infinity
    ally = 0
    enemy = 0
    moves = legal_moves(state)
    for move in moves:
        ally += calculate_best2(state.board, move, state.to_move, (0,1))
        ally += calculate_best2(state.board, move, state.to_move, (1,0))
        ally += calculate_best2(state.board, move, state.to_move, (1,-1))
        ally += calculate_best2(state.board, move, state.to_move, (1,1))
        ally += calculate_best2(state.board, move, state.to_move, (-1,0))
        ally += calculate_best2(state.board, move, state.to_move, (0,-1))
        ally += calculate_best2(state.board, move, state.to_move, (-1,1))
        ally += calculate_best2(state.board, move, state.to_move, (-1,-1))

        player = if_(state.to_move == 'X', 'O', 'X')

        enemy += calculate_best2(state.board, move, player, (0,1))
        enemy += calculate_best2(state.board, move, player, (1,0))
        enemy += calculate_best2(state.board, move, player, (1,-1))
        enemy += calculate_best2(state.board, move, player, (1,1))
        enemy += calculate_best2(state.board, move, player, (-1,0))
        enemy += calculate_best2(state.board, move, player, (0,-1))
        enemy += calculate_best2(state.board, move, player, (-1,1))
        enemy += calculate_best2(state.board, move, player, (-1,-1))
    return ally - enemy

def calculate_best2(board, move, player, (delta_x, delta_y)):
    h = 0
    k = 0
    f = 1
    x, y = move
    while 0 < x < 8 and 0 < y < 7:
        if board.get((x, y)) == player:
            h += 70
            k += 1
            f+=1
            if k == 4:
                h *= f
                return h
        elif board.get((x, y)) is None:
            h += 20
            k += 1
            if k == 4:
                h *= f
                return h
        else:
            return 0

        x += delta_x
        y += delta_y
    return h