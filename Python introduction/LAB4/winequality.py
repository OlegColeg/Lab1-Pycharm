#!/usr/bin/env python3
"""
Sisteme Inteligente - Laboratorul 4
Analiza Calității Vinurilor (Roșii și Albe)
"""

# Pasul 1: Importăm bibliotecile necesare
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

# Setăm stilul pentru vizualizări
plt.style.use('ggplot')
sns.set(font_scale=1.2)
plt.rcParams['figure.figsize'] = (12, 8)

# Pasul 2: Încărcăm seturile de date
# Definim căile către fișiere
red_wine_path = 'winequality-red.csv'
white_wine_path = 'winequality-white.csv'

# Verificăm dacă fișierele există
if not os.path.exists(red_wine_path) or not os.path.exists(white_wine_path):
    print("EROARE: Fișierele CSV nu au fost găsite în directorul de lucru.")
    print("Te rugăm să descarci seturile de date de pe Kaggle și să le salvezi în directorul scriptului:")
    print("1. Descarcă Wine Quality Data Set de pe Kaggle: https://www.kaggle.com/datasets/rajyellow46/wine-quality")
    print("2. Salvează fișierele 'winequality-red.csv' și 'winequality-white.csv' în directorul scriptului")
    print("3. Rulează din nou scriptul")
    exit(1)

# Încărcăm datele
try:
    # Citim fișierele CSV (acestea folosesc ';' ca separator)
    red_wine = pd.read_csv(red_wine_path, sep=';')
    white_wine = pd.read_csv(white_wine_path, sep=';')

    print("Fișierele au fost încărcate cu succes!")
    print(f"Dimensiune set date vin roșu: {red_wine.shape}")
    print(f"Dimensiune set date vin alb: {white_wine.shape}")
except Exception as e:
    print(f"EROARE la citirea fișierelor: {e}")
    exit(1)

# Pasul 3: Pregătirea datelor
# Adăugăm coloana 'type' pentru a identifica tipul de vin
red_wine['type'] = 'red'
white_wine['type'] = 'white'

# Combinăm cele două seturi de date
wines = pd.concat([red_wine, white_wine], axis=0)

# Resetăm indexul pentru a avea un index continuu
wines.reset_index(drop=True, inplace=True)

# Verificăm dimensiunile setului de date final
print(f"Dimensiunea setului de date combinat: {wines.shape}")

# Afișăm primele rânduri pentru a verifica structura datelor
print("\nPrimele 5 rânduri:")
print(wines.head())

# Verificăm dacă există valori lipsă
print("\nVerificăm valorile lipsă:")
missing_values = wines.isnull().sum()
print(missing_values)

if missing_values.sum() > 0:
    print("ATENȚIE: Există valori lipsă în set!")
else:
    print("Nu există valori lipsă în setul de date.")

# Pasul 4: Analiza descriptivă a datelor
# Descriere statistică de bază
print("\nDescriere statistică generală:")
print(wines.describe())

# Numărăm distribuția tipurilor de vin
print("\nDistribuția tipurilor de vin:")
type_counts = wines['type'].value_counts()
print(type_counts)
print(f"Procent vin roșu: {type_counts['red'] / len(wines) * 100:.2f}%")
print(f"Procent vin alb: {type_counts['white'] / len(wines) * 100:.2f}%")

# Convertim coloana 'type' în valori numerice pentru analiză (red = 0, white = 1)
wines['type_numeric'] = wines['type'].map({'red': 0, 'white': 1})

# Selectăm doar coloanele numerice pentru analiză
numeric_cols = [col for col in wines.columns
                if col not in ['type', 'type_numeric']
                and np.issubdtype(wines[col].dtype, np.number)]

print("\nColoane numerice pentru analiză:")
print(numeric_cols)

# Pasul 5: Calcularea statisticilor cerute pentru fiecare coloană
print("\n=== STATISTICI GRUPATE PE TIPUL DE VIN ===")


# Funcție pentru calculul modei
def get_mode(x):
    mode_result = stats.mode(x)
    # Verificăm versiunea scipy pentru a extrage corect valoarea modei
    if hasattr(mode_result, 'mode'):
        return mode_result.mode[0]
    else:
        return mode_result[0][0]


# Inițializăm dicționarul pentru statistici
statistics = {}

