
negative = []
zerouri = []
pozitive = []

print("Introduceți numere întregi (linie goală pentru a termina):")
while True:
    linie = input()
    if linie == "":
        break

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

print("Numerele negative:", negative)
print("Zerouri:", zerouri)
print("Numerele pozitive:", pozitive)