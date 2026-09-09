def read_board():
    # Чете дъска 3x3 от входа (ама 7 реда).
    board = []
    lines = []
    for _ in range(7):
        lines.append(input().rstrip("\n"))
    for i in range(1, 7, 2):  # тук са редовете с информацията, дето ни интересува
        row = lines[i]
        cells = []
        for part in row.split('|'):
            part = part.strip()
            if part in ['X', 'O', '_']:
                cells.append(part)
        if len(cells) == 3:
            board.append(cells)
    return board


def print_board(board):
    # Отпечатва дъската.
    print("+---+---+---+")
    for r in board:
        print(f"| {r[0]} | {r[1]} | {r[2]} |")
        print("+---+---+---+")


def winner(board):
    # Гледа ой е спечелил (или None).
    lines = []
    # По редове и колони
    for i in range(3):
        lines.append(board[i])
        lines.append([board[0][i], board[1][i], board[2][i]])
    # По диагонали
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line[0] != '_' and line[0] == line[1] == line[2]:
            return line[0]
    return None


def is_full(board):
    # Проверява дали дъската е пълна.
    for r in board:
        if '_' in r:
            return False
    return True


def get_moves(board):
    # Връща ВСИЧКИ ВЪЗМОЖНИ ходове (row, col)
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == '_']


def minimax(board, player, maximizing, alpha, beta, depth):
    # Алгоритъм Minimax връща (стойност на дъската, най-добър ход).
    # depth гледа за по-бърза победа или по-бавна загуба.
    # X e max, a O e min
    w = winner(board)
    if w == 'X':
        return 10 - depth, None
    if w == 'O':
        return -10 + depth, None
    if is_full(board):
        return 0, None

    if maximizing: # X
        best_val = -999
        best_move = None
        for r, c in get_moves(board):
            board[r][c] = player
            val, _ = minimax(board, 'O', False, alpha, beta, depth+1)
            board[r][c] = '_'
            if val > best_val:
                best_val = val
                best_move = (r, c)
            alpha = max(alpha, val)
            if beta <= alpha:  # режем
                break
        return best_val, best_move

    else: # O
        best_val = 999
        best_move = None
        for r, c in get_moves(board):
            board[r][c] = player
            val, _ = minimax(board, 'X', True, alpha, beta, depth+1)
            board[r][c] = '_'
            if val < best_val:
                best_val = val
                best_move = (r, c)
            beta = min(beta, val)
            if beta <= alpha:  # режем
                break
        return best_val, best_move


def agent_move(board, player):
    # Връща най-добрия ход за нашия играч.
    if player == 'X':
        maximizing = True
    else:
        maximizing = False
    _, move = minimax(board, player, maximizing, -999, 999, 0)
    return move


def play_judge():
    # Judge gamemode :(
    turn_line = input().strip().split()
    turn = turn_line[1]
    board = read_board()

    if winner(board) or is_full(board):
        print(-1)
        return

    r, c = agent_move(board, turn)
    print(r+1, c+1)


def play_game():
    # Интерактивния gamemode :)
    first = input().strip().split()[1]
    human = input().strip().split()[1]
    board = read_board()

    turn = first
    if human == 'O':
        agent = 'X'
    else:
        agent = 'O'

    print_board(board)

    while True:
        w = winner(board)
        if w:
            print(f"WINNER: {w}")
            return
        if is_full(board):
            print("DRAW")
            return

        if turn == human:  # human move
            r, c = map(int, input().split())
            r -= 1
            c -= 1
            if 0 <= r < 3 and 0 <= c < 3 and board[r][c] == '_':
                board[r][c] = human
            else:
                print("INVALID MOVE")
                continue
            print_board(board)
            turn = agent
        else:  # agent move
            r, c = agent_move(board, agent)
            board[r][c] = agent
            print_board(board)
            turn = human


if __name__ == "__main__":
    mode = input().strip()
    if mode == "JUDGE":
        play_judge()
    else:
        play_game()