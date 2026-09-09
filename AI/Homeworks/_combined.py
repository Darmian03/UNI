import math
import random

# -----------------------------
# kNN Implementation
# -----------------------------

def load_iris_data(path):
    # Зареждане на Iris данните от файла
    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            features = list(map(float, parts[:4]))
            label = parts[4]
            data.append((features, label))
    return data


def min_max_normalize(dataset):
    # Нормализация (Min-Max) на всички характеристики до [0, 1]
    # Извличаме само колоните
    cols = list(zip(*[row[0] for row in dataset]))

    mins = [min(col) for col in cols]
    maxs = [max(col) for col in cols]

    normalized = []
    for features, label in dataset:
        new_f = []
        for i, val in enumerate(features):
            if maxs[i] - mins[i] == 0:
                new_f.append(0.0)
            else:
                new_f.append((val - mins[i]) / (maxs[i] - mins[i]))
        normalized.append((new_f, label))

    return normalized


def stratified_split(dataset, train_ratio=0.8):
    # Разделяне на данните на train и test сетове
    by_class = {}
    for features, label in dataset:
        by_class.setdefault(label, []).append((features, label))

    train, test = [], []

    for label, items in by_class.items():
        random.shuffle(items)
        split = int(len(items) * train_ratio)
        train.extend(items[:split])
        test.extend(items[split:])

    random.shuffle(train)
    random.shuffle(test)
    return train, test


def euclidean_distance(a, b):
    # Евклидово разстояние между два вектора
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(len(a))))


def knn_predict(train, input_features, k):
    # kNN алгоритъма
    distances = []
    for feat, label in train:
        d = euclidean_distance(feat, input_features)
        distances.append((d, label))

    distances.sort(key=lambda x: x[0])
    k_nearest = distances[:k]

    # Мажоритарно гласуване
    votes = {}
    for _, label in k_nearest:
        votes[label] = votes.get(label, 0) + 1

    return max(votes.items(), key=lambda x: x[1])[0]


def accuracy(dataset, predictions):
    # Изчисляване на точността
    correct = sum(1 for (_, label), pred in zip(dataset, predictions) if label == pred)
    return correct / len(dataset)


def cross_validation(dataset, k, folds=10):
    # Cross валидация
    random.shuffle(dataset)
    fold_size = len(dataset) // folds

    accs = []

    for i in range(folds):
        # Създаваме fold
        start = i * fold_size
        end = start + fold_size

        test_fold = dataset[start:end]
        train_fold = dataset[:start] + dataset[end:]

        preds = [knn_predict(train_fold, feat, k) for feat, _ in test_fold]
        acc = accuracy(test_fold, preds)
        accs.append(acc)

    avg = sum(accs) / len(accs)
    var = sum((x - avg) ** 2 for x in accs) / len(accs)
    std = math.sqrt(var)

    return accs, avg, std


def main_kNN():
    k_value = int(input().strip())

    # 1. Зареждаме
    data = load_iris_data("data/iris/iris.data")

    # 2. Нормализираме
    data = min_max_normalize(data)

    # 3. Stratified train/test split
    train_set, test_set = stratified_split(data)

    # 4. Тренираме accuracy
    train_preds = [knn_predict(train_set, feat, k_value) for feat, _ in train_set]
    train_acc = accuracy(train_set, train_preds)

    # 5. 10-fold CV
    fold_acc, avg_acc, std_acc = cross_validation(train_set, k_value)

    # 6. Тестваме accuracy
    test_preds = [knn_predict(train_set, feat, k_value) for feat, _ in test_set]
    test_acc = accuracy(test_set, test_preds)

    # 7. Извеждане
    print("1. Train Set Accuracy:")
    print(f"    Accuracy: {train_acc * 100:.2f}%\n")

    print("2. 10-Fold Cross-Validation Results:\n")
    for i, a in enumerate(fold_acc, 1):
        print(f"    Accuracy Fold {i}: {a * 100:.2f}%")
    print()
    print(f"    Average Accuracy: {avg_acc * 100:.2f}%")
    print(f"    Standard Deviation: {std_acc * 100:.2f}%\n")

    print("3. Test Set Accuracy:")
    print(f"    Accuracy: {test_acc * 100:.2f}%")


