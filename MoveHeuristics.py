def improved_score(playerAI, grid):
    available_moves = grid.get_neighbors(playerAI.pos, only_available=True)
    opponent_position = grid.find(3 - playerAI.player_num)
    num_moves_opp = len(grid.get_neighbors(opponent_position, only_available=True))
    num_moves = [len(grid.get_neighbors(move, only_available=True)) - num_moves_opp for move in available_moves]
    max_idx = num_moves.index(max(num_moves))
    new_position = available_moves[max_idx]
    return new_position


def improved_score_heuristic(playerAI, grid):
    num_moves = len(grid.get_neighbors(playerAI.pos, only_available=True))
    opponent_position = grid.find(3 - playerAI.player_num)
    num_moves_opp = len(grid.get_neighbors(opponent_position, only_available=True))
    return num_moves - num_moves_opp


def AIS(playerAI, grid):
    num_moves = len(grid.get_neighbors(playerAI.pos, only_available=True))
    opponent_position = grid.find(3 - playerAI.player_num)
    num_moves_opp = len(grid.get_neighbors(opponent_position, only_available=True))
    return num_moves - 2 * num_moves_opp


def OCLS(playerAI, grid):
    available_moves = grid.get_neighbors(playerAI.pos, only_available=True)
    num_moves = sum(len(grid.get_neighbors(move, only_available=True)) for move in available_moves)
    opponent_position = grid.find(3 - playerAI.player_num)
    available_moves_opp = grid.get_neighbors(opponent_position, only_available=True)
    num_moves_opp = sum(len(grid.get_neighbors(move, only_available=True)) for move in available_moves_opp)
    return num_moves - num_moves_opp


def combine_heuristics(playerAI, grid):
    combined_heuristic = 0.7 * AIS(playerAI, grid) + 0.3 * OCLS(playerAI, grid)
    return combined_heuristic