# Pentru fiecare coloană numerică, calculăm statisticile cerute
for col in numeric_cols:
    # Media
    mean_by_type = wines.groupby('type')[col].mean()

    # Mediana
    median_by_type = wines.groupby('type')[col].median()

    # Moda
    mode_by_type = wines.groupby('type')[col].apply(get_mode)

    # Deviația standard
    std_by_type = wines.groupby('type')[col].std()

    # Variația
    var_by_type = wines.groupby('type')[col].var()

    # Range (min-max)
    range_by_type = wines.groupby('type')[col].apply(lambda x: x.max() - x.min())

    # Combinăm statisticile într-un DataFrame
    stats_df = pd.DataFrame({
        'Medie': mean_by_type,
        'Mediană': median_by_type,
        'Modă': mode_by_type,
        'Deviație standard': std_by_type,
        'Variație': var_by_type,
        'Range': range_by_type
    })

    # Salvăm statisticile în dicționar
    statistics[col] = stats_df

    # Afișăm statisticile pentru fiecare coloană
    print(f"\nStatistici pentru {col}:")
    print(stats_df)

    # Calculăm și diferența procentuală între valorile medii pentru vinul roșu și alb
    red_mean = stats_df.loc['red', 'Medie']
    white_mean = stats_df.loc['white', 'Medie']

    if red_mean != 0:  # Evităm împărțirea la zero
        percent_diff = ((white_mean - red_mean) / abs(red_mean)) * 100
        print(f"Diferența procentuală: {percent_diff:.2f}%")
        if percent_diff > 0:
            print(f"Vinul alb are valori mai mari pentru {col} cu {abs(percent_diff):.2f}%")
        else:
            print(f"Vinul roșu are valori mai mari pentru {col} cu {abs(percent_diff):.2f}%")

# Pasul 6: Vizualizări pentru a compara distribuțiile
plt.figure(figsize=(15, 12))

for i, col in enumerate(numeric_cols):
    plt.subplot(4, 3, i + 1)
    sns.boxplot(x='type', y=col, data=wines)
    plt.title(f'Boxplot: {col} vs Type')
    plt.tight_layout()

plt.savefig('boxplots.png')
print("\nGraficul boxplots.png a fost salvat.")
plt.close()

# Vizualizăm distribuția densității pentru fiecare caracteristică
plt.figure(figsize=(15, 12))

for i, col in enumerate(numeric_cols):
    plt.subplot(4, 3, i + 1)
    sns.kdeplot(data=wines, x=col, hue='type', fill=True, common_norm=False, alpha=.5)
    plt.title(f'Densitate: {col} per Type')
    plt.tight_layout()

plt.savefig('density_plots.png')
print("Graficul density_plots.png a fost salvat.")
plt.close()

# Pasul 7: Calcularea corelațiilor
# Calculăm corelațiile între toate variabilele numerice
correlation_matrix = wines.select_dtypes(include=[np.number]).corr()

# Afișăm matricea de corelație
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Matricea de Corelație')
plt.tight_layout()
plt.savefig('correlation_matrix.png')
print("Graficul correlation_matrix.png a fost salvat.")
plt.close()

# Pasul 8: Identificarea celor mai importante caracteristici
# Calculăm corelațiile absolute între fiecare caracteristică și tipul de vin
correlations = []
for col in numeric_cols:
    corr = abs(np.corrcoef(wines[col], wines['type_numeric'])[0, 1])
    correlations.append((col, corr))

# Sortăm corelațiile în ordine descrescătoare
correlations.sort(key=lambda x: x[1], reverse=True)

print("\n=== CORELAȚII ABSOLUTE CU TIPUL DE VIN ===")
for col, corr in correlations:
    print(f"{col}: {corr:.4f}")

# Vizualizăm top 5 caracteristici cu cea mai mare corelație
top_features = [corr[0] for corr in correlations[:5]]

plt.figure(figsize=(15, 10))
for i, feature in enumerate(top_features):
    plt.subplot(2, 3, i + 1)
    sns.scatterplot(x=feature, y='type_numeric', data=wines, alpha=0.3)
    plt.title(f'{feature} vs Type (corr={correlations[i][1]:.4f})')
    plt.ylabel('Type (0=red, 1=white)')

plt.tight_layout()
plt.savefig('top_correlations.png')
print("Graficul top_correlations.png a fost salvat.")
plt.close()

# Pasul 9: Vizualizarea distribuției celor mai importante caracteristici
plt.figure(figsize=(15, 10))
for i, feature in enumerate(top_features[:5]):
    plt.subplot(2, 3, i + 1)
    sns.histplot(data=wines, x=feature, hue='type', kde=True,
                 element="step", palette=['red', 'skyblue'], bins=30)
    plt.title(f'Distribuția {feature}')
    plt.tight_layout()

plt.savefig('feature_distributions.png')
print("Graficul feature_distributions.png a fost salvat.")
plt.close()

