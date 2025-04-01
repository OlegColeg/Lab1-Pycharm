
cuvinte_unice = []

print("Introduceți cuvinte (linie goală pentru a termina):")

while True:
    cuvant = input()

    if cuvant == "":
        break

    if cuvant not in cuvinte_unice:
        cuvinte_unice.append(cuvant)

print("Cuvintele unice în ordine sunt:")
for cuvant in cuvinte_unice:
    print(cuvant)