import numpy as np
import random
import time

from MoveHeuristics import improved_score_heuristic as evaluate
from MoveHeuristics import combine_heuristics, prune_throw_options

ALLOWANCE = 0.05
TIME_LIMIT = 2 - 2 * ALLOWANCE

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
    depth_limit = 5
    start_time = time.process_time()
    trap, _ = throw_maximize_with_a_b(grid, AI, depth, depth_limit, -np.inf, np.inf, start_time)
    return trap


def throw_maximize_with_a_b(grid, AI, depth, depth_limit, alpha, beta, start_time):
    
    
    depth += 1
    opponent = grid.find(3 - AI.player_num)
    available_cells = grid.get_neighbors(opponent, only_available=True)
    if len(available_cells) == 0 or depth > depth_limit:
        available_cells = grid.getAvailableCells()
        trap = random.choice(available_cells)
        return trap, combine_heuristics(AI, grid)
    
    if time.process_time() - start_time >= TIME_LIMIT:
        trap = random.choice(available_cells)
        return trap, combine_heuristics(AI, grid)
    
    cutoff = 4
    if len(available_cells) > cutoff:
        available_cells = prune_throw_options(AI, grid, available_cells, cutoff, True)

    max_throw, max_utility = None, -np.inf
    for available_cell in available_cells:
        grid_copy = grid.clone()
        grid_copy.trap(available_cell)
        utility = throw_minimize_with_a_b(grid_copy, AI, depth, depth_limit, alpha, beta, start_time)

        if utility > max_utility:
            max_throw, max_utility = available_cell, utility

        if max_utility >= beta:
            break

        if max_utility > alpha:
            alpha = max_utility

    return max_throw, max_utility


def throw_minimize_with_a_b(grid, AI, depth, depth_limit, alpha, beta, start_time):

    depth += 1
    opponent_num = 3 - AI.player_num
    opponent = grid.find(opponent_num)
    available_cells = grid.get_neighbors(opponent, only_available=True)
    if len(available_cells) == 0  or depth > depth_limit:
        return combine_heuristics(AI, grid)
    
    if time.process_time() - start_time >= TIME_LIMIT:
        return combine_heuristics(AI, grid)
        
    min_utility = np.inf
    for available_cell in available_cells:
        grid_copy = grid.clone()
        grid_copy.move(available_cell, opponent_num)
        _, utility = throw_maximize_with_a_b(grid_copy, AI, depth, depth_limit, alpha, beta, start_time)
        
        utility *= 0.85

        if utility < min_utility:
            min_utility = utility

        if min_utility <= alpha:
            break

        if min_utility < beta:
            beta = min_utility

    return min_utility
