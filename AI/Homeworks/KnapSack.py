import random
import time

# POPULATION_SIZE = 2000  N * 10
# TOURNAMENT_SIZE = 20    N // 10
# MUTATION_RATE = 0.005   1 / N
GENERATIONS = 50

def read_input():
    # Четене на стандартния вход.
    first_line = input().strip().split()
    capacity = int(first_line[0])
    n = int(first_line[1])
    weights = []
    values = []
    for _ in range(n):
        m, c = map(int, input().strip().split())
        weights.append(m)
        values.append(c)
    return capacity, weights, values

def fitness(individual, weights, values, capacity):
    # Фитнес функция на хромозома (ако weight > 0 стойността е 0).
    total_weight = 0
    total_value = 0
    for i, gene in enumerate(individual):
        if gene == 1:
            total_weight += weights[i]
            total_value += values[i]
    if total_weight > capacity:
        return total_value // 2 - total_weight + capacity
    else:
        return total_value

def tournament_selection(population, fitnesses, n):
    # Tournament selection...
    tournament_size = max( 10, n // 10) 
    best = None
    for _ in range(tournament_size):
        i = random.randint(0, len(population) - 1)
        if best is None or fitnesses[i] > fitnesses[best]:
            best = i
    return population[best][:]

def uniform_crossover(parent1, parent2):
    # Uniform crossover...
    child1, child2 = [], []
    for g1, g2 in zip(parent1, parent2):
        if random.random() < 0.5:
            child1.append(g1)
            child2.append(g2)
        else:
            child1.append(g2)
            child2.append(g1)
    return child1, child2

def mutate(individual, n):
    # Mutation...
    for i in range(n):
        if random.random() < 1/n:
            individual[i] = 1 - individual[i]

def genetic_knapsack(capacity, weights, values):
    # Генетичния алгоритъм.
    n = len(weights)
    population_size  = n * 15

    population = [[random.randint(0, 1) for _ in range(n)] for _ in range(population_size)]
    fitnesses = [fitness(ind, weights, values, capacity) for ind in population]

    best_values = []
    for gen in range(GENERATIONS):
        new_population = []
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, fitnesses, n)
            parent2 = tournament_selection(population, fitnesses, n)
            child1, child2 = uniform_crossover(parent1, parent2)
            mutate(child1, n)
            mutate(child2, n)

            new_population.extend([child1, child2])
        population = new_population[:population_size]
        fitnesses = [fitness(ind, weights, values, capacity) for ind in population]
        best = max(fitnesses)
        if gen == 0 or gen % (GENERATIONS // 10) == 0 or gen == GENERATIONS - 1:
            best_values.append(best)

    return best_values

def main():
    capacity, weights, values = read_input()

    start_time = time.time()
    best_values = genetic_knapsack(capacity, weights, values)
    end_time = time.time()

    elapsed_ms = (end_time - start_time) * 1000
    print(f"# TIMES_MS: alg={elapsed_ms:.3f}")
    for val in best_values:
        print(val)
    print()
    print(best_values[-1])

if __name__ == "__main__":
    main()