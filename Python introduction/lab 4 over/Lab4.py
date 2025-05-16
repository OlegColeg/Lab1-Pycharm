import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression

# 1. Citim datele din fișierul CSV și eliminăm rândurile cu valori lipsă
df = pd.read_csv("wine-quality-white-and-red.csv")


# 2. Afișăm câte valori lipsă are fiecare coloană (pentru verificare)
print(df.isna().sum())

# 3. Afișăm statistici de bază (media, min, max, etc.) pentru fiecare coloană numerică
print(df.describe())

# 4. Convertim coloana 'type' în valori numerice: 0 = red, 1 = white
df["type"] = df["type"].map({"red": 0, "white": 1})

# 5. Grupăm datele după tipul vinului și calculăm:
#    - media (mean),
#    - valoarea centrală (median),
#    - abaterea standard (std),
#    - variația (var),
#    - intervalul valorilor (max - min) cu ajutorul funcției lambda
statistical_analysis = df.groupby("type").agg(
    [
        "mean",
        "median",
        "std",           # abaterea standard: cât variază valorile față de medie
        "var",           # variația (varianța): cât de răspândite sunt valorile
        lambda x: x.max() - x.min()  # intervalul (range): diferența între max și min
    ]
)
print(statistical_analysis)

# 6. Calculăm corelația absolută a fiecărei coloane cu 'type' (tipul vinului),
#    apoi sortăm rezultatele pentru a vedea ce caracteristici sunt cele mai relevante
correlation = df.corr()["type"].abs().sort_values(ascending=False)
print("Corelația cu tipul de vin:\n", correlation)

# 7. Vizualizăm distribuția acidității volatile în funcție de tipul de vin
sns.histplot(data=df, x="volatile acidity", hue="type")
plt.title("Distribuția acidității volatile pe tipuri de vin")
plt.show()

# 8. Vizualizăm distribuția alcoolului în funcție de tipul de vin folosind boxplot
sns.boxplot(data=df, x="type", y="alcohol")
plt.title("Distribuția alcoolului în funcție de tipul vinului")
plt.show()

# 9. Afișăm o hartă a corelațiilor între toate caracteristicile
plt.figure(figsize=(12, 10))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.title("Matricea corelațiilor între caracteristici")
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# 10. Alegem 3 caracteristici care au corelație mai mare cu tipul vinului
top_features = ["free sulfur dioxide", "citric acid", "residual sugar"]
X = df[top_features]  # setul de intrare (features)
y = df["type"]        # eticheta (tipul de vin)

# 11. Împărțim datele în set de antrenament (80%) și testare (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 12. Creăm și antrenăm un model de regresie logistică pentru clasificarea vinului
model = LogisticRegression()
model.fit(X_train, y_train)

# 13. Facem predicții pe setul de testare și evaluăm performanța modelului
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=["Red", "White"])

print(f"Acuratețea modelului: {accuracy:.2%}")
print("Raportul de clasificare:\n", report)

# 14. Vizualizăm distribuția celor 3 caracteristici selectate pentru fiecare tip de vin
sns.set(style="whitegrid")
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for i, feature in enumerate(top_features):
    sns.histplot(
        data=df,
        x=feature,
        hue="type",
        kde=True,
        ax=axes[i],
        palette="Set1",
        element="step",
        common_norm=False,
    )
    axes[i].set_title(f"Distribuția caracteristicii: {feature}")

plt.tight_layout()
plt.show()