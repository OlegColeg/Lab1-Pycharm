import numpy as np
from skimage import io
import matplotlib.pyplot as plt

# a. Citirea imaginilor din fișiere și salvarea într-un np.array de dimensiune 9x400x600
def citire_imagini():
    images_array = np.zeros((9, 400, 600))
    for idx in range(9):
        file_path = f"images/car_{idx}.npy"
        try:
            image = np.load(file_path)
            images_array[idx] = image
        except FileNotFoundError:
            print(f"Fișierul {file_path} nu a fost găsit.")
    return images_array

# Citire imagini
images_array = citire_imagini()
print(f"Forma array-ului de imagini: {images_array.shape}")

# b. Calcularea sumei valorilor pixelilor tuturor imaginilor
suma_totala = np.sum(images_array)
print(f"Suma totală a valorilor pixelilor din toate imaginile: {suma_totala}")

# c. Calcularea sumei valorilor pixelilor pentru fiecare imagine în parte
sume_per_imagine = np.sum(images_array, axis=(1, 2))
print("Suma valorilor pixelilor pentru fiecare imagine:")
for idx, suma in enumerate(sume_per_imagine):
    print(f"Imagine {idx}: {suma}")

# d. Afișarea indexului imaginii cu suma maximă
idx_max = np.argmax(sume_per_imagine)
print(f"Indexul imaginii cu suma maximă: {idx_max}")

# e. Calcularea și afișarea imaginii medii
mean_image = np.mean(images_array, axis=0)
print(f"Forma imaginii medii: {mean_image.shape}")

# Afișarea imaginii medii
plt.figure(figsize=(10, 6))
plt.imshow(mean_image.astype(np.uint8))
plt.title("Imaginea medie")
plt.colorbar()
plt.savefig("mean_image.png")

# Folosind skimage pentru afișare
io.imshow(mean_image.astype(np.uint8))
io.show()

# f. Calcularea deviației standard a imaginilor
std_dev = np.std(images_array)
print(f"Deviația standard a imaginilor: {std_dev}")

# g. Normalizarea imaginilor
normalized_images = (images_array - mean_image) / std_dev
print(f"Forma array-ului de imagini normalizate: {normalized_images.shape}")
print(f"Media imaginilor normalizate: {np.mean(normalized_images)}")
print(f"Deviația standard a imaginilor normalizate: {np.std(normalized_images)}")

# h. Decuparea fiecărei imagini (liniile 200-300, coloanele 280-400)
cropped_images = images_array[:, 200:301, 280:401]
print(f"Forma array-ului de imagini decupate: {cropped_images.shape}")

# Afișarea primei imagini decupate pentru verificare
plt.figure(figsize=(6, 6))
plt.imshow(cropped_images[0].astype(np.uint8))
plt.title("Prima imagine decupată")
plt.colorbar()
plt.savefig("cropped_image_0.png")

# Funcție pentru a afișa toate imaginile decupate
def afiseaza_imagini_decupate(images):
    fig, axes = plt.subplots(3, 3, figsize=(12, 12))
    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            if idx < len(images):
                axes[i, j].imshow(images[idx].astype(np.uint8))
                axes[i, j].set_title(f"Imagine {idx} decupată")
                axes[i, j].axis('off')
    plt.tight_layout()
    plt.savefig("toate_imaginile_decupate.png")
    plt.show()

# Afișarea tuturor imaginilor decupate
afiseaza_imagini_decupate(cropped_images)