# -----------------------------
# NBC Implementation
# -----------------------------


import math
import random


def load_data(path, mode):
    data = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            cls = parts[0]
            attrs = parts[1:]
            data.append((cls, attrs))

    if mode == 0:
        return data
    else:
        return fill_missing_with_mode(data)


def fill_missing_with_mode(dataset):
    classes = {}
    for cls, attrs in dataset:
        classes.setdefault(cls, []).append(attrs)

    # Намерете мода по клас и атрибут
    modes = {}
    for cls, rows in classes.items():
        cols = list(zip(*rows))
        col_modes = []
        for col in cols:
            non_missing = [x for x in col if x != "?"]
            if not non_missing:
                col_modes.append("y")  # fallback
            else:
                # мода
                col_modes.append(max(set(non_missing), key=non_missing.count))
        modes[cls] = col_modes

    # заместете
    new_data = []
    for cls, attrs in dataset:
        new_attrs = []
        for i, val in enumerate(attrs):
            if val == "?":
                new_attrs.append(modes[cls][i])
            else:
                new_attrs.append(val)
        new_data.append((cls, new_attrs))

    return new_data


def stratified_split(dataset, train_ratio=0.8):
    by_class = {}
    for cls, attrs in dataset:
        by_class.setdefault(cls, []).append((cls, attrs))

    train, test = [], []

    for cls, items in by_class.items():
        random.shuffle(items)
        split = int(len(items) * train_ratio)
        train.extend(items[:split])
        test.extend(items[split:])

    random.shuffle(train)
    random.shuffle(test)
    return train, test


def train_nb(train, lambda_smooth=1.0):
    class_counts = {}
    feature_counts = {}
    classes = set([row[0] for row in train])

    for cls in classes:
        class_counts[cls] = 0
        feature_counts[cls] = [dict() for _ in range(16)]

    for cls, attrs in train:
        class_counts[cls] += 1
        for i in range(16):
            val = attrs[i]
            feature_counts[cls][i][val] = feature_counts[cls][i].get(val, 0) + 1

    total = len(train)
    return class_counts, feature_counts, total


def predict_nb(model, row, lambda_smooth=1.0):
    class_counts, feat_counts, total = model
    attrs = row[1]

    best_class = None
    best_log = -1e18

    for cls in class_counts.keys():
        logp = math.log(class_counts[cls] / total)

        for i in range(16):
            val = attrs[i]
            count = feat_counts[cls][i].get(val, 0)
            denom = class_counts[cls] + lambda_smooth * len(feat_counts[cls][i])
            num = count + lambda_smooth
            logp += math.log(num / denom)

        if logp > best_log:
            best_log = logp
            best_class = cls

    return best_class


def accuracy(dataset, model):
    correct = 0
    for row in dataset:
        pred = predict_nb(model, row)
        if pred == row[0]:
            correct += 1
    return correct / len(dataset)


def cross_validate(dataset, folds=10, lambda_smooth=1.0):
    random.shuffle(dataset)
    fold_size = len(dataset) // folds

    accs = []

    for i in range(folds):
        start = i * fold_size
        end = start + fold_size

        test_fold = dataset[start:end]
        train_fold = dataset[:start] + dataset[end:]

        model = train_nb(train_fold, lambda_smooth)
        acc = accuracy(test_fold, model)
        accs.append(acc)

    avg = sum(accs) / len(accs)
    var = sum((x - avg) ** 2 for x in accs) / len(accs)
    std = math.sqrt(var)
    return accs, avg, std


