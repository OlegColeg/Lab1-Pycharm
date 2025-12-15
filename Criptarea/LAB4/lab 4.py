#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lucrare de laborator nr. 4 - Algoritmul DES
Sarcina 2.4: În algoritmul DES este dat mesajul (8 caractere). De aflat L₁.

Student: Poziția 15 în catalog
Formula: 15 mod 11 = 4 (Sarcina 2.4)
"""

import random

# Tabelele standard DES
IP_TABLE = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

E_TABLE = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

P_TABLE = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

PC1_TABLE = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2_TABLE = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

S_BOXES = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]


def afiseaza_tabel(titlu, tabel, cols=8):
    """Afișează un tabel într-un format ușor de citit"""
    print(f"\n{titlu}:")
    print("-" * 60)
    for i in range(0, len(tabel), cols):
        print("  ".join(f"{tabel[j]:2d}" for j in range(i, min(i + cols, len(tabel)))))
    print()


def text_to_binary(text):
    """Convertește text în string binar"""
    binary = ''.join(format(ord(c), '08b') for c in text)
    return binary


def binary_to_hex(binary):
    """Convertește string binar în hexazecimal"""
    hex_value = hex(int(binary, 2))[2:].upper().zfill(len(binary) // 4)
    return hex_value


def permute(input_bits, table):
    """Aplică o permutare conform unui tabel dat"""
    return ''.join(input_bits[i - 1] for i in table)


def left_shift(bits, n):
    """Rotește biții la stânga cu n pozițiți"""
    return bits[n:] + bits[:n]


def xor(bits1, bits2):
    """Efectuează operația XOR între doi vectori de biți"""
    return ''.join('1' if b1 != b2 else '0' for b1, b2 in zip(bits1, bits2))


def s_box_substitution(input_48_bits):
    """Aplică substituția prin S-boxes"""
    output = ''
    for i in range(8):
        # Extragem blocul de 6 biți
        block = input_48_bits[i * 6:(i + 1) * 6]

        # Calculăm rândul (primul și ultimul bit)
        row = int(block[0] + block[5], 2)

        # Calculăm coloana (cei 4 biți din mijloc)
        col = int(block[1:5], 2)

        # Obținem valoarea din S-box
        val = S_BOXES[i][row][col]

        # Convertim în binar (4 biți)
        output += format(val, '04b')

    return output


def generate_subkey(key_64_bits, round_num):
    """Generează subcheia pentru runda dată"""
    # PC-1 permutation
    key_56_bits = permute(key_64_bits, PC1_TABLE)

    # Împărțim în C și D
    C = key_56_bits[:28]
    D = key_56_bits[28:]

    # Aplicăm shift-urile pentru fiecare rundă
    for i in range(round_num):
        C = left_shift(C, SHIFT_TABLE[i])
        D = left_shift(D, SHIFT_TABLE[i])

    # Combinăm și aplicăm PC-2
    CD = C + D
    subkey = permute(CD, PC2_TABLE)

    return subkey


def f_function(R, subkey):
    """Funcția f din DES"""
    # Expansiune E
    expanded_R = permute(R, E_TABLE)

    # XOR cu subcheia
    xor_result = xor(expanded_R, subkey)

    # S-box substitution
    s_box_output = s_box_substitution(xor_result)

    # Permutare P
    result = permute(s_box_output, P_TABLE)

    return result


def calculate_L1(message, key):
    """
    Calculează L₁ în algoritmul DES

    Pași:
    1. Convertim mesajul în binar (64 biți)
    2. Aplicăm permutarea inițială IP
    3. Împărțim în L₀ și R₀
    4. Generăm subcheia K₁
    5. Calculăm L₁ = R₀ (conform formulei Ln = Rn-1)
    """

    print("\n" + "=" * 70)
    print(" CALCULUL LUI L₁ ÎN ALGORITMUL DES")
    print("=" * 70)

    # Pasul 1: Convertim mesajul în binar
    print(f"\n➤ PASUL 1: Convertirea mesajului în binar")
    print(f"   Mesaj (text): '{message}'")

    message_bits = text_to_binary(message)
    print(f"   Mesaj (binar): {message_bits}")
    print(f"   Mesaj (hex):   {binary_to_hex(message_bits)}")
    print(f"   Lungime: {len(message_bits)} biți")

    # Afișare formatată a mesajului în blocuri
    print(f"\n   Mesaj formatat (blocuri de 8 biți):")
    for i in range(0, 64, 8):
        byte_val = message_bits[i:i + 8]
        char = chr(int(byte_val, 2))
        print(f"   Biți {i + 1:2d}-{i + 8:2d}: {byte_val} = {int(byte_val, 2):3d} = '{char}'")

    # Pasul 2: Aplicăm permutarea inițială IP
    print(f"\n➤ PASUL 2: Aplicarea permutării inițiale IP")
    afiseaza_tabel("Tabelul IP", IP_TABLE, 8)

    ip_result = permute(message_bits, IP_TABLE)
    print(f"   Rezultat după IP: {ip_result}")
    print(f"   Rezultat (hex):   {binary_to_hex(ip_result)}")

    # Pasul 3: Împărțim în L₀ și R₀
    print(f"\n➤ PASUL 3: Împărțirea în L₀ și R₀")
    L0 = ip_result[:32]
    R0 = ip_result[32:]

    print(f"   L₀ = {L0}")
    print(f"   L₀ (hex) = {binary_to_hex(L0)}")
    print(f"   L₀ (formatat):")
    for i in range(0, 32, 8):
        print(f"      {L0[i:i + 8]}")

    print(f"\n   R₀ = {R0}")
    print(f"   R₀ (hex) = {binary_to_hex(R0)}")
    print(f"   R₀ (formatat):")
    for i in range(0, 32, 8):
        print(f"      {R0[i:i + 8]}")

    # Pasul 4: Generăm subcheia K₁
    print(f"\n➤ PASUL 4: Generarea subcheii K₁")
    print(f"   Cheie (text): '{key}'")

    key_bits = text_to_binary(key)
    print(f"   Cheie (binar): {key_bits}")
    print(f"   Cheie (hex):   {binary_to_hex(key_bits)}")

    K1 = generate_subkey(key_bits, 1)
    print(f"\n   Subcheia K₁ = {K1}")
    print(f"   K₁ (hex) = {binary_to_hex(K1)}")
    print(f"   K₁ (formatat în blocuri de 6 biți):")
    for i in range(0, 48, 6):
        print(f"      {K1[i:i + 6]}")

    # Pasul 5: Calculăm L₁
    print(f"\n➤ PASUL 5: Calculul lui L₁")
    print(f"\n   Formula DES pentru runda 1:")
    print(f"   L₁ = R₀")
    print(f"   R₁ = L₀ ⊕ f(R₀, K₁)")

    L1 = R0

    print(f"\n   Conform formulei Ln = Rn-1:")
    print(f"   L₁ = R₀ = {L1}")
    print(f"   L₁ (hex) = {binary_to_hex(L1)}")

    # Bonus: Calculăm și R₁ pentru completitudine
    print(f"\n➤ BONUS: Calculul complet al rundei 1 (inclusiv R₁)")

    print(f"\n   a) Expansiunea E(R₀):")
    expanded_R0 = permute(R0, E_TABLE)
    print(f"      E(R₀) = {expanded_R0}")
    print(f"      E(R₀) (hex) = {binary_to_hex(expanded_R0)}")

    print(f"\n   b) XOR: K₁ ⊕ E(R₀):")
    xor_result = xor(K1, expanded_R0)
    print(f"      K₁       = {K1}")
    print(f"      E(R₀)    = {expanded_R0}")
    print(f"      K₁⊕E(R₀) = {xor_result}")

    print(f"\n   c) Substituție S-boxes:")
    print(f"      Input (8 blocuri × 6 biți):")
    for i in range(8):
        block = xor_result[i * 6:(i + 1) * 6]
        print(f"         B{i + 1} = {block}")

    s_box_output = s_box_substitution(xor_result)
    print(f"\n      Output (8 blocuri × 4 biți):")
    for i in range(8):
        block = s_box_output[i * 4:(i + 1) * 4]
        print(f"         S{i + 1}(B{i + 1}) = {block} = {int(block, 2)}")

    print(f"\n      S-boxes output complet: {s_box_output}")

    print(f"\n   d) Permutare P:")
    f_result = permute(s_box_output, P_TABLE)
    print(f"      f(R₀, K₁) = {f_result}")
    print(f"      f(R₀, K₁) (hex) = {binary_to_hex(f_result)}")

    print(f"\n   e) Calcul R₁:")
    R1 = xor(L0, f_result)
    print(f"      L₀          = {L0}")
    print(f"      f(R₀, K₁)   = {f_result}")
    print(f"      R₁ = L₀⊕f   = {R1}")
    print(f"      R₁ (hex)    = {binary_to_hex(R1)}")

    # Rezultat final
    print("\n" + "=" * 70)
    print(" REZULTAT FINAL")
    print("=" * 70)
    print(f"\n   L₁ = {L1}")
    print(f"   L₁ (hex) = {binary_to_hex(L1)}")
    print(f"\n   L₁ formatat (blocuri de 4 biți):")
    for i in range(0, 32, 4):
        print(f"      {L1[i:i + 4]}", end="")
        if (i + 4) % 16 == 0:
            print()

    print(f"\n\n   Verificare: L₁ (32 biți) = {L1}")
    print(f"              R₁ (32 biți) = {R1}")
    print(f"              L₁ + R₁ = {len(L1) + len(R1)} biți ✓")
    print("\n" + "=" * 70)

    return L1


def main():
    """Funcția principală"""
    print("\n" + "=" * 70)
    print(" LUCRARE DE LABORATOR NR. 4 - ALGORITMUL DES")
    print(" Sarcina 2.4: Calculul lui L₁")
    print(" Student: Poziția 15 în catalog (15 mod 11 = 4)")
    print("=" * 70)

    # Meniu
    print("\nAlegeți modul de introducere a datelor:")
    print("1. Introduceți manual mesajul și cheia")
    print("2. Folosiți valorile implicite (din PDF)")
    print("3. Generați aleatoriu mesajul și cheia")

    choice = input("\nOpțiunea dvs. (1/2/3): ").strip()

    if choice == "1":
        # Input manual
        message = input("\nIntroduceți mesajul (exact 8 caractere): ")
        while len(message) != 8:
            print("❌ Eroare: Mesajul trebuie să aibă exact 8 caractere!")
            message = input("Introduceți mesajul (exact 8 caractere): ")

        key = input("Introduceți cheia (exact 8 caractere): ")
        while len(key) != 8:
            print("❌ Eroare: Cheia trebuie să aibă exact 8 caractere!")
            key = input("Introduceți cheia (exact 8 caractere): ")

    elif choice == "3":
        # Generare aleatorie
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        message = ''.join(random.choice(chars) for _ in range(8))
        key = ''.join(random.choice(chars) for _ in range(8))

        print(f"\n✓ Mesaj generat aleatoriu: '{message}'")
        print(f"✓ Cheie generată aleatoriu: '{key}'")

    else:
        # Valori implicite din PDF
        # Mesajul din PDF în hex: 0123456789ABCDEF
        # Convertim în caractere ASCII
        message = "\x01\x23\x45\x67\x89\xAB\xCD\xEF"
        # Cheia din PDF: 133457799BBCDFF1
        key = "\x13\x34\x57\x79\x9B\xBC\xDF\xF1"

        print(f"\n✓ Folosim valorile din PDF:")
        print(f"  Mesaj (hex): 0123456789ABCDEF")
        print(f"  Cheie (hex): 133457799BBCDFF1")

    # Calculăm L₁
    L1 = calculate_L1(message, key)

    # Salvăm rezultatul într-un fișier
    import os
    output_file = os.path.join(os.path.expanduser("~"), "rezultat_L1.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write(" REZULTATUL CALCULULUI L₁ ÎN DES\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Mesaj (text): '{message}'\n")
        f.write(f"Mesaj (hex):  {binary_to_hex(text_to_binary(message))}\n")
        f.write(f"Cheie (text): '{key}'\n")
        f.write(f"Cheie (hex):  {binary_to_hex(text_to_binary(key))}\n\n")
        f.write(f"L₁ (binar): {L1}\n")
        f.write(f"L₁ (hex):   {binary_to_hex(L1)}\n")

    print(f"\n✓ Rezultatul a fost salvat în: {output_file}")


if __name__ == "__main__":
    main()
