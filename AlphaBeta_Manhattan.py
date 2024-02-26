def make_best_move_minimax_alpha_beta_manhattan_distance(game):
    best_score = -float("inf")
    best_move = None
    alpha = -float("inf")
    beta = float("inf")

    for move in game.get_possible_moves(game.board, game.computer):
        new_board = game.make_move(game.board, move)
        score = minimax_alpha_beta_manhattan_distance(game, new_board, False, 0, 4, alpha, beta, set())
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, best_score)
        if beta <= alpha:
            break

    if best_move is not None:
        (start_row, start_col), (end_row, end_col) = best_move
        game.move_piece(start_row, start_col, end_row, end_col)

    return best_move


def minimax_alpha_beta_manhattan_distance(game, board, is_maximizing, current_depth, depth, alpha, beta, visited_states):
    game.minimax_calls_alpha_beta += 1

    if game.check_winner(board) is not None:
        return game.get_score(board) - current_depth
    elif current_depth == depth:
        return evaluate_manhattan_distance(game, board, game.player)

    state_key = tuple(map(tuple, board))
    if state_key in visited_states:
        return 0

    visited_states.add(state_key)

    if is_maximizing:
        best_score = -float("inf")
        for move in game.get_possible_moves(board, game.computer):
            new_board = game.make_move(board, move)
            score = minimax_alpha_beta_manhattan_distance(game, new_board, False, current_depth + 1, depth, alpha, beta, visited_states)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score

    else:
        best_score = float("inf")
        for move in game.get_possible_moves(board, game.player):
            new_board = game.make_move(board, move)
            score = minimax_alpha_beta_manhattan_distance(game, new_board, True, current_depth + 1, depth, alpha, beta, visited_states)
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break
        return best_score


def evaluate_manhattan_distance(game, board, computer):
    flagpos = ()
    menor_distancia = float("inf")
    for row in range(game.lado):
        for col in range(game.lado):
            if board[row][col] == "N":
                flagpos = (row, col)
                break

    if computer == "Cinza":
        for row in range(game.lado):
            for col in range(game.lado):
                if board[row][col] == computer:
                    distance = game.calculate_manhattan_distance(
                        row, col, flagpos[0], flagpos[1]
                    )
                    menor_distancia = min(menor_distancia, distance)

    elif computer == "Amarelo":
        for lado in range(game.lado):
            # Calcular a distância da borda superior e inferior para a bandeira
            distance_top = calculate_manhattan_distance(flagpos[0], flagpos[1], 0, lado)
            distance_bottom = calculate_manhattan_distance(flagpos[0], flagpos[1], game.lado - 1, lado)

            # Calcular a distância da borda esquerda e direita para a bandeira
            distance_left = calculate_manhattan_distance(flagpos[0], flagpos[1], lado, 0)
            distance_right = calculate_manhattan_distance(flagpos[0], flagpos[1], lado, game.lado - 1)

            # Atualizar a menor distância encontrada
            menor_distancia = min(
                menor_distancia,
                distance_top,
                distance_bottom,
                distance_left,
                distance_right,
            )

    return abs(6 - menor_distancia)


def calculate_manhattan_distance(row, col, flag_row, flag_col):
    return abs(row - flag_row) + abs(col - flag_col)
