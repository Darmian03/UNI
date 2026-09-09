import time

def is_goal(board, n):
    # Проверка дали текущото състояние е крайната цел.
    # лявата половина '<', дясната '>', а средата '_'
    return board == ['<'] * n + ['_'] + ['>'] * n

def generate_moves(board, zero_pos):
    # Генерира всички възможни следващи ходове (нови състояния).
    moves = []
    n = len(board)
    
    if zero_pos > 1 and board[zero_pos - 2] == '>' and board[zero_pos - 1] != '>' and board[zero_pos - 1] != '_':
        # '>' прескача надясно
        new_board = board[:]
        new_board[zero_pos], new_board[zero_pos - 2] = new_board[zero_pos - 2], new_board[zero_pos]
        moves.append((new_board, zero_pos - 2))
    if zero_pos < n - 2 and board[zero_pos + 2] == '<' and board[zero_pos + 1] != '<' and board[zero_pos + 1] != '_':
        # '<' прескача наляво
        new_board = board[:]
        new_board[zero_pos], new_board[zero_pos + 2] = new_board[zero_pos + 2], new_board[zero_pos]
        moves.append((new_board, zero_pos + 2))

    if zero_pos > 0 and board[zero_pos - 1] == '>':
        # местим '>' надясно (една позиция)
        new_board = board[:]
        new_board[zero_pos], new_board[zero_pos - 1] = new_board[zero_pos - 1], new_board[zero_pos]
        moves.append((new_board, zero_pos - 1))
    if zero_pos < n - 1 and board[zero_pos + 1] == '<':
        # местим '<' наляво (една позиция)
        new_board = board[:]
        new_board[zero_pos], new_board[zero_pos + 1] = new_board[zero_pos + 1], new_board[zero_pos]
        moves.append((new_board, zero_pos + 1))

    return moves

def dfs(board, zero_pos, n, output):
    # Рекурсивна реализация на DFS.
    if is_goal(board, n):
        output.append(board[:])
        return True

    for new_board, new_zero_pos in generate_moves(board, zero_pos):
        if dfs(new_board, new_zero_pos, n, output):
            output.append(board[:])
            return True
    return False

def main():
    n = int(input().strip())

    # начално състояние: N жаби гледат надясно, среда '_', N жаби гледат наляво
    board = ['>'] * n + ['_'] + ['<'] * n
    zero_pos = n  # индекс на празното поле
    start_time = time.time()

    output = []
    dfs(board, zero_pos, n, output)
    end_time = time.time()

    # Използваме reversed(), за да обърнем реда на отпечатване
    elapsed_ms = (end_time - start_time) * 1000
    print(f"# TIMES_MS: alg={elapsed_ms:.3f}")
    
    for state in reversed(output):
        print(''.join(state))

if __name__ == "__main__":
    main()