def main_NBC():
    mode = int(input().strip())    # 0 или 1

    # 1. Зареждаме
    data = load_data("data/congressional+voting+records/house-votes-84.data", mode)

    # 2. Stratified train/test split
    train_set, test_set = stratified_split(data)

    # 3. Тренираме NB
    model = train_nb(train_set)

    # 4. Тренираме точността
    train_acc = accuracy(train_set, model)

    # 5. 10-fold CV
    fold_acc, avg_acc, std_acc = cross_validate(train_set)

    # 6. Тестваме Accuracy
    test_acc = accuracy(test_set, model)

    # 7. Извеждане
    print("1. Train Set Accuracy:")
    print(f"    Accuracy: {train_acc * 100:.2f}%\n")

    print("2. 10-Fold Cross-Validation Results:\n")
    for i, a in enumerate(fold_acc, 1):
        print(f"    Accuracy Fold {i}: {a * 100:.2f}%")
    print()
    print(f"    Average Accuracy: {avg_acc * 100:.2f}%")
    print(f"    Standard Deviation: {std_acc * 100:.2f}%\n")

    print("3. Test Set Accuracy:")
    print(f"    Accuracy: {test_acc * 100:.2f}%")


# -----------------------------
# ID3 Implementation
# -----------------------------

import math
import random


