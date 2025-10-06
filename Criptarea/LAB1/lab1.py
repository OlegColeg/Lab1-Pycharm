

"""
Lucrare de laborator nr. 1 - Sarcina 1.1
Cifrul lui Cezar pentru alfabetul limbii engleze
"""


def char_to_num(char):
    """
    Convertește caracterul în numărul corespunzător (A=0, B=1, ..., Z=25)
    """
    return ord(char) - ord('A')


def num_to_char(num):
    """
    Convertește numărul în caracterul corespunzător (0=A, 1=B, ..., 25=Z)
    """
    return chr(num + ord('A'))


def caesar_encrypt(text, key):
    """
    Criptează textul folosind cifrul Cezar cu cheia dată
    Formula: c = (x + k) mod 26
    """
    result = ""
    for char in text:
        if 'A' <= char <= 'Z':
            x = char_to_num(char)  # Obținem poziția în alfabet
            c = (x + key) % 26  # Aplicăm formula de criptare
            result += num_to_char(c)
    return result


def caesar_decrypt(text, key):
    """
    Decriptează textul folosind cifrul Cezar cu cheia dată
    Formula: m = (y - k) mod 26
    """
    result = ""
    for char in text:
        if 'A' <= char <= 'Z':
            y = char_to_num(char)  # Obținem poziția în alfabet
            m = (y - key + 26) % 26  # Aplicăm formula de decriptare (+26 pentru numere negative)
            result += num_to_char(m)
    return result


def validate_key(key_input):
    """
    Validează cheia introdusă de utilizator
    """
    try:
        key = int(key_input)
        if 1 <= key <= 25:
            return key, None
        else:
            return None, "Cheia trebuie să fie între 1 și 25 inclusiv!"
    except ValueError:
        return None, "Cheia trebuie să fie un număr întreg!"


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


def display_alphabet_table(key):
    """
    Afișează tabelul alfabetului pentru cheia dată (ca în Tabelul 1)
    """
    print(f"\n{'=' * 80}")
    print(f"TABELUL ALFABETULUI PENTRU CHEIA k = {key}")
    print(f"{'=' * 80}")

    # Prima linie - pozițiile 0-25
    print("Poziție: ", end="")
    for i in range(26):
        print(f"{i:2}", end=" ")
    print()

    # A doua linie - alfabetul original
    print("Original:", end=" ")
    for i in range(26):
        print(f"{num_to_char(i):2}", end=" ")
    print()

    # A treia linie - pozițiile deplasate
    print("Deplasare:", end="")
    for i in range(26):
        shifted_pos = (i + key) % 26
        print(f"{shifted_pos:2}", end=" ")
    print()

    # A patra linie - alfabetul deplasat
    print("Rezultat:", end=" ")
    for i in range(26):
        shifted_pos = (i + key) % 26
        print(f"{num_to_char(shifted_pos):2}", end=" ")
    print()
    print(f"{'=' * 80}")


def main_menu():
    """
    Afișează meniul principal
    """
    print("\n" + "=" * 50)
    print("🔒 CIFRUL LUI CEZAR")
    print("=" * 50)
    print("1. Criptare")
    print("2. Decriptare")
    print("3. Afișează tabelul alfabetului")
    print("4. Ieșire")
    print("=" * 50)


def main():
    """
    Funcția principală a programului
    """
    print("Bun venit la implementarea Cifrului lui Cezar!")
    print("Alfabetul folosit: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z")
    print("Pozițiile:          0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25")

    while True:
        main_menu()
        choice = input("Alegeti o opțiune (1-4): ").strip()

        if choice == '1':  # Criptare
            print("\n--- CRIPTARE ---")

            # Introducerea cheii
            while True:
                key_input = input("Introduceți cheia (1-25): ").strip()
                key, error = validate_key(key_input)
                if key:
                    break
                print(f"❌ Eroare: {error}")

            # Introducerea textului
            while True:
                text_input = input("Introduceți textul de criptat: ").strip()
                text, error = validate_text(text_input)
                if text:
                    break
                print(f"❌ Eroare: {error}")

            # Preprocesarea și criptarea
            processed_text = preprocess_text(text)
            encrypted_text = caesar_encrypt(processed_text, key)

            print(f"\n✅ REZULTATUL CRIPTĂRII:")
            print(f"Text original: {text}")
            print(f"Text procesat: {processed_text}")
            print(f"Text criptat: {encrypted_text}")

        elif choice == '2':  # Decriptare
            print("\n--- DECRIPTARE ---")

            # Introducerea cheii
            while True:
                key_input = input("Introduceți cheia (1-25): ").strip()
                key, error = validate_key(key_input)
                if key:
                    break
                print(f"❌ Eroare: {error}")

            # Introducerea criptogramei
            while True:
                text_input = input("Introduceți criptograma: ").strip()
                text, error = validate_text(text_input)
                if text:
                    break
                print(f"❌ Eroare: {error}")

            # Preprocesarea și decriptarea
            processed_text = preprocess_text(text)
            decrypted_text = caesar_decrypt(processed_text, key)

            print(f"\n✅ REZULTATUL DECRIPTĂRII:")
            print(f"Criptograma: {text}")
            print(f"Criptograma procesată: {processed_text}")
            print(f"Text decriptat: {decrypted_text}")

        elif choice == '3':  # Afișează tabelul
            print("\n--- TABELUL ALFABETULUI ---")
            while True:
                key_input = input("Introduceți cheia pentru a afișa tabelul (1-25): ").strip()
                key, error = validate_key(key_input)
                if key:
                    break
                print(f"❌ Eroare: {error}")

            display_alphabet_table(key)

        elif choice == '4':  # Ieșire
            print("\n👋 La revedere!")
            break

        else:
            print("❌ Opțiune invalidă! Alegeți între 1-4.")

        # Pauză pentru a citi rezultatul
        input("\nApăsați Enter pentru a continua...")


# Funcții pentru testare rapidă (opțional)
def quick_test():
    """
    Testare rapidă a algoritmului cu exemple din documentație
    """
    print("\n" + "=" * 60)
    print("TESTARE RAPIDĂ")
    print("=" * 60)

    # Testul 1: Exemplul din documentație
    print("Test 1 - Exemplul din documentație:")
    print("Mesaj: 'cifrul cezar', Cheia: 3")

    original = "cifrul cezar"
    processed = preprocess_text(original)
    encrypted = caesar_encrypt(processed, 3)
    decrypted = caesar_decrypt(encrypted, 3)

    print(f"Original: {original}")
    print(f"Procesat: {processed}")
    print(f"Criptat: {encrypted}")
    print(f"Decriptat: {decrypted}")
    print(f"Test {'✅ REUȘIT' if processed == decrypted else '❌ EȘUAT'}")

    # Testul 2: Testul cu S -> V
    print(f"\nTest 2 - Litera S cu cheia 3:")
    s_encrypted = caesar_encrypt('S', 3)
    s_decrypted = caesar_decrypt(s_encrypted, 3)
    print(f"S criptat cu k=3: {s_encrypted}")
    print(f"{s_encrypted} decriptat cu k=3: {s_decrypted}")
    print(f"Test {'✅ REUȘIT' if s_decrypted == 'S' else '❌ EȘUAT'}")


if __name__ == "__main__":
    # Rulează testele rapide întâi
    quick_test()

    # Apoi rulează programul principal
    main()