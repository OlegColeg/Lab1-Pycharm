#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lucrare de laborator nr. 1 - Sarcina 1.2
Cifrul lui Cezar cu permutare (2 chei)
k1 = cheia numerică (1-25)
k2 = cuvântul-cheie pentru permutarea alfabetului (min 7 litere)
"""


def create_permuted_alphabet(keyword):
    """
    Creează alfabetul permutat bazat pe cuvântul-cheie
    Exemplu: keyword="cryptography" -> "CRYPTOGAHBDEFI..."
    """
    # Convertim cuvântul-cheie la majuscule și eliminăm duplicatele păstrând ordinea
    seen = set()
    unique_keyword = ""
    for char in keyword.upper():
        if char not in seen and char.isalpha():
            seen.add(char)
            unique_keyword += char

    # Creăm alfabetul permutat: cuvântul-cheie + restul literelor în ordine
    permuted = unique_keyword
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if char not in seen:
            permuted += char

    return permuted


def char_to_pos(char, alphabet):
    """
    Găsește poziția unui caracter în alfabetul dat
    """
    return alphabet.index(char)


def pos_to_char(pos, alphabet):
    """
    Convertește o poziție în caracterul corespunzător din alfabetul dat
    """
    return alphabet[pos]


def caesar_encrypt_permuted(text, k1, k2):
    """
    Criptează textul folosind cifrul Cezar cu alfabetul permutat
    k1 = cheia numerică pentru deplasare
    k2 = cuvântul-cheie pentru permutarea alfabetului
    """
    permuted_alphabet = create_permuted_alphabet(k2)
    result = ""

    for char in text:
        if 'A' <= char <= 'Z':
            # Găsim poziția în alfabetul original
            original_pos = ord(char) - ord('A')  # A=0, B=1, etc.

            # Aplicăm formula Cezar cu alfabetul permutat
            # c = (x + k1) mod 26, dar folosim alfabetul permutat
            encrypted_pos = (original_pos + k1) % 26
            encrypted_char = pos_to_char(encrypted_pos, permuted_alphabet)
            result += encrypted_char

    return result, permuted_alphabet


def caesar_decrypt_permuted(text, k1, k2):
    """
    Decriptează textul folosind cifrul Cezar cu alfabetul permutat
    k1 = cheia numerică pentru deplasare
    k2 = cuvântul-cheie pentru permutarea alfabetului
    """
    permuted_alphabet = create_permuted_alphabet(k2)
    result = ""

    for char in text:
        if 'A' <= char <= 'Z':
            # Găsim poziția caracterului în alfabetul permutat
            encrypted_pos = char_to_pos(char, permuted_alphabet)

            # Aplicăm formula inversă pentru a obține poziția originală
            # m = (y - k1 + 26) mod 26
            original_pos = (encrypted_pos - k1 + 26) % 26
            original_char = chr(original_pos + ord('A'))  # Convertim la caracter original
            result += original_char

    return result, permuted_alphabet


def validate_k1(key_input):
    """
    Validează prima cheie (numerică)
    """
    try:
        key = int(key_input)
        if 1 <= key <= 25:
            return key, None
        else:
            return None, "Cheia k1 trebuie să fie între 1 și 25 inclusiv!"
    except ValueError:
        return None, "Cheia k1 trebuie să fie un număr întreg!"


def validate_k2(keyword):
    """
    Validează a doua cheie (cuvântul-cheie)
    """
    if not keyword or keyword.strip() == "":
        return None, "Cuvântul-cheie k2 nu poate fi gol!"

    # Verifică dacă conține doar litere
    clean_keyword = keyword.strip()
    if not clean_keyword.isalpha():
        return None, "Cuvântul-cheie k2 poate conține doar litere ale alfabetului latin!"

    # Verifică lungimea minimă
    if len(clean_keyword) < 7:
        return None, "Cuvântul-cheie k2 trebuie să aibă o lungime de cel puțin 7 caractere!"

    return clean_keyword, None


def validate_text(text):
    """
    Validează textul introdus de utilizator
    """
    if not text or text.strip() == "":
        return None, "Textul nu poate fi gol!"

    # Verifică dacă textul conține doar litere și spații
    for char in text:
        if not (char.isalpha() or char.isspace()):
            return None, "Textul poate conține doar litere (A-Z, a-z) și spații!"

    return text, None


def preprocess_text(text):
    """
    Preprocesează textul: transformă în majuscule și elimină spațiile
    """
    return text.upper().replace(' ', '')


def display_permutation_table(k1, k2):
    """
    Afișează tabelul cu alfabetul permutat (ca în Tabelul 2)
    """
    permuted_alphabet = create_permuted_alphabet(k2)

    print(f"\n{'=' * 100}")
    print(f"TABELUL ALPHABETULUI PERMUTAT")
    print(f"Cheia k1 = {k1}, Cuvântul-cheie k2 = '{k2.upper()}'")
    print(f"{'=' * 100}")

    # Prima linie - pozițiile 0-25
    print("Poziție:     ", end="")
    for i in range(26):
        print(f"{i:2}", end=" ")
    print()

    # A doua linie - alfabetul original
    print("Original:    ", end="")
    for i in range(26):
        print(f"{chr(i + ord('A')):2}", end=" ")
    print()

    # A treia linie - alfabetul permutat
    print("Permutat:    ", end="")
    for char in permuted_alphabet:
        print(f"{char:2}", end=" ")
    print()

    # A patra linie - pozițiile deplasate
    print("Deplasare:   ", end="")
    for i in range(26):
        shifted_pos = (i + k1) % 26
        print(f"{shifted_pos:2}", end=" ")
    print()

    # A cincea linie - alfabetul final (cu deplasare)
    print("Rezultat:    ", end="")
    for i in range(26):
        shifted_pos = (i + k1) % 26
        print(f"{permuted_alphabet[shifted_pos]:2}", end=" ")
    print()
    print(f"{'=' * 100}")

    return permuted_alphabet


def brute_force_demo():
    """
    Demonstrația atacului brute force din documentație
    """
    print(f"\n{'=' * 80}")
    print("DEMONSTRAȚIA ATACULUI BRUTE FORCE")
    print("Exemplul din documentație: 'BRUTE FORCE ATTACK' cu k=17")
    print(f"{'=' * 80}")

    original = "BRUTE FORCE ATTACK"
    processed = preprocess_text(original)

    # Criptăm cu k=17
    encrypted = ""
    for char in processed:
        if 'A' <= char <= 'Z':
            x = ord(char) - ord('A')
            c = (x + 17) % 26
            encrypted += chr(c + ord('A'))

    print(f"Mesajul original: {original}")
    print(f"Mesajul procesat: {processed}")
    print(f"Criptat cu k=17:  {encrypted}")
    print(f"\nÎncercarea tuturor cheilor:")
    print("-" * 40)

    # Încercăm toate cheile
    for k in range(1, 26):
        decrypted = ""
        for char in encrypted:
            if 'A' <= char <= 'Z':
                y = ord(char) - ord('A')
                m = (y - k + 26) % 26
                decrypted += chr(m + ord('A'))

        # Evidențiem cheia corectă
        marker = " ← MESAJ CITIBIL!" if decrypted == processed else ""
        print(f"{k:2} {decrypted}{marker}")


def main_menu():
    """
    Afișează meniul principal
    """
    print("\n" + "=" * 60)
    print("🔒 CIFRUL LUI CEZAR CU PERMUTARE (2 CHEI)")
    print("=" * 60)
    print("1. Criptare")
    print("2. Decriptare")
    print("3. Afișează tabelul alphabetului permutat")
    print("4. Demonstrația atacului brute force")
    print("5. Ieșire")
    print("=" * 60)


def main():
    """
    Funcția principală a programului
    """
    print("🔒 CIFRUL LUI CEZAR CU PERMUTARE")
    print("Această versiune folosește 2 chei:")
    print("  k1 = cheia numerică (1-25)")
    print("  k2 = cuvântul-cheie pentru permutarea alfabetului (min 7 litere)")
    print("\nSpațiul de chei: 26! × 25 = 10,082,286,528,165,140,889,600,000,000")

    while True:
        main_menu()
        choice = input("Alegeți o opțiune (1-5): ").strip()

        if choice == '1':  # Criptare
            print("\n--- CRIPTARE ---")

            # Introducerea cheii k1
            while True:
                k1_input = input("Introduceți cheia k1 (1-25): ").strip()
                k1, error = validate_k1(k1_input)
                if k1:
                    break
                print(f"❌ Eroare: {error}")

            # Introducerea cheii k2
            while True:
                k2_input = input("Introduceți cuvântul-cheie k2 (min 7 litere): ").strip()
                k2, error = validate_k2(k2_input)
                if k2:
                    break
                print(f"❌ Eroare: {error}")

            # Introducerea textului
            while True:
                text_input = input("Introduceți textul de criptat: ").strip()
                text, error = validate_text(text_input)
                if text:
                    break
                print(f"❌ Eroare: {error}")

            # Procesarea și criptarea
            processed_text = preprocess_text(text)
            encrypted_text, permuted_alphabet = caesar_encrypt_permuted(processed_text, k1, k2)

            print(f"\n✅ REZULTATUL CRIPTĂRII:")
            print(f"Text original:        {text}")
            print(f"Text procesat:        {processed_text}")
            print(f"Cheia k1:             {k1}")
            print(f"Cuvântul-cheie k2:    {k2.upper()}")
            print(f"Alfabetul permutat:   {permuted_alphabet}")
            print(f"Text criptat:         {encrypted_text}")

        elif choice == '2':  # Decriptare
            print("\n--- DECRIPTARE ---")

            # Introducerea cheii k1
            while True:
                k1_input = input("Introduceți cheia k1 (1-25): ").strip()
                k1, error = validate_k1(k1_input)
                if k1:
                    break
                print(f"❌ Eroare: {error}")

            # Introducerea cheii k2
            while True:
                k2_input = input("Introduceți cuvântul-cheie k2 (min 7 litere): ").strip()
                k2, error = validate_k2(k2_input)
                if k2:
                    break
                print(f"❌ Eroare: {error}")

            # Introducerea criptogramei
            while True:
                text_input = input("Introduceți criptograma: ").strip()
                text, error = validate_text(text_input)
                if text:
                    break
                print(f"❌ Eroare: {error}")

            # Procesarea și decriptarea
            processed_text = preprocess_text(text)
            decrypted_text, permuted_alphabet = caesar_decrypt_permuted(processed_text, k1, k2)

            print(f"\n✅ REZULTATUL DECRIPTĂRII:")
            print(f"Criptograma:          {text}")
            print(f"Criptograma procesată: {processed_text}")
            print(f"Cheia k1:             {k1}")
            print(f"Cuvântul-cheie k2:    {k2.upper()}")
            print(f"Alfabetul permutat:   {permuted_alphabet}")
            print(f"Text decriptat:       {decrypted_text}")

        elif choice == '3':  # Afișează tabelul
            print("\n--- TABELUL ALPHABETULUI PERMUTAT ---")

            while True:
                k1_input = input("Introduceți cheia k1 (1-25): ").strip()
                k1, error = validate_k1(k1_input)
                if k1:
                    break
                print(f"❌ Eroare: {error}")

            while True:
                k2_input = input("Introduceți cuvântul-cheie k2 (min 7 litere): ").strip()
                k2, error = validate_k2(k2_input)
                if k2:
                    break
                print(f"❌ Eroare: {error}")

            display_permutation_table(k1, k2)

        elif choice == '4':  # Demonstrația brute force
            brute_force_demo()

        elif choice == '5':  # Ieșire
            print("\n👋 La revedere!")
            break

        else:
            print("❌ Opțiune invalidă! Alegeți între 1-5.")

        # Pauză pentru a citi rezultatul
        input("\nApăsați Enter pentru a continua...")


def quick_test():
    """
    Testare rapidă a algoritmului cu exemplul din documentație
    """
    print("\n" + "=" * 80)
    print("TESTARE RAPIDĂ")
    print("=" * 80)

    print("Test - Exemplul din documentație:")
    print("k1 = 3, k2 = 'cryptography'")

    k1 = 3
    k2 = "cryptography"
    test_message = "HELLO WORLD"

    processed = preprocess_text(test_message)
    encrypted, alphabet = caesar_encrypt_permuted(processed, k1, k2)
    decrypted, _ = caesar_decrypt_permuted(encrypted, k1, k2)

    print(f"Mesaj original:       {test_message}")
    print(f"Mesaj procesat:       {processed}")
    print(f"Alfabetul permutat:   {alphabet}")
    print(f"Criptat:              {encrypted}")
    print(f"Decriptat:            {decrypted}")
    print(f"Test {'✅ REUȘIT' if processed == decrypted else '❌ EȘUAT'}")

    print(f"\nComparație cu alfabetul din documentație:")
    expected_alphabet = "CRYPTOGAHBDEFIJKLMNQSUVWXZ"
    print(f"Așteptat:  {expected_alphabet}")
    print(f"Obținut:   {alphabet}")
    print(f"Alfabet {'✅ CORECT' if alphabet == expected_alphabet else '❌ INCORECT'}")


if __name__ == "__main__":
    # Rulează testele rapide întâi
    quick_test()

    # Apoi rulează programul principal
    main()