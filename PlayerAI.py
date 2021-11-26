import random
from BaseAI import BaseAI
import numpy as np
from Grid import Grid
from MoveHeuristics import improved_score

# TO BE IMPLEMENTED


class PlayerAI(BaseAI):

    def __init__(self, initial_position=None) -> None:
        # You may choose to add attributes to your player - up to you!
        super().__init__()
        self.pos = initial_position

    def setPosition(self, new_pos: tuple):
        self.pos = new_pos

    def getPosition(self):
        return self.pos

    def getMove(self, grid: Grid, computerAI: BaseAI) -> tuple:
        """
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player moves.

        You may adjust the input variables as you wish but output has to be the coordinates.

        """
        # find all available moves
        # available_moves = grid.get_neighbors(self.pos, only_available=True)

        # make random move
        # new_pos = random.choice(available_moves) if available_moves else None

        new_pos = improved_score(self, grid, computerAI)
        self.setPosition(new_pos)

        return new_pos


    def getTrap(self, grid: Grid) -> tuple:
        """
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player *wants*
        to throw the trap.

        You do not need to account for probabilities. We've implemented that for you.

        You may adjust the input variables as you wish but output has to be the coordinates.

        """
        # find all available cells in the grid
        available_cells = grid.getAvailableCells()

        # find all available cells
        trap = random.choice(available_cells) if available_cells else None

        return trap
