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


def main():
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


if __name__ == "__main__":
    main()