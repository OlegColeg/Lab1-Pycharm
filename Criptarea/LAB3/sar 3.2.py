def creeaza_mapare_alfabet():
    """Creează maparea pentru alfabetul românesc: 31 de litere codificate cu 0-30"""
    alfabet_ro = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"

    # Dictionar litera -> numar
    litera_la_numar = {}
    for i, litera in enumerate(alfabet_ro):
        litera_la_numar[litera] = i

    # Dictionar numar -> litera
    numar_la_litera = {}
    for i, litera in enumerate(alfabet_ro):
        numar_la_litera[i] = litera

    return litera_la_numar, numar_la_litera, alfabet_ro


def pregateste_text(text):
    """Pregătește textul: elimină spații și convertește la majuscule"""
    alfabet_ro = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"

    text_procesat = ""
    for c in text.upper():
        if c in alfabet_ro:
            text_procesat += c

    return text_procesat


def pregateste_cheie(cheie):
    """Pregătește cheia: elimină spații și convertește la majuscule"""
    alfabet_ro = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"

    cheie_procesata = ""
    for c in cheie.upper():
        if c in alfabet_ro:
            cheie_procesata += c

    return cheie_procesata


def extinde_cheie(text, cheie):
    """Extinde cheia pentru a acoperi întreaga lungime a textului"""
    cheie_extinsa = ""
    index_cheie = 0

    for i in range(len(text)):
        cheie_extinsa += cheie[index_cheie % len(cheie)]
        index_cheie += 1

    return cheie_extinsa


def cripteaza_vigenere(text, cheie):
    """
    Criptează textul folosind cifrul Vigenère
    Formula: c_i = (m_i + k_i) mod 31
    """
    litera_la_numar, numar_la_litera, alfabet_ro = creeaza_mapare_alfabet()

    # Pregătește textul și cheia
    text_clar = pregateste_text(text)
    cheie_procesata = pregateste_cheie(cheie)

    if len(text_clar) == 0:
        return "", [], [], [], []

    # Extinde cheia
    cheie_extinsa = extinde_cheie(text_clar, cheie_procesata)

    # Afișează procesul
    print("\n" + "=" * 80)
    print("PROCESUL DE CRIPTARE")
    print("=" * 80)
    print(f"\nText clar:     {text_clar}")
    print(f"Cheie:         {cheie_extinsa}")

    # Listele pentru tabel
    text_litere = []
    cheie_litere = []
    text_numere = []
    cheie_numere = []
    suma_mod = []
    text_cifrat_litere = []

    text_cifrat = ""

    for i in range(len(text_clar)):
        # Convertește literele în numere
        m_i = litera_la_numar[text_clar[i]]
        k_i = litera_la_numar[cheie_extinsa[i]]

        # Aplică formula: c_i = (m_i + k_i) mod 31
        c_i = (m_i + k_i) % 31

        # Convertește înapoi în literă
        litera_cifrata = numar_la_litera[c_i]
        text_cifrat += litera_cifrata

        # Salvează pentru tabel
        text_litere.append(text_clar[i])
        cheie_litere.append(cheie_extinsa[i])
        text_numere.append(m_i)
        cheie_numere.append(k_i)
        suma_mod.append(c_i)
        text_cifrat_litere.append(litera_cifrata)

    # Afișează tabelul
    print("\nTabel de criptare:")
    print("-" * 80)
    print(f"{'Text clar':<12} | {' '.join(f'{l:>2}' for l in text_litere)}")
    print(f"{'Cheie':<12} | {' '.join(f'{l:>2}' for l in cheie_litere)}")
    print(f"{'Text (num)':<12} | {' '.join(f'{n:>2}' for n in text_numere)}")
    print(f"{'Cheie (num)':<12} | {' '.join(f'{n:>2}' for n in cheie_numere)}")
    print(f"{'M+K (mod 31)':<12} | {' '.join(f'{n:>2}' for n in suma_mod)}")
    print(f"{'Text cifrat':<12} | {' '.join(f'{l:>2}' for l in text_cifrat_litere)}")
    print("-" * 80)

    return text_cifrat, text_litere, cheie_litere, text_numere, cheie_numere


