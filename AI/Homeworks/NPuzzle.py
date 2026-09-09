import time

class SearchNode:
    # Класа представлява едно състояние на дъската в дървото на търсене.

    def __init__(self, board, goal_positions, size, move=None, previous=None):
        self.board = board  # Текущото състояние на дъската
        self.size = size
        self.move = move  # Ходът, който доведе до това състояние (left, right, up, down)
        self.previous = previous  # Препратка към предишния възел в пътя
        self.goal_positions = goal_positions  # Речник с целевите позиции на плочките
    
    def manhattan(self):
        # За всяка плочка изчисляваме разстоянието до нейната целева позиция
        distance = 0
        for i in range(len(self.board)):
            if self.board[i] != 0:
                goal_row, goal_col = self.goal_positions[self.board[i]]
                curr_row, curr_col = i // self.size, i % self.size
                distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
        return distance
    
    def get_neighbors(self):
        # Генерира списък всички валидни съседни състояния.
        zero_pos = self.board.index(0)  # Намираме позицията на празната плочка
        row, col = zero_pos // self.size, zero_pos % self.size
        neighbors = []
        
        # Празната плочка се мести наляво
        if col > 0:
            new_board = self.board[:]
            swap_pos = zero_pos - 1
            new_board[zero_pos], new_board[swap_pos] = new_board[swap_pos], new_board[zero_pos]
            neighbors.append((new_board, 'right'))
        
        # Празната плочка се мести надясно
        if col < self.size - 1:
            new_board = self.board[:]
            swap_pos = zero_pos + 1
            new_board[zero_pos], new_board[swap_pos] = new_board[swap_pos], new_board[zero_pos]
            neighbors.append((new_board, 'left'))
        
        # Празната плочка се мести нагоре
        if row > 0:
            new_board = self.board[:]
            swap_pos = zero_pos - self.size
            new_board[zero_pos], new_board[swap_pos] = new_board[swap_pos], new_board[zero_pos]
            neighbors.append((new_board, 'down'))
        
        # Празната плочка се мести надолу
        if row < self.size - 1:
            new_board = self.board[:]
            swap_pos = zero_pos + self.size
            new_board[zero_pos], new_board[swap_pos] = new_board[swap_pos], new_board[zero_pos]
            neighbors.append((new_board, 'up'))
        
        return neighbors
    
    def get_path(self):
        # Връща списък с ходовете от началното състояние до текущото.
        path = []
        node = self

        while node.previous is not None:
            path.append(node.move)
            node = node.previous
        path.reverse()
        return path


def read_input():
    # Четене на стандартния вход.
    n = int(input())
    target_zero_idx = int(input())
    size = int((n + 1) ** 0.5)
    board = []
    
    for i in range(size):
        row = list(map(int, input().split()))
        board.extend(row)
    
    return n, target_zero_idx, board, size

def get_goal_state(n, target_zero_idx):
    # Създава целевото състояние (като имаме напредвид позицията на 0).
    if target_zero_idx == -1:
        goal = list(range(1, n + 1)) + [0]
    else:
        # Създаваме целево състояние с нулата на зададена позиция
        goal = [0] * (n + 1)
        goal[target_zero_idx] = 0
        num = 1
        for i in range(n + 1):
            if i != target_zero_idx:
                goal[i] = num
                num += 1
    
    return goal

def goalpositions(goal, size):
    # Hashmap за позициите на всяка плочка в целевото състояние като тип (ред, колона).
    # Защо?? Еми изчисляваме manhattan по бързо

    positions = {}
    for i in range(len(goal)):
        if goal[i] != 0:
            positions[goal[i]] = (i // size, i % size)
    return positions

def inversions(board):
    # Брои инверсиите (т.е. имаме по-голямо число преди по-малко)
    inversions = 0
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            if board[i] > board[j] and board[i] != 0 and board[j] != 0:
                inversions += 1
    return inversions

def solvable(board, goal, size):
    # Проверяваме дали пъзелът е решим.

    board_inv = inversions(board)
    goal_inv = 0
    
    zero_pos_board = board.index(0)
    zero_pos_goal = goal.index(0)
    
    board_row = zero_pos_board // size
    goal_row = zero_pos_goal // size
    
    if size % 2 == 1:
        # Нечетен размер - проверяваме само четността на инверсиите
        return board_inv % 2 == goal_inv % 2
    else:
        # Четен размер - проверяваме четността на (инверсии + ред)
        board_parity = (board_inv + board_row) % 2
        goal_parity = (goal_inv + goal_row) % 2
        return board_parity == goal_parity

def search(node, g, threshold, goal, goal_positions, size):
    # DLS-то на IDA* алгоритъма.
    f = g + node.manhattan()

    # Ако надхвъря threshold, връщаме f за следваща итерация
    if f > threshold:
        return f, None

    # Това решението ли е? Ако да - връщаме го
    if node.board == goal:
        return -1, node

    min_threshold = float('inf')

    # Обикаляме съседите
    for neighbor_board, direction in node.get_neighbors():
        # ОПТИМИЗАЦИЯ: не се връщаме към предишното състояние
        if node.previous is not None and neighbor_board == node.previous.board:
            continue

        neighbor_node = SearchNode(neighbor_board, goal_positions, size, direction, node)
        result, solution = search(neighbor_node, g + 1, threshold, goal, goal_positions, size)

        # Има решение
        if result == -1:
            return -1, solution

        # Запомняме threshold за следващата итерация
        if result < min_threshold:
            min_threshold = result

    return min_threshold, None


def ida(start_board, goal, goal_positions, size):
    # Алгоритъм IDA*
    # Начален state
    start_node = SearchNode(start_board, goal_positions, size)
    threshold = start_node.manhattan()

    while True:
        result, solution = search(start_node, 0, threshold, goal, goal_positions, size)

        # Има решение
        if result == -1:
            return solution.get_path()

        # Няма решение (не би трябвало да се случи)
        if result == float('inf'):
            return None

        # Увеличаваме threshold
        threshold = result


def main():
    n, target_zero_idx, board, size = read_input()
    goal = get_goal_state(n, target_zero_idx)
    start_time = time.time()
    
    # Проверка за решимост
    if not solvable(board, goal, size):
        print(-1)
        return
    
    # Проверка дали е вече решен
    if board == goal:
        print(0)
        return
    
    # Предварително изчисляваме целевите позиции за оптимизация
    goal_positions = goalpositions(goal, size)
    
    # IDA* търсенето
    solution = ida(board, goal, goal_positions, size)
    end_time = time.time()
    
    # Извеждаме резултата
    elapsed_ms = (end_time - start_time) * 1000
    print(f"# TIMES_MS: alg={elapsed_ms:.3f}")
    
    if solution is None:
        print(-1)
    else:
        print(len(solution))
        for move in solution:
            print(move)

if __name__ == "__main__":
    main()