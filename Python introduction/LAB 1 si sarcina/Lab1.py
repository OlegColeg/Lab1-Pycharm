#
# Exerciții
# 1. Se dau următoarele etichete prezise de un clasificator binar, y_pred = [1, 1, 1, 0, 1,
# 0, 1, 1, 0, 0] și etichetele y_true = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0].
# a. Definiți metoda accuracy_score(y_true, y_pred) care să calculeze acuratețea
# clasificatorului binar.
# Obs:
# - Acuratețe =
# 𝑛
# i$1 𝑦_𝑝𝑟𝑒𝑑i
# -- 𝑦_𝑡𝑟𝑢𝑒i
# 𝑛
# print(two_rand_nums())
# ∑
# Sisteme inteligente Laboratorul 1
# b. Definiți metoda precision_recall_score(y_true, y_pred) care returnează
# precizia și recall-ul clasificatorului binar.
# Obs:
# - 0 - negativ, 1 - pozitiv
# 𝑡𝑝
# - Precizie =
# 𝑡𝑝 1 2𝑝
# 𝑡𝑝
# - Recall =
# 𝑡𝑝 1 2𝑛
# - tp = true positive, numărul etichetelor prezise ca fiind pozitive și care
# au fost clasificate corect
# - fp = false positive, numărul etichetelor prezise ca fiind pozitive, dar
# care sunt de fapt negative
# - fn = false negative, numărul etichetelor prezise ca fiind negative, dar
# care sunt de fapt pozitive
# c. Definiți metoda mse(y_true, y_pred) (mean square error) care calculează
# media pătratelor erorilor de clasificare.
# Obs:
# - MSE =
# 𝑛
# i$1 (𝑦_𝑝𝑟𝑒𝑑i – 𝑦_𝑡𝑟𝑢𝑒i)
# 6
# 𝑛
# d. Definiți metoda mae(y_true, y_pred) (mean absolute error) care calculează
# media erorii absolute de clasificare.
# Obs:
# - MAE =
# 𝑛
# i$1 |𝑦_𝑝𝑟𝑒𝑑i – 𝑦_𝑡𝑟𝑢𝑒i
# |
y_pred = [1, 1, 1, 0, 1, 0, 1, 1, 0, 0]
y_true = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

tp = 0
tn = 0
fp = 0
fn = 0
for i in range(len(y_pred)):
    if y_pred[i] == 1 and y_pred[i] == y_true[i]:
        tp += 1
for i in range(len(y_pred)):
    if y_pred[i] == 1 and y_pred[i] != y_true[i]:
        fp += 1
for i in range(len(y_pred)):
    if y_pred[i] == 0 and y_pred[i] != y_true[i]:
        fn += 1
for i in range(len(y_pred)):
    if y_pred[i] == 0 and y_pred[i]  == y_true[i]:
        tn += 1

    print("TP: ", tp)
    print("TN: ", tn)
    print("FP: ", fp)
    print("FN: ", fn)
    break