def decripteaza_vigenere(text_cifrat, cheie):
    """
    Decriptează textul folosind cifrul Vigenère
    Formula: m_i = (c_i - k_i) mod 31
    """
    litera_la_numar, numar_la_litera, alfabet_ro = creeaza_mapare_alfabet()

    # Pregătește textul și cheia
    text_cifrat_procesat = pregateste_text(text_cifrat)
    cheie_procesata = pregateste_cheie(cheie)

    if len(text_cifrat_procesat) == 0:
        return "", [], [], [], []

    # Extinde cheia
    cheie_extinsa = extinde_cheie(text_cifrat_procesat, cheie_procesata)

    # Afișează procesul
    print("\n" + "=" * 80)
    print("PROCESUL DE DECRIPTARE")
    print("=" * 80)
    print(f"\nText cifrat:   {text_cifrat_procesat}")
    print(f"Cheie:         {cheie_extinsa}")

    # Listele pentru tabel
    cifrat_litere = []
    cheie_litere = []
    cifrat_numere = []
    cheie_numere = []
    diferenta_mod = []
    text_clar_litere = []

    text_clar = ""

    for i in range(len(text_cifrat_procesat)):
        # Convertește literele în numere
        c_i = litera_la_numar[text_cifrat_procesat[i]]
        k_i = litera_la_numar[cheie_extinsa[i]]

        # Aplică formula: m_i = (c_i - k_i) mod 31
        m_i = (c_i - k_i) % 31

        # Convertește înapoi în literă
        litera_clara = numar_la_litera[m_i]
        text_clar += litera_clara

        # Salvează pentru tabel
        cifrat_litere.append(text_cifrat_procesat[i])
        cheie_litere.append(cheie_xinsa[i])
        cifrat_numere.append(c_i)
        cheie_numere.append(k_i)
        diferenta_mod.append(m_i)
        text_clar_litere.append(litera_clara)

    # Afișează tabelul
    print("\nTabel de decriptare:")
    print("-" * 80)
    print(f"{'Text cifrat':<12} | {' '.join(f'{l:>2}' for l in cifrat_litere)}")
    print(f"{'Cheie':<12} | {' '.join(f'{l:>2}' for l in cheie_litere)}")
    print(f"{'Cifrat (num)':<12} | {' '.join(f'{n:>2}' for n in cifrat_numere)}")
    print(f"{'Cheie (num)':<12} | {' '.join(f'{n:>2}' for n in cheie_numere)}")
    print(f"{'C-K (mod 31)':<12} | {' '.join(f'{n:>2}' for n in diferenta_mod)}")
    print(f"{'Text clar':<12} | {' '.join(f'{l:>2}' for l in text_clar_litere)}")
    print("-" * 80)

    return text_clar, cifrat_litere, cheie_litere, cifrat_numere, cheie_numere


def afiseaza_alfabet():
    """Afișează alfabetul românesc și codificarea lui"""
    alfabet_ro = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"

    print("\n" + "=" * 80)
    print("ALFABETUL ROMÂNESC ȘI CODIFICAREA LUI")
    print("=" * 80)

    for i, litera in enumerate(alfabet_ro):
        print(f"{litera} = {i:2d}", end="   ")
        if (i + 1) % 8 == 0:
            print()
    print("\n" + "=" * 80)


def valideaza_intrare(text, tip="text"):
    """Validează intrarea utilizatorului"""
    alfabet_ro = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZaăâbcdefghiîjklmnopqrsștțuvwxyz "

    for c in text:
        if c not in alfabet_ro:
            return False, f"Caracter invalid: '{c}'. Folosiți doar litere românești (A-Z, a-z, Ă, Â, Î, Ș, Ț)."

    if tip == "cheie":
        text_fara_spatii = text.replace(" ", "")
        if len(text_fara_spatii) < 7:
            return False, "Cheia trebuie să aibă cel puțin 7 caractere (fără spații)."

    return True, ""


def meniu_principal():
    """Meniu interactiv pentru cifrul Vigenère"""
    print("=" * 80)
    print("CIFRUL VIGENÈRE PENTRU LIMBA ROMÂNĂ")
    print("=" * 80)
    print("Alfabetul românesc: 31 de litere codificate cu numerele 0, 1, ..., 30")

    while True:
        print("\n" + "=" * 80)
        print("MENIU PRINCIPAL")
        print("=" * 80)
        print("1. Afișează alfabetul și codificarea")
        print("2. Criptare")
        print("3. Decriptare")
        print("4. Ieșire")

        optiune = input("\nOpțiunea dvs. (1/2/3/4): ").strip()

        if optiune == '4':
            print("\nLa revedere!")
            break

        if optiune == '1':
            afiseaza_alfabet()
            continue

        if optiune not in ['2', '3']:
            print("Opțiune invalidă! Alegeți 1, 2, 3 sau 4.")
            continue

        # Citește cheia
        while True:
            cheie = input("\nIntroduceți cheia (minim 7 caractere): ").strip()
            valid, mesaj = valideaza_intrare(cheie, "cheie")
            if valid:
                break
            print(f"Eroare: {mesaj}")

        # Criptare
        if optiune == '2':
            while True:
                text = input("\nIntroduceți mesajul de criptat: ").strip()
                valid, mesaj = valideaza_intrare(text, "text")
                if valid:
                    break
                print(f"Eroare: {mesaj}")

            rezultat, _, _, _, _ = cripteaza_vigenere(text, cheie)
            print(f"\n{'CRIPTOGRAMĂ:':<15} {rezultat}")

        # Decriptare
        else:
            while True:
                text = input("\nIntroduceți criptograma de decriptat: ").strip()
                valid, mesaj = valideaza_intrare(text, "text")
                if valid:
                    break
                print(f"Eroare: {mesaj}")

            rezultat, _, _, _, _ = decripteaza_vigenere(text, cheie)
            print(f"\n{'MESAJ DECRIPTAT:':<15} {rezultat}")

        print("\n" + "=" * 80)


if __name__ == "__main__":
    meniu_principal()