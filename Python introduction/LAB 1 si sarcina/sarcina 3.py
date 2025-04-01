
def divizori_proprii(n):

    divizori = []

    # Verificăm fiecare număr de la 1 la n-1
    for i in range(1, n):
        # Dacă i este divizor al lui n, îl adăugăm în listă
        if n % i == 0:
            divizori.append(i)

    # Returnăm lista cu divizori
    return divizori

print("Introduceți un număr întreg pozitiv pentru a găsi divizorii proprii:")
try:
    numar = int(input())

    if numar <= 0:
        print("Vă rugăm introduceți un număr întreg pozitiv.")
    else:
        # Calculăm divizorii proprii
        div = divizori_proprii(numar)

        # Afișăm rezultatele
        print(f"Divizorii proprii ai lui {numar} sunt: {div}")
        print(f"Suma divizorilor proprii: {sum(div)}")
except:
    print("Input invalid. Vă rugăm introduceți un număr întreg.")