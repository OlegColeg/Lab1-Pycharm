# Exercițiul 108: Negative, Zero și Pozitive
def negative_zero_pozitive():
    # Creăm trei liste goale pentru a stoca numerele
    negative = []
    zerouri = []
    pozitive = []

    # Cerem utilizatorului să introducă numere întregi
    print("Introduceți numere întregi (linie goală pentru a termina):")

    # Continuăm să cerem numere până când primim o linie goală
    while True:
        linie = input()

        # Verificăm dacă linia este goală pentru a ieși din buclă
        if linie == "":
            break

        # Încercăm să convertim intrarea în număr întreg
        try:
            numar = int(linie)

            # Verificăm dacă numărul este negativ, zero sau pozitiv
            if numar < 0:
                negative.append(numar)
            elif numar == 0:
                zerouri.append(numar)
            else:
                pozitive.append(numar)
        except:
            print("Input invalid. Vă rugăm introduceți un număr întreg.")

    # Afișăm rezultatele
    print("Numerele negative:", negative)
    print("Zerouri:", zerouri)
    print("Numerele pozitive:", pozitive)

