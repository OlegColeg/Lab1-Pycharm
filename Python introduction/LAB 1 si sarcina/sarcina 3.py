
# Exercițiul 109: Lista Divizorilor Proprii
def divizori_proprii(n):
    """
    Returnează o listă cu toți divizorii proprii ai lui n
    (numere care împart exact n, excluzând n însuși)
    """
    # Creăm o listă goală pentru divizori
    divizori = []

    # Verificăm fiecare număr de la 1 la n-1
    for i in range(1, n):
        # Dacă i este divizor al lui n, îl adăugăm în listă
        if n % i == 0:
            divizori.append(i)

    # Returnăm lista cu divizori
    return divizori


# Exemplu de utilizare pentru funcția divizori_proprii
def test_divizori_proprii():
    # Cerem utilizatorului să introducă un număr pozitiv
    print("Introduceți un număr întreg pozitiv pentru a găsi divizorii proprii:")
    numar = int(input())

    # Verificăm dacă numărul este pozitiv
    if numar <= 0:
        print("Vă rugăm introduceți un număr întreg pozitiv.")
        return

    # Calculăm divizorii proprii
    div = divizori_proprii(numar)

    # Afișăm rezultatele
    print(f"Divizorii proprii ai lui {numar} sunt: {div}")
    print(f"Suma divizorilor proprii: {sum(div)}")

# Pentru a rula oricare dintre exerciții, eliminați # de la începutul liniei dorite:
# evitare_duplicate()
# negative_zero_pozitive()
# test_divizori_proprii()