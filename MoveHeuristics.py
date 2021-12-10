import itertools

def improved_score(AI, grid):
    available_moves = grid.get_neighbors(AI.pos, only_available=True)
    opponent_position = grid.find(3 - AI.player_num)
    num_moves_opp = len(grid.get_neighbors(opponent_position, only_available=True))
    num_moves = [len(grid.get_neighbors(move, only_available=True)) - num_moves_opp for move in available_moves]
    max_idx = num_moves.index(max(num_moves))
    new_position = available_moves[max_idx]
    return new_position


def prune_throw_options(AI, grid, available_cells, cutoff, reverse):
    scores = []
    for available_cell in available_cells:
        grid_copy = grid.clone()
        grid_copy.trap(available_cell)
        score = combine_heuristics(AI, grid)
        scores.append(score)
    available_cells = [available_cell for _, available_cell in sorted(zip(scores, available_cells), reverse=reverse)]
    available_cells = available_cells[:cutoff]
    return available_cells

def improved_score_heuristic(AI, grid):
    num_moves = len(grid.get_neighbors(AI.pos, only_available=True))
    opponent_position = grid.find(3 - AI.player_num)
    num_moves_opp = len(grid.get_neighbors(opponent_position, only_available=True))
    return num_moves - num_moves_opp


def AIS(AI, grid):
    num_moves = len(grid.get_neighbors(AI.pos, only_available=True))
    opponent_position = grid.find(3 - AI.player_num)
    num_moves_opp = len(grid.get_neighbors(opponent_position, only_available=True))
    return num_moves - 2 * num_moves_opp


def OCLS(AI, grid):
    available_moves = grid.get_neighbors(AI.pos, only_available=True)
    num_moves = sum(len(grid.get_neighbors(move, only_available=True)) for move in available_moves)
    opponent_position = grid.find(3 - AI.player_num)
    available_moves_opp = grid.get_neighbors(opponent_position, only_available=True)
    num_moves_opp = sum(len(grid.get_neighbors(move, only_available=True)) for move in available_moves_opp)
    return num_moves - num_moves_opp

def two_step_OCLS(AI, grid):
    available_moves = grid.get_neighbors(AI.pos, only_available=True)
    next_steps = [grid.get_neighbors(move, only_available=True) for move in available_moves]
    next_steps = list(itertools.chain(*next_steps))
    num_moves = sum(len(grid.get_neighbors(next_step, only_available=True)) for next_step in next_steps)
    opponent_position = grid.find(3 - AI.player_num)
    available_moves_opp = grid.get_neighbors(opponent_position, only_available=True)
    next_steps_opp = [grid.get_neighbors(move, only_available=True) for move in available_moves_opp]
    next_steps_opp = list(itertools.chain(*next_steps_opp))
    num_moves_opp = sum(len(grid.get_neighbors(next_step, only_available=True)) for next_step in next_steps_opp)
    return num_moves - num_moves_opp


def combine_heuristics(AI, grid):
    combined_heuristic = 0.3 * two_step_OCLS(AI, grid) + 0.3 * OCLS(AI, grid) + 0.2 * AIS(AI, grid) + 0.2 * improved_score_heuristic(AI, grid)
    opponent_position = grid.find(3 - AI.player_num)
    opponent_edges = sum([position == 0 for position in opponent_position])
    position = grid.find(AI.player_num)
    edges = sum([position == 0 for position in position])
    edges_diff = opponent_edges - edges
    combined_heuristic += edges_diff
    return combined_heuristic
