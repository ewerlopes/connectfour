from abc import ABCMeta, abstractmethod

import pygame
import numpy as np
import itertools
import settings
import utils

"""
This class has classes for the game objects: Chips and Players.
"""

class RedChip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = utils.load_image('red_chip.png')
        self.rect = self.image.get_rect()


class YellowChip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = utils.load_image('yellow_chip.png')
        self.rect = self.image.get_rect()


class Player:
    __metaclass__ = ABCMeta

    def __init__(self, chip, color, name, id, score):
        self.chip = chip
        self.color = color
        self.name = name
        self.id = id
        self.score = score

    @abstractmethod
    def move(self, state, game_problem):
        """
        Defines the action to take. Return None in case the player is a human (allows for receive input).
        :return:
        """
        pass


class RedPlayer(Player):
    def __init__(self):
        Player.__init__(self, RedChip, settings.COLORS.RED.value, 'Red', 'RED', 0)

    def move(self, state, game_problem):
        pass

class YellowPlayer(Player):
    def __init__(self):
        Player.__init__(self, YellowChip, settings.COLORS.YELLOW.value, 'Yellow', 'YELLOW', 0)

    def move(self, state, game_problem):
        pass

################################################################################
# SEGMENT TABLES                                                               #
#                                                                              #
# Segments are quartets of indices that represent four squares aligned and     #
# consecutive in the board.                                                    #
# If a segment contains piece of the same player, that player won the game.    #
# all_segments is a 2d array, each row is a segment                            #
# rev_segments is an index square -> group of segments that pass by the square #
################################################################################

all_segments = []
rev_segments = [[] for x in range(7*6)]

_indices = np.arange(7*6).reshape((7, 6))


def add_rev(line):
    for x in range(len(line)-3):
        seg = line[x:x+4]
        all_segments.append(seg)
        for n in seg:
            rev_segments[n].append(seg)

for col in _indices:
    add_rev(col)

for row in _indices.transpose():
    add_rev(row)

for idx in (_indices, _indices[:, ::-1]):
    for di in range(-7, 7):
        diag = idx.diagonal(di)
        add_rev(diag)


all_segments = np.asarray(all_segments)
rev_segments = np.asarray([np.asarray(x) for x in rev_segments])


##########################
# evaldiff lookup tables #
##########################

# keep the scores of segment combos
evaldiff_lookup = {
    1: np.zeros(3**4, dtype=int),
    2: np.zeros(3**4, dtype=int),
}

# used to check if the opponent would win if we don't fill the empty square
evaldiff_threat_lookup = {
    1: np.zeros(3**4, dtype=int),
    2: np.zeros(3**4, dtype=int),
}

for comb in itertools.product(range(3), range(3), range(3), range(3)):
    c = [0, 0, 0]
    score1 = 0
    score2 = 0

    for x in comb:
        c[x] += 1

    if c[0] == 4:
        score1 = 1
        score2 = 1
    elif c[0] + c[1] == 4:
        score1 = (c[1] + 1) ** 2
        score2 = c[1] ** 2
    elif c[0] + c[2] == 4:
        score2 = (c[2] + 1) ** 2
        score1 = c[2] ** 2

    key = np.dot(np.array(comb, dtype=int),
                 np.array([3**0, 3**1, 3**2, 3**3], dtype=int))
    evaldiff_lookup[1][key] = score1
    evaldiff_lookup[2][key] = score2
    if score2 == 4 ** 2:
        evaldiff_threat_lookup[1][key] = 1
    elif score1 == 4 ** 2:
        evaldiff_threat_lookup[2][key] = 1


#########
# BOARD #
#########

PLAYER1 = 1
PLAYER2 = 2
DRAW = 0
COMPUTE = -1


class WrongMoveError(Exception):
    pass


class Board(object):
    def __init__(self, pos=None, next_to_move=PLAYER1, end=COMPUTE, cols=7, rows=6):
        if pos is None:
            pos = np.zeros((cols, rows), dtype=int)
        self._pos = pos
        self._next_to_move = next_to_move
        if end == COMPUTE:
            self._end = self._check_end(pos)
        else:
            self._end = end

    @property
    def end(self):
        return self._end

    @property
    def get_next_to_move(self):
        return self._next_to_move

    @property
    def other(self):
        return PLAYER1 if self._next_to_move != PLAYER1 else PLAYER2

    @classmethod
    def _check_end(cls, pos):
        for seg in cls.segments(pos):
            c = np.bincount(seg)
            if c[0]:
                continue
            if c[PLAYER1] == 4:
                return PLAYER1
            elif c[PLAYER2] == 4:
                return PLAYER2

        if pos.all():
            return DRAW
        else:
            return None

    @classmethod
    def _check_end_around(cls, pos, r, c, side):
        if (cls.segments_around(pos, r, c) == side).all(1).any():
            return side

        if pos.all():
            return DRAW
        else:
            return None

    @classmethod
    def segments(cls, pos):
        if isinstance(pos, Board):
            return cls.segments(pos._pos)
        else:
            pos = pos.flatten()
            return pos[all_segments]

    @classmethod
    def segments_around(cls, pos, r, c):
        if isinstance(pos, Board):
            return cls.segments_around(pos._pos, r, c)
        else:
            idx = c * pos.shape[1] + r
            pos = pos.flatten()
            return pos[rev_segments[idx]]

    def __str__(self):
        disc = {
            0: ' ',
            1: 'X',
            2: 'O'
            }

        s = []
        for row in reversed(self._pos.transpose()):
            s.append(' | '.join(disc[x] for x in row))
        s.append(' | '.join('-'*7))
        s.append(' | '.join(map(str, range(1, 8))))
        s = ['| ' + x + ' |' for x in s]
        s = [i + ' ' + x for i, x in zip('ABCDEFG  ', s)]
        s = '\n'.join(s)

        if self._end is DRAW:
            s += '\n<<< Game over: draw' % [self._end]
        elif self._end is not None:
            s += '\n<<< Game over: %s win' % disc[self._end]
        else:
            s += '\n<<< Move to %s' % disc[self._next_to_move]
        return s

    def move(self, m):
        if not (0 <= m < 7):
            raise ValueError(m)

        pos = self._pos.copy()

        r = pos[m].argmin()
        if pos[m][r] != 0:
            raise WrongMoveError('Full Column')
        pos[m][r] = self._next_to_move
        end = self._check_end_around(pos, r, m, self._next_to_move)
        stm = self.other
        return Board(pos, stm, end)

    def freerow(self, m):
        r = self._pos[m].argmin()
        if self._pos[m][r] != 0:
            return None
        return r

    def moves(self):
        return np.flatnonzero(self._pos[:, -1] == 0)

    def hashkey(self):
        """Generates an hashkey

        Returns a tuple (key, flip)
        flip is True if it returned the key of the symmetric Board.

        """
        k1 = 0
        k2 = 0

        for x in self._pos.flat:
            k1 *= 3
            k1 += int(x)
            assert k1 >= 0

        for x in self._pos[::-1].flat:
            k2 *= 3
            k2 += int(x)
            assert k2 >= 0

        if k2 < k1:
            return k2, True
        else:
            return k1, False
