import numpy as np
# import random

from MoveHeuristics import improved_score_heuristic as evaluate
from MoveHeuristics import combine_heuristics


def move_minimax_decision(AI, grid):
    depth = 0
    depth_limit = 2
    move, _ = move_maximize(grid, AI, depth, depth_limit)
    # if move is None:
        # find all available moves
        # available_moves = grid.get_neighbors(playerAI.pos, only_available = True)
        # make random move
        # move = random.choice(available_moves) if available_moves else None
    return move


def move_maximize(grid, AI, depth, depth_limit):

    depth += 1
    pos = grid.find(AI.player_num)
    available_moves = grid.get_neighbors(pos, only_available=True)
    if len(available_moves) == 0 or depth > depth_limit:
        return pos, evaluate(AI, grid)

    max_move, max_utility = None, -np.inf
    for available_move in available_moves:
        grid_copy = grid.clone()
        grid_copy.move(available_move, AI.player_num)
        utility = move_minimize(grid_copy, AI, depth, depth_limit)

        if utility > max_utility:
            max_move, max_utility = available_move, utility

    return max_move, max_utility


def move_minimize(grid, AI, depth, depth_limit):

    pos = grid.find(AI.player_num)
    available_neighbors = grid.get_neighbors(pos, only_available=True)
    if len(available_neighbors) == 0:
        return evaluate(AI, grid)

    min_utility = np.inf
    for available_neighbor in available_neighbors:
        grid_copy = grid.clone()
        grid_copy.trap(available_neighbor)
        _, utility = move_maximize(grid_copy, AI, depth, depth_limit)

        if utility < min_utility:
            min_utility = utility

    return min_utility


def move_minimax_decision_with_a_b(AI, grid):
    depth = 0
    depth_limit = 3
    move, _ = move_maximize_with_a_b(grid, AI, depth, depth_limit, -np.inf, np.inf)
    return move


def move_maximize_with_a_b(grid, AI, depth, depth_limit, alpha, beta):

    depth += 1
    pos = grid.find(AI.player_num)
    available_moves = grid.get_neighbors(pos, only_available=True)
    if len(available_moves) == 0 or depth > depth_limit:
        return pos, combine_heuristics(AI, grid)

    max_move, max_utility = None, -np.inf
    for available_move in available_moves:
        grid_copy = grid.clone()
        grid_copy.move(available_move, AI.player_num)
        utility = move_minimize_with_a_b(grid_copy, AI, depth, depth_limit, alpha, beta)

        if utility > max_utility:
            max_move, max_utility = available_move, utility

        if max_utility >= beta:
            break

        if max_utility > alpha:
            alpha = max_utility

    return max_move, max_utility


def move_minimize_with_a_b(grid, AI, depth, depth_limit, alpha, beta):

    pos = grid.find(AI.player_num)
    available_neighbors = grid.get_neighbors(pos, only_available=True)
    if len(available_neighbors) == 0:
        return combine_heuristics(AI, grid)

    min_utility = np.inf
    for available_neighbor in available_neighbors:
        grid_copy = grid.clone()
        grid_copy.trap(available_neighbor)
        _, utility = move_maximize_with_a_b(grid_copy, AI, depth, depth_limit, alpha, beta)

        if utility < min_utility:
            min_utility = utility

        if min_utility <= alpha:
            break

        if min_utility < beta:
            beta = min_utility

    return min_utility