# Pasul 10: Explicarea rezultatelor
print("\n=== EXPLICAREA REZULTATELOR ===")
print("Din analiză, am identificat următoarele caracteristici cu cea mai mare corelație cu tipul de vin:")

for i, (feature, corr) in enumerate(correlations[:5]):
    print(f"\n{i + 1}. {feature} (corelație: {corr:.4f}):")
    print(f"   - Media pentru vinul roșu: {statistics[feature].loc['red', 'Medie']:.4f}")
    print(f"   - Media pentru vinul alb: {statistics[feature].loc['white', 'Medie']:.4f}")
    print(f"   - Diferența: {statistics[feature].loc['white', 'Medie'] - statistics[feature].loc['red', 'Medie']:.4f}")

    # Explicații pentru fiecare caracteristică
    if feature == 'total sulfur dioxide':
        print("   Explicație: Dioxidul de sulf total este semnificativ mai mare în vinurile albe, deoarece")
        print("   acestea necesită mai mult conservant pentru a preveni oxidarea și pentru a menține prospețimea.")
        print("   Vinurile roșii conțin taninuri care acționează ca antioxidanți naturali, reducând necesitatea SO2.")
        print("   În industria vinificației, vinurile albe sunt de obicei tratate cu doze mai mari de SO2 pentru")
        print("   a preveni oxidarea și dezvoltarea bacteriilor nedorite.")

    elif feature == 'chlorides':
        print(
            "   Explicație: Clorurile (mineralele de sare) sunt mai abundente în vinurile roșii. Acest lucru se datorează")
        print(
            "   procesului de macerare, unde pielea strugurilor roșii eliberează mai multe minerale, inclusiv săruri.")
        print("   De asemenea, strugurii roșii sunt adesea cultivați în soluri cu un conținut mai ridicat de minerale.")
        print("   Vinurile albe au un conținut mai redus de cloruri, contribuind la profilul lor mai proaspăt și acid.")

    elif feature == 'volatile acidity':
        print("   Explicație: Aciditatea volatilă este mai mare în vinurile roșii datorită procesului de fermentare")
        print("   malolactică, care transformă acidul malic în acid lactic, eliberând compuși volatili.")
        print("   Vinurile roșii sunt adesea fermentate la temperaturi mai ridicate și pentru perioade mai lungi,")
        print("   ceea ce poate conduce la niveluri mai ridicate de acizi volatili, în special acid acetic.")
        print(
            "   Vinurile albe sunt de obicei fermentate la temperaturi mai scăzute, păstrând aciditatea volatilă redusă.")

    elif feature == 'free sulfur dioxide':
        print("   Explicație: SO2 liber este mai mare în vinurile albe pentru a le proteja împotriva oxidării")
        print("   și pentru a menține prospețimea aromatică. Vinurile albe, având mai puțini compuși fenolici")
        print("   (taninuri) decât vinurile roșii, sunt mai susceptibile la oxidare și deteriorare microbiană.")
        print("   Acest nivel mai ridicat de SO2 liber ajută la conservarea aromelor proaspete și fructate.")

    elif feature == 'density':
        print("   Explicație: Densitatea tinde să fie mai mare în vinurile roșii din cauza conținutului")
        print("   mai ridicat de extracte uscate, taninuri și compuși fenolici extrași din pielița și")
        print("   semințele strugurilor în timpul macerării. Vinurile albe, fiind produse fără contact")
        print("   prelungit cu părțile solide ale strugurilor, au o densitate mai mică.")

# Pasul 11: Concluzii
print("\n=== CONCLUZII ===")
print("În urma analizei statistice detaliate a caracteristicilor vinurilor roșii și albe, am identificat")
print("diferențe semnificative care permit distingerea acestora. Aceste diferențe reflectă atât")
print("compoziția chimică naturală a strugurilor, cât și diferitele tehnici de vinificație utilizate.")
print("\nCele mai distinctive caracteristici sunt:")
for i, (feature, corr) in enumerate(correlations[:3]):
    print(f"{i + 1}. {feature} (corelație: {corr:.4f})")

print("\nAceste caracteristici oferă o bază solidă pentru clasificarea automată a vinurilor folosind")
print("algoritmi de Machine Learning. Diferențele chimice identificate sunt direct legate de procesele")
print("de producție distincte pentru vinurile roșii și albe, precum și de materialele prime utilizate.")
print("\nDin punct de vedere al științei datelor, am demonstrat cum analiza statistică simplă poate")
print("evidenția tipare importante în date, care pot fi utilizate ulterior pentru construirea modelelor")
print("predictive eficiente.")