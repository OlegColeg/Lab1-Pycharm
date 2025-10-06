def creeaza_matrice(cheie):
    """Creează matricea Playfair 6x6 pentru alfabetul românesc (31 litere + 5 celule libere)"""
    alfabet_ro = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"

    # Pregătește cheia: elimină duplicate și convertește la majuscule
    cheie = cheie.upper()
    cheie_procesata = ""
    for c in cheie:
        if c in alfabet_ro and c not in cheie_procesata:
            cheie_procesata += c

    # Creează șirul pentru matrice: cheie + restul alfabetului
    sir_matrice = cheie_procesata
    for c in alfabet_ro:
        if c not in sir_matrice:
            sir_matrice += c

    # Completează cu simboluri pentru a ajunge la 36 (6x6)
    while len(sir_matrice) < 36:
        sir_matrice += "*"

    # Creează matricea 6x6
    matrice = []
    for i in range(6):
        rand = []
        for j in range(6):
            rand.append(sir_matrice[i * 6 + j])
        matrice.append(rand)

    return matrice


def afiseaza_matrice(matrice):
    """Afișează matricea Playfair"""
    print("\nMatricea Playfair:")
    for rand in matrice:
        print(" ".join(rand))
    print()


def gaseste_pozitie(matrice, litera):
    """Găsește poziția unei litere în matrice"""
    for i in range(6):
        for j in range(6):
            if matrice[i][j] == litera:
                return i, j
    return None, None


def pregateste_text(text, pentru_criptare=True):
    """Pregătește textul pentru criptare/decriptare"""
    alfabet_ro = "AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ"

    # Elimină spații și caracterele non-alfabetice, convertește la majuscule
    text_procesat = ""
    for c in text.upper():
        if c in alfabet_ro:
            text_procesat += c

    if pentru_criptare:
        # Inserează X, Q sau Z între literele duble
        text_cu_separatori = ""
        i = 0
        while i < len(text_procesat):
            text_cu_separatori += text_procesat[i]
            if i + 1 < len(text_procesat) and text_procesat[i] == text_procesat[i + 1]:
                text_cu_separatori += 'X'
            i += 1
        text_procesat = text_cu_separatori

        # Adaugă 'X' la final dacă lungimea este impară
        if len(text_procesat) % 2 == 1:
            text_procesat += 'X'

    # Împarte în perechi
    perechi = []
    for i in range(0, len(text_procesat), 2):
        if i + 1 < len(text_procesat):
            perechi.append(text_procesat[i] + text_procesat[i + 1])

    return perechi


def cripteaza_pereche(matrice, litera1, litera2):
    """Criptează o pereche de litere"""
    rand1, col1 = gaseste_pozitie(matrice, litera1)
    rand2, col2 = gaseste_pozitie(matrice, litera2)

    if rand1 is None or rand2 is None:
        return litera1 + litera2

    # Cazul 1: Linii și coloane diferite (dreptunghi)
    if rand1 != rand2 and col1 != col2:
        return matrice[rand1][col2] + matrice[rand2][col1]

    # Cazul 2: Aceeași linie
    elif rand1 == rand2:
        return matrice[rand1][(col1 + 1) % 6] + matrice[rand2][(col2 + 1) % 6]

    # Cazul 3: Aceeași coloană
    else:
        return matrice[(rand1 + 1) % 6][col1] + matrice[(rand2 + 1) % 6][col2]


def decripteaza_pereche(matrice, litera1, litera2):
    """Decriptează o pereche de litere"""
    rand1, col1 = gaseste_pozitie(matrice, litera1)
    rand2, col2 = gaseste_pozitie(matrice, litera2)

    if rand1 is None or rand2 is None:
        return litera1 + litera2

    # Cazul 1: Linii și coloane diferite (dreptunghi)
    if rand1 != rand2 and col1 != col2:
        return matrice[rand1][col2] + matrice[rand2][col1]

    # Cazul 2: Aceeași linie
    elif rand1 == rand2:
        return matrice[rand1][(col1 - 1) % 6] + matrice[rand2][(col2 - 1) % 6]

    # Cazul 3: Aceeași coloană
    else:
        return matrice[(rand1 - 1) % 6][col1] + matrice[(rand2 - 1) % 6][col2]


def cripteaza_playfair(text, cheie):
    """Criptează textul folosind algoritmul Playfair"""
    matrice = creeaza_matrice(cheie)
    afiseaza_matrice(matrice)

    perechi = pregateste_text(text, pentru_criptare=True)
    print(f"Text pregătit în perechi: {' '.join(perechi)}\n")

    text_criptat = ""
    for pereche in perechi:
        text_criptat += cripteaza_pereche(matrice, pereche[0], pereche[1])

    return text_criptat


def decripteaza_playfair(text_criptat, cheie):
    """Decriptează textul folosind algoritmul Playfair"""
    matrice = creeaza_matrice(cheie)
    afiseaza_matrice(matrice)

    perechi = pregateste_text(text_criptat, pentru_criptare=False)
    print(f"Text criptat în perechi: {' '.join(perechi)}\n")

    text_decriptat = ""
    for pereche in perechi:
        text_decriptat += decripteaza_pereche(matrice, pereche[0], pereche[1])

    return text_decriptat


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
    """Meniu interactiv pentru algoritmul Playfair"""
    print("=" * 60)
    print("ALGORITM PLAYFAIR PENTRU LIMBA ROMÂNĂ")
    print("=" * 60)

    while True:
        print("\nAlegeți operația:")
        print("1. Criptare")
        print("2. Decriptare")
        print("3. Ieșire")

        optiune = input("\nOpțiunea dvs. (1/2/3): ").strip()

        if optiune == '3':
            print("La revedere!")
            break

        if optiune not in ['1', '2']:
            print("Opțiune invalidă! Alegeți 1, 2 sau 3.")
            continue

        # Citește cheia
        while True:
            cheie = input("\nIntroduceți cheia (minim 7 caractere): ").strip()
            valid, mesaj = valideaza_intrare(cheie, "cheie")
            if valid:
                break
            print(f"Eroare: {mesaj}")

        # Citește textul/criptograma
        if optiune == '1':
            while True:
                text = input("\nIntroduceți mesajul de criptat: ").strip()
                valid, mesaj = valideaza_intrare(text, "text")
                if valid:
                    break
                print(f"Eroare: {mesaj}")

            rezultat = cripteaza_playfair(text, cheie)
            print(f"CRIPTOGRAMĂ: {rezultat}")

        else:  # optiune == '2'
            while True:
                text = input("\nIntroduceți criptograma de decriptat: ").strip()
                valid, mesaj = valideaza_intrare(text, "text")
                if valid:
                    break
                print(f"Eroare: {mesaj}")

            rezultat = decripteaza_playfair(text, cheie)
            print(f"MESAJ DECRIPTAT: {rezultat}")
            print("\nNotă: Eliminați manual literele X inserate și adăugați spații conform logicii mesajului.")

        print("\n" + "-" * 60)


if __name__ == "__main__":
    meniu_principal()