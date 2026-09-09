import random
import time

def print_board(queen_positions):
    # Принтира дъската с цариците.
    n = len(queen_positions)
    for r in range(n):
        row = []
        for c in range(n):
            if queen_positions[c] == r:
                row.append('Q')
            else:
                row.append('_')
        print(' '.join(row))

def min_conflicts(n, max_steps=100000):
    # Min Conflict алгоритъм (ай стига бе)

    # Слагаме царици на random
    # queen_positions = np.random.randint(0, n, size=n)
    queen_positions = [random.randint(0, n - 1) for _ in range(n)]

    # Правим и попълваме масивите за цариците
    rows = [0] * n
    pos_diag = [0] * (2 * n - 1)
    neg_diag = [0] * (2 * n - 1)

    for col, row in enumerate(queen_positions):
        rows[row] += 1
        pos_diag[row + col] += 1
        neg_diag[n - 1 + row - col] += 1

    for step in range(max_steps):
        # Намираме конфликтните царици
        conflicted = [
            col for col, row in enumerate(queen_positions)
            if rows[row] > 1
            or pos_diag[row + col] > 1
            or neg_diag[n - 1 + row - col] > 1
        ]

        # Ако няма конфликтни царици -> имаме решение
        if not conflicted:
            return queen_positions

        # Избираме случайна царица в конфликт
        col = random.choice(conflicted)
        current_row = queen_positions[col]

        min_conf = n
        best_rows = []

        rows[current_row] -= 1
        pos_diag[current_row + col] -= 1
        neg_diag[n - 1 + current_row - col] -= 1

        for r in range(n):
            # Пресмятаме броя конфликти, ако поставим царицата в ред r
            conflicts = (
                rows[r]
                + pos_diag[r + col]
                + neg_diag[n - 1 + r - col]
            )

            # Търсим ред с минимален конфликт
            if conflicts < min_conf:
                min_conf = conflicts
                best_rows = [r]
            elif conflicts == min_conf:
                best_rows.append(r)

        # Задаваме малка вероятност за random ход
        if random.random() < 0.01:
            new_row = random.randint(0, n - 1)
        else:
            new_row = random.choice(best_rows)

        # Ако редът се променя -> актуализираме конфликтите
        queen_positions[col] = new_row
        rows[new_row] += 1
        pos_diag[new_row + col] += 1
        neg_diag[n - 1 + new_row - col] += 1

    return None

def main():
    n = int(input())
    start_time = time.time()

    if n in (2, 3):
        print(-1)
        return

    result = min_conflicts(n)
    end_time = time.time()

    elapsed_ms = (end_time - start_time) * 1000
    # print(f"# TIME_MS: alg={elapsed_ms:.3f}")
    print(result)

    if n <= 0:
        print_board(result)

if __name__ == "__main__":
    main()