import numpy as np
import random
import time
import sys
import os
from BaseAI import BaseAI
from Grid import Grid
from MoveExpectiMinimax import move_minimax_decision

# TO BE IMPLEMENTED
#
class FixedAI(BaseAI):

    def __init__(self) -> None:
        # You may choose to add attributes to your player - up to you!
        super().__init__()
        self.pos = None
        self.player_num = None

    def getPosition(self):
        return self.pos

    def setPosition(self, new_position):
        self.pos = new_position

    def getPlayerNum(self):
        return self.player_num

    def setPlayerNum(self, num):
        self.player_num = num

    def getMove(self, grid: Grid) -> tuple:
        """
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player moves.

        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Trap* actions,
        taking into account the probabilities of them landing in the positions you believe they'd throw to.

        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.

        """
        # new_position = improved_score(self, grid)
        new_position = move_minimax_decision(self, grid)
        return new_position

    def getTrap(self, grid: Grid) -> tuple:
        """
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player *WANTS* to throw the trap.

        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Move* actions,
        taking into account the probabilities of it landing in the positions you want.

        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.

        """

        """EasyAI throws randomly to the immediate neighbors of the opponent"""

        # find opponent
        opponent = grid.find(3 - self.player_num)

        # find all available cells in the grid
        available_cells = grid.get_neighbors(opponent, only_available=True)

        if len(available_cells) == 0:
            available_cells = grid.getAvailableCells()

        # throw to one of the available cells randomly
        trap = random.choice(available_cells)

        return trap
