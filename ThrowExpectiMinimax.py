import numpy as np
import random

from MoveHeuristics import improved_score_heuristic as evaluate
from MoveHeuristics import combine_heuristics


def throw_minimax_decision(AI, grid):
    depth = 0
    depth_limit = 2
    trap, _ = throw_maximize(grid, AI, depth, depth_limit)
    # if move is None:
        # find all available moves
        # available_moves = grid.get_neighbors(playerAI.pos, only_available = True)
        # make random move
        # move = random.choice(available_moves) if available_moves else None
    return trap


def throw_maximize(grid, AI, depth, depth_limit):

    depth += 1
    opponent = grid.find(3 - AI.player_num)
    available_cells = grid.get_neighbors(opponent, only_available=True)
    if len(available_cells) == 0 or depth > depth_limit:
        available_cells = grid.getAvailableCells()
        trap = random.choice(available_cells)
        return trap, evaluate(AI, grid)

    max_throw, max_utility = None, -np.inf
    for available_cell in available_cells:
        grid_copy = grid.clone()
        grid_copy.trap(available_cell)
        utility = throw_minimize(grid_copy, AI, depth, depth_limit)

        if utility > max_utility:
            max_throw, max_utility = available_cell, utility

    return max_throw, max_utility


def throw_minimize(grid, AI, depth, depth_limit):

    opponent_num = 3 - AI.player_num
    opponent = grid.find(opponent_num)
    available_cells = grid.get_neighbors(opponent, only_available=True)
    if len(available_cells) == 0:
        return evaluate(AI, grid)

    min_utility = np.inf
    for available_cell in available_cells:
        grid_copy = grid.clone()
        grid_copy.move(available_cell, opponent_num)
        _, utility = throw_maximize(grid_copy, AI, depth, depth_limit)

        if utility < min_utility:
            min_utility = utility

    return min_utility


def throw_minimax_decision_with_a_b(AI, grid):
    depth = 0
    depth_limit = 3
    trap, _ = throw_maximize_with_a_b(grid, AI, depth, depth_limit, -np.inf, np.inf)
    return trap


def throw_maximize_with_a_b(grid, AI, depth, depth_limit, alpha, beta):

    depth += 1
    opponent = grid.find(3 - AI.player_num)
    available_cells = grid.get_neighbors(opponent, only_available=True)
    if len(available_cells) == 0 or depth > depth_limit:
        available_cells = grid.getAvailableCells()
        trap = random.choice(available_cells)
        return trap, combine_heuristics(AI, grid)

    max_throw, max_utility = None, -np.inf
    for available_cell in available_cells:
        grid_copy = grid.clone()
        grid_copy.trap(available_cell)
        utility = throw_minimize_with_a_b(grid_copy, AI, depth, depth_limit, alpha, beta)

        if utility > max_utility:
            max_throw, max_utility = available_cell, utility

        if max_utility >= beta:
            break

        if max_utility > alpha:
            alpha = max_utility

    return max_throw, max_utility


def throw_minimize_with_a_b(grid, AI, depth, depth_limit, alpha, beta):

    opponent_num = 3 - AI.player_num
    opponent = grid.find(opponent_num)
    available_cells = grid.get_neighbors(opponent, only_available=True)
    if len(available_cells) == 0:
        return combine_heuristics(AI, grid)

    min_utility = np.inf
    for available_cell in available_cells:
        grid_copy = grid.clone()
        grid_copy.move(available_cell, opponent_num)
        _, utility = throw_maximize_with_a_b(grid_copy, AI, depth, depth_limit, alpha, beta)

        if utility < min_utility:
            min_utility = utility

        if min_utility <= alpha:
            break

        if min_utility < beta:
            beta = min_utility

    return min_utility
