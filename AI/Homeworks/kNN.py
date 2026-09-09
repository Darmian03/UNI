import math
import random


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


def main():
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


if __name__ == "__main__":
    main()