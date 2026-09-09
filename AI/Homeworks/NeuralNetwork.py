import math
import random


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

def dsigmoid(y):
    return y * (1 - y)

def tanh(x):
    return math.tanh(x)

def dtanh(y):
    return 1 - y * y


# Инициализация
def init_network(layers):
    weights = []
    biases = []

    for i in range(len(layers) - 1):
        weights.append([
            [random.uniform(-1, 1) for _ in range(layers[i])]
            for _ in range(layers[i + 1])
        ])
        biases.append([random.uniform(-1, 1) for _ in range(layers[i + 1])])

    return weights, biases


# Forward propagation
def forward(inputs, weights, biases, act):
    activations = [inputs]

    for i in range(len(weights)):
        layer_out = []
        for j in range(len(weights[i])):
            s = biases[i][j]
            for k in range(len(activations[-1])):
                s += weights[i][j][k] * activations[-1][k]
            layer_out.append(act(s))
        activations.append(layer_out)

    return activations


# Backpropagation
def backward(activations, expected, weights, biases, dact):
    deltas = [None] * len(weights)

    # Изходен слой
    deltas[-1] = [
        (expected[i] - activations[-1][i]) * dact(activations[-1][i])
        for i in range(len(expected))
    ]

    # Скритите слоеве
    for i in reversed(range(len(deltas) - 1)):
        deltas[i] = []
        for j in range(len(activations[i + 1])):
            err = 0
            for k in range(len(deltas[i + 1])):
                err += deltas[i + 1][k] * weights[i + 1][k][j]
            deltas[i].append(err * dact(activations[i + 1][j]))

    # Обновяване на теглата
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            for k in range(len(weights[i][j])):
                weights[i][j][k] += deltas[i][j] * activations[i][k]
            biases[i][j] += deltas[i][j]


# Обучение
def train(data, weights, biases, act, dact, epochs):
    for _ in range(epochs):
        for x, y in data:
            activations = forward(x, weights, biases, act)
            backward(activations, y, weights, biases, dact)


# Тестване
def test(name, data, weights, biases, act):
    print(f"\n{name}:")
    for x, _ in data:
        y = forward(x, weights, biases, act)[-1][0]
        print(f"{tuple(x)} -> {y:.4f}")


def main():
    # -------- Вход --------
    function_name = input().strip()     # AND, OR, XOR, ALL
    activation_type = int(input())      # 0 - sigmoid, 1 - tanh
    hidden_layers = int(input())        # брой скрити слоеве

    neurons = []
    for _ in range(hidden_layers):
        neurons.append(int(input()))    # неврони за всеки слой

    # -------- Данни --------
    functions = {
        "AND": [([0, 0], [0]), ([0, 1], [0]), ([1, 0], [0]), ([1, 1], [1])],
        "OR":  [([0, 0], [0]), ([0, 1], [1]), ([1, 0], [1]), ([1, 1], [1])],
        "XOR": [([0, 0], [0]), ([0, 1], [1]), ([1, 0], [1]), ([1, 1], [0])]
    }

    act, dact = (sigmoid, dsigmoid) if activation_type == 0 else (tanh, dtanh)

    to_run = ["AND", "OR", "XOR"] if function_name == "ALL" else [function_name]

    # -------- Обучение и тест --------
    for fn in to_run:
        layers = [2] + neurons + [1]
        weights, biases = init_network(layers)
        train(functions[fn], weights, biases, act, dact, epochs=1000)
        test(fn, functions[fn], weights, biases, act)


if __name__ == "__main__":
    main()
