# Exercițiul 107: Evitarea Duplicatelor
def evitare_duplicate():
    # Creăm o listă goală pentru cuvintele unice
    cuvinte_unice = []

    # Cerem utilizatorului să introducă cuvinte
    print("Introduceți cuvinte (linie goală pentru a termina):")

    # Continuăm să cerem cuvinte până când primim o linie goală
    while True:
        cuvant = input()

        # Verificăm dacă linia este goală pentru a ieși din buclă
        if cuvant == "":
            break

        # Adăugăm cuvântul doar dacă nu există deja în listă
        if cuvant not in cuvinte_unice:
            cuvinte_unice.append(cuvant)

    # Afișăm toate cuvintele unice
    print("Cuvintele unice în ordine sunt:")
    for cuvant in cuvinte_unice:
        print(cuvant)