def load_breast_cancer(path):
    # Зареждане на Breast Cancer данните
    data = []
    with open(path, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            label = parts[0]        # class label
            features = parts[1:]   # categorical attributes
            data.append((features, label))
    return data


def fill_missing_values(dataset):
    # Обработка на липсващи стойности '?' чрез модална стойност на атрибута по клас
    # values[attr_index][class] = list of values
    values = {}

    for features, label in dataset:
        for i, val in enumerate(features):
            if val != "?":
                if i not in values:
                    values[i] = {}
                if label not in values[i]:
                    values[i][label] = []
                values[i][label].append(val)

    # намиране на модална стойност
    modes = {}
    for i in values:
        modes[i] = {}
        for label in values[i]:
            counts = {}
            for v in values[i][label]:
                counts[v] = counts.get(v, 0) + 1
            modes[i][label] = max(counts, key=counts.get)

    # замяна на '?'
    new_data = []
    for features, label in dataset:
        new_features = []
        for i, val in enumerate(features):
            if val == "?":
                new_features.append(modes[i][label])
            else:
                new_features.append(val)
        new_data.append((new_features, label))

    return new_data


def entropy(dataset):
    # Ентропия и информационна печалба
    counts = {}
    for _, label in dataset:
        counts[label] = counts.get(label, 0) + 1

    total = len(dataset)
    ent = 0.0
    for c in counts.values():
        p = c / total
        ent -= p * math.log2(p)
    return ent


def information_gain(dataset, attr):
    base_entropy = entropy(dataset)
    subsets = {}

    for features, label in dataset:
        val = features[attr]
        if val not in subsets:
            subsets[val] = []
        subsets[val].append((features, label))

    remainder = 0.0
    for subset in subsets.values():
        remainder += (len(subset) / len(dataset)) * entropy(subset)

    return base_entropy - remainder


def majority_class(dataset):
    counts = {}
    for _, label in dataset:
        counts[label] = counts.get(label, 0) + 1
    return max(counts, key=counts.get)


# =====================================================
# Дърво на решенията (ID3)
# =====================================================

class Node:
    def __init__(self, attribute=None, label=None):
        self.attribute = attribute  # index of attribute
        self.label = label          # class label (for leaf)
        self.children = {}

    def is_leaf(self):
        return self.label is not None


def id3(dataset, attributes, min_gain):
    # Pre-pruning: използваме минимална информационна печалба G
    labels = [label for _, label in dataset]

    # ако всички примери са от един клас
    if labels.count(labels[0]) == len(labels):
        return Node(label=labels[0])

    # ако няма атрибути
    if not attributes:
        return Node(label=majority_class(dataset))

    # избор на най-добър атрибут
    best_attr = None
    best_gain = -1
    for attr in attributes:
        gain = information_gain(dataset, attr)
        if gain > best_gain:
            best_gain = gain
            best_attr = attr

    # pre-pruning по минимална информационна печалба
    if best_gain < min_gain:
        return Node(label=majority_class(dataset))

    node = Node(attribute=best_attr)
    subsets = {}

    for features, label in dataset:
        val = features[best_attr]
        if val not in subsets:
            subsets[val] = []
        subsets[val].append((features, label))

    remaining_attrs = [a for a in attributes if a != best_attr]

    for val in subsets:
        node.children[val] = id3(subsets[val], remaining_attrs, min_gain)

    return node


def predict(tree, features):
    while not tree.is_leaf():
        val = features[tree.attribute]
        if val not in tree.children:
            return tree.label
        tree = tree.children[val]
    return tree.label


# =====================================================
# Post-pruning: Reduced Error Pruning
# =====================================================

def accuracy(dataset, tree):
    correct = 0
    for features, label in dataset:
        if predict(tree, features) == label:
            correct += 1
    return correct / len(dataset)


def reduced_error_pruning(tree, train_set, val_set):
    if tree.is_leaf():
        return tree

    for val in tree.children:
        tree.children[val] = reduced_error_pruning(
            tree.children[val], train_set, val_set
        )

    acc_before = accuracy(val_set, tree)

    pruned = Node(label=majority_class(train_set))
    acc_after = accuracy(val_set, pruned)

    if acc_after >= acc_before:
        return pruned
    return tree


def stratified_split(dataset, ratio=0.8):
    by_class = {}
    for item in dataset:
        label = item[1]
        if label not in by_class:
            by_class[label] = []
        by_class[label].append(item)

    train, test = [], []
    for items in by_class.values():
        random.shuffle(items)
        split = int(len(items) * ratio)
        train.extend(items[:split])
        test.extend(items[split:])

    random.shuffle(train)
    random.shuffle(test)
    return train, test


def cross_validation(dataset, min_gain, folds=10):
    random.shuffle(dataset)
    fold_size = len(dataset) // folds
    accs = []

    for i in range(folds):
        start = i * fold_size
        end = start + fold_size
        val = dataset[start:end]
        train = dataset[:start] + dataset[end:]

        attrs = list(range(len(dataset[0][0])))
        tree = id3(train, attrs, min_gain)
        accs.append(accuracy(val, tree))

    avg = sum(accs) / folds
    std = math.sqrt(sum((a - avg) ** 2 for a in accs) / folds)
    return accs, avg, std


def main_ID3():
    mode = int(input().strip())  # 0, 1 или 2

    data = load_breast_cancer("data/breast+cancer/breast-cancer.data")
    data = fill_missing_values(data)

    train_set, test_set = stratified_split(data)
    attributes = list(range(len(data[0][0])))

    MIN_GAIN = 0.1  # за pre-pruning

    # обучение
    tree = id3(
        train_set,
        attributes,
        MIN_GAIN if mode in [0, 2] else 0.0
    )

    # post-pruning
    if mode in [1, 2]:
        train_set, val_set = stratified_split(train_set, 0.9)
        tree = reduced_error_pruning(tree, train_set, val_set)

    # резултати
    train_acc = accuracy(train_set, tree)
    folds, avg, std = cross_validation(train_set, MIN_GAIN)
    test_acc = accuracy(test_set, tree)

    print("1. Train Set Accuracy:")
    print(f"    Accuracy: {train_acc*100:.2f}%\n")

    print("10-Fold Cross-Validation Results:\n")
    for i, a in enumerate(folds, 1):
        print(f"    Accuracy Fold {i}: {a*100:.2f}%")

    print(f"\n    Average Accuracy: {avg*100:.2f}%")
    print(f"    Standard Deviation: {std*100:.2f}%\n")

    print("2. Test Set Accuracy:")
    print(f"    Accuracy: {test_acc*100:.2f}%")


# -----------------------------
# kMeans Implementation
# -----------------------------


import math
import random


# -------------------------------------------------
# Данни
# -------------------------------------------------

def load_data(path):
    data = []
    with open(path, "r") as f:
        for line in f:
            x, y = map(float, line.split())
            data.append((x, y))
    return data


def euclidean(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


# -------------------------------------------------
# Инициализации
# -------------------------------------------------

def random_centroids(data, k):
    return random.sample(data, k)


def kmeans_plus_plus(data, k):
    centroids = [random.choice(data)]

    while len(centroids) < k:
        distances = []
        for p in data:
            d = min(euclidean(p, c)**2 for c in centroids)
            distances.append(d)

        r = random.uniform(0, sum(distances))
        s = 0
        for i, d in enumerate(distances):
            s += d
            if s >= r:
                centroids.append(data[i])
                break

    return centroids


# -------------------------------------------------
# k-Means
# -------------------------------------------------

def assign(data, centroids):
    labels = []
    for p in data:
        dists = [euclidean(p, c) for c in centroids]
        labels.append(dists.index(min(dists)))
    return labels


def update(data, labels, k):
    new = []
    for i in range(k):
        cluster = [data[j] for j in range(len(data)) if labels[j] == i]
        if not cluster:
            new.append(random.choice(data))
        else:
            x = sum(p[0] for p in cluster) / len(cluster)
            y = sum(p[1] for p in cluster) / len(cluster)
            new.append((x, y))
    return new


def kmeans(data, k, init):
    centroids = init(data, k)
    for _ in range(100):
        labels = assign(data, centroids)
        new_centroids = update(data, labels, k)
        if new_centroids == centroids:
            break
        centroids = new_centroids
    return labels, centroids


# -------------------------------------------------
# Метрики
# -------------------------------------------------

def wcss(data, labels, centroids):
    return sum(euclidean(data[i], centroids[labels[i]])**2 for i in range(len(data)))


def silhouette(data, labels, k):
    scores = []

    for i, p in enumerate(data):
        same = [data[j] for j in range(len(data)) if labels[j] == labels[i] and j != i]
        a = sum(euclidean(p, q) for q in same) / len(same) if same else 0

        b = float("inf")
        for c in range(k):
            if c == labels[i]:
                continue
            other = [data[j] for j in range(len(data)) if labels[j] == c]
            if other:
                dist = sum(euclidean(p, q) for q in other) / len(other)
                b = min(b, dist)

        scores.append((b - a) / max(a, b) if max(a, b) != 0 else 0)

    return sum(scores) / len(scores)


def main_kMeans():
    filename, k = input().split()
    
    if "normal" in filename:
        path = "kMeans data/normal/normal.txt"
    else:
        path = "kMeans data/unbalance/unbalance.txt"

    data = load_data(path)

    # -------- Random Restart --------
    best = None
    best_w = float("inf")

    for _ in range(10):
        labels, centroids = kmeans(data, k, random_centroids)
        w = wcss(data, labels, centroids)
        if w < best_w:
            best_w = w
            best = (labels, centroids)

    labels, centroids = best
    print("Random Restart")
    print("WCSS:", best_w)
    print("Silhouette:", silhouette(data, labels, k))

    # -------- kMeans++ --------
    labels, centroids = kmeans(data, k, kmeans_plus_plus)
    print("\nkMeans++")
    print("WCSS:", wcss(data, labels, centroids))
    print("Silhouette:", silhouette(data, labels, k))


# -----------------------------
# NN Implementation
# -----------------------------


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
def backward(activations, expected, weights, biases, dact, lr):
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
                weights[i][j][k] += lr * deltas[i][j] * activations[i][k]
            biases[i][j] += lr * deltas[i][j]


# Обучение
def train(data, weights, biases, act, dact, lr, epochs):
    for _ in range(epochs):
        for x, y in data:
            activations = forward(x, weights, biases, act)
            backward(activations, y, weights, biases, dact, lr)


# Тестване
def test(name, data, weights, biases, act):
    print(f"\n{name}:")
    for x, _ in data:
        y = forward(x, weights, biases, act)[-1][0]
        print(f"{tuple(x)} -> {y:.4f}")


def main_NN():
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
        train(functions[fn], weights, biases, act, dact, lr=0.5, epochs=1000)
        test(fn, functions[fn], weights, biases, act)