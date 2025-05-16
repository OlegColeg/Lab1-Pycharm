# Importul bibliotecilor necesare
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Încărcarea datelor
df = pd.read_csv('Automobile.csv')

# 1. Analiza și curățarea datelor
print("Primele 5 rânduri din setul de date:")
print(df.head())

print("\nInformații despre setul de date:")
print(df.info())

print("\nStatistici descriptive:")
print(df.describe())

print("\nVerificarea valorilor lipsă:")
print(df.isnull().sum())

# Înlocuirea valorilor lipsă cu media pentru coloanele numerice
for col in df.select_dtypes(include=np.number).columns:
    df[col] = df[col].fillna(df[col].mean())

# Verificarea valorilor lipsă după înlocuire
print("\nValori lipsă după înlocuire:")
print(df.isnull().sum())

# 2. Vizualizarea datelor
plt.figure(figsize=(12, 6))
sns.countplot(x='origin', data=df)
plt.title('Distribuția automobilelor în funcție de origine')
plt.savefig('origin_distribution.png')
plt.close()

plt.figure(figsize=(12, 6))
sns.boxplot(x='origin', y='mpg', data=df)
plt.title('Distribuția MPG în funcție de origine')
plt.savefig('mpg_by_origin.png')
plt.close()

plt.figure(figsize=(12, 6))
sns.boxplot(x='origin', y='horsepower', data=df)
plt.title('Distribuția puterii motorului în funcție de origine')
plt.savefig('horsepower_by_origin.png')
plt.close()

# 3. Pregătirea datelor pentru modelare
# Selectarea caracteristicilor și țintei
X = df.drop(['name', 'origin'], axis=1)
y = df['origin']

# Împărțirea datelor în set de antrenare și testare
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Standardizarea caracteristicilor
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. Antrenarea și evaluarea modelelor
models = {
    'Regresie Logistică': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(random_state=42),
    'SVM': SVC(random_state=42),
    'KNN': KNeighborsClassifier()
}

results = {}

for name, model in models.items():
    # Antrenarea modelului
    model.fit(X_train_scaled, y_train)

    # Predicția
    y_pred = model.predict(X_test_scaled)

    # Evaluarea modelului
    accuracy = accuracy_score(y_test, y_pred)
    results[name] = accuracy

    print(f"\nModel: {name}")
    print(f"Acuratețe: {accuracy:.4f}")
    print("\nRaport de clasificare:")
    print(classification_report(y_test, y_pred))

    # Matrice de confuzie
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
    plt.title(f'Matrice de confuzie - {name}')
    plt.xlabel('Predicție')
    plt.ylabel('Valoare reală')
    plt.savefig(f'confusion_matrix_{name}.png')
    plt.close()

# 5. Compararea modelelor
plt.figure(figsize=(10, 6))
sns.barplot(x=list(results.keys()), y=list(results.values()))
plt.title('Compararea acurateței modelelor')
plt.ylim(0, 1)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('model_comparison.png')
plt.close()

# Găsirea celui mai bun model
best_model = max(results, key=results.get)
print(f"\nCel mai bun model: {best_model} cu acuratețea {results[best_model]:.4f}")

# 6. Importanța caracteristicilor (pentru Random Forest)
if 'Random Forest' in models:
    rf_model = models['Random Forest']
    feature_importances = pd.Series(rf_model.feature_importances_, index=X.columns)
    plt.figure(figsize=(12, 8))
    feature_importances.sort_values(ascending=False).plot(kind='bar')
    plt.title('Importanța caracteristicilor în modelul Random Forest')
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    plt.close()

# 7. Concluzie
print("\nCONCLUZIE:")
print(f"1. Am învățat că originea automobilelor poate fi clasificată cu succes folosind caracteristicile lor tehnice.")
print(f"2. Cel mai bun model a fost {best_model}, obținând o acuratețe de {results[best_model]:.4f}.")
print("3. Caracteristicile precum consumul (mpg), puterea motorului și greutatea sunt importante pentru clasificare.")
print(
    "4. Îmbunătățiri potențiale: optimizarea hiperparametrilor, adăugarea de caracteristici noi sau utilizarea tehnicilor de ensemble learning.")