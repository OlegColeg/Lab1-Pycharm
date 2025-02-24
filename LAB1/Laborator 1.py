def accuracy_score(y_true, y_pred):
    correct_predictions = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp)
    return correct_predictions / len(y_true)


def precision_recall_score(y_true, y_pred):
    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    return precision, recall


def mse(y_true, y_pred):
    errors = [(yt - yp) ** 2 for yt, yp in zip(y_true, y_pred)]
    return sum(errors) / len(y_true)


def mae(y_true, y_pred):
    errors = [abs(yt - yp) for yt, yp in zip(y_true, y_pred)]
    return sum(errors) / len(y_true)


# Datele test
y_pred = [1, 1, 1, 0, 1, 0, 1, 1, 0, 0]
y_true = [1, 1, 1, 0, 1, 0, 1, 0, 1, 0]

# Testare funcții
print("Accuracy:", accuracy_score(y_true, y_pred))
print("Precision & Recall:", precision_recall_score(y_true, y_pred))
print("MSE:", mse(y_true, y_pred))
print("MAE:", mae(y_true, y_pred))
