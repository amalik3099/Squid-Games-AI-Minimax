import numpy as np
# import random

from MoveHeuristics import improved_score_heuristic as evaluate


def move_minimax_decision(playerAI, grid):
    grid.over = False
    depth = 0
    depth_limit = 2
    move, _ = move_maximize(grid, playerAI, depth, depth_limit)
    # if move is None:
        # find all available moves
        # available_moves = grid.get_neighbors(playerAI.pos, only_available = True)
        # make random move
        # move = random.choice(available_moves) if available_moves else None
    return move


def move_maximize(grid, playerAI, depth, depth_limit):

    depth += 1
    pos = grid.find(playerAI.player_num)
    available_moves = grid.get_neighbors(pos, only_available=True)
    if len(available_moves) == 0 or depth > depth_limit:
        return pos, evaluate(playerAI, grid)

    max_move, max_utility = None, -np.inf
    for available_move in available_moves:
        grid_copy = grid.clone()
        grid_copy.move(available_move, playerAI.player_num)
        utility = move_minimize(grid_copy, playerAI, depth, depth_limit)

        if utility > max_utility:
            max_move, max_utility = available_move, utility

    return max_move, max_utility


def move_minimize(grid, playerAI, depth, depth_limit):

    pos = grid.find(playerAI.player_num)
    available_neighbors = grid.get_neighbors(pos, only_available=True)
    if len(available_neighbors) == 0:
        return evaluate(grid)

    min_utility = np.inf
    for available_neighbor in available_neighbors:
        grid_copy = grid.clone()
        grid_copy.trap(available_neighbor)
        _, utility = move_maximize(grid_copy, playerAI, depth, depth_limit)

        if utility < min_utility:
            min_utility = utility

    return min_utility
