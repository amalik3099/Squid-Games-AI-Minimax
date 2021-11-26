def improved_score(playerAI, grid, computerAI):
    available_moves = grid.get_neighbors(playerAI.pos, only_available=True)
    opponent_position = computerAI.getPosition()
    num_moves_opp = len(grid.get_neighbors(opponent_position, only_available = True))
    num_moves = [len(grid.get_neighbors(move, only_available = True)) - num_moves_opp for move in available_moves]
    max_idx = num_moves.index(max(num_moves))
    new_pos = available_moves[max_idx]
    return new_pos
