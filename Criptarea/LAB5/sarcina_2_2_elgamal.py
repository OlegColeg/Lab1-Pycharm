"""
LUCRAREA DE LABORATOR NR. 5 - SARCINA 2.2
ALGORITMUL ELGAMAL
Student: Oală Oleg, Varianta 15
"""

import random

def string_to_number(text):
    """Convertește text în număr (UTF-8 -> HEX -> DEC)"""
    text_bytes = text.encode('utf-8')
    hex_string = text_bytes.hex()
    decimal = int(hex_string, 16)
    return hex_string, decimal

def number_to_string(num):
    """Convertește număr înapoi în text"""
    hex_string = format(num, 'x')
    if len(hex_string) % 2 != 0:
        hex_string = '0' + hex_string
    text_bytes = bytes.fromhex(hex_string)
    text = text_bytes.decode('utf-8')
    return text

# ================== PARAMETRII DAȚI ==================
print("=" * 70)
print("SARCINA 2.2 - ALGORITMUL ELGAMAL")
print("=" * 70)
print("\n>>> PARAMETRII ELGAMAL\n")

# Parametrii publici dați în sarcină
p = int("3231700607131100730015351347782516336248805713348907517458843413926"
        "9806834136210002792056362640164685458556357935330816928829023080573"
        "4726252735547424612457410262025279165729728627063003252634282131457"
        "6693141422365422094111134862999165747826803423055308634905063555771"
        "2219187890332729569696129743856241741236237225197346402691855797767"
        "9768230146253979330580152268587307611975324364758554607150438968449"
        "4036613049769781285429595865959756705128385213278446852292550456827"
        "2879113720098931873959143374175837826000278034973198552060607533234"
        "12260325468408812003110590748428100399496695611969695624862903233807283912703")

g = 2

print(f"p (număr prim, 2048 biți):")
print(f"  Primii 50 caractere: {str(p)[:50]}...")
print(f"  Ultimii 50 caractere: ...{str(p)[-50:]}")
print(f"  Lungime în biți: {p.bit_length()}")
print(f"\nGenerator g = {g}")

# ================== PASUL 1: MESAJUL ORIGINAL ==================
print("\n>>> PASUL 1: MESAJUL ORIGINAL\n")

message = "Oală Oleg"
print(f"Text: '{message}'")

# Convertim mesajul în număr
hex_message, m = string_to_number(message)
print(f"\nReprezentare hexazecimală: {hex_message}")
print(f"Reprezentare zecimală (m): {m}")
print(f"Lungime m în biți: {m.bit_length()}")

# Verificăm că mesajul este mai mic decât p
if m >= p:
    print("\nERRORE: Mesajul este prea lung pentru acest modul!")
    exit(1)
print(f"\nVerificare: m < p? {m < p} ✓")

# ================== PASUL 2: GENERAREA CHEILOR ==================
print("\n>>> PASUL 2: GENERAREA CHEILOR\n")

# Generăm cheia privată x (numită 'a' în teorie)
# x trebuie să fie în intervalul [2, p-2]
print("Generăm cheia privată x (1 < x < p-1)...")
x = random.randint(2, p - 2)
print(f"Cheia privată x:")
print(f"  Primii 50 caractere: {str(x)[:50]}...")
print(f"  Ultimii 50 caractere: ...{str(x)[-50:]}")
print(f"  Lungime în biți: {x.bit_length()}")

# Calculăm cheia publică y = g^x mod p (numită 'h' în teorie)
print("\nCalculăm cheia publică y = g^x mod p...")
y = pow(g, x, p)
print(f"Cheia publică y:")
print(f"  Primii 50 caractere: {str(y)[:50]}...")
print(f"  Ultimii 50 caractere: ...{str(y)[-50:]}")
print(f"  Lungime în biți: {y.bit_length()}")

print("\n" + "=" * 70)
print("CHEILE GENERATE:")
print("Cheia publică: (p, g, y)")
print(f"  p = {str(p)[:50]}...{str(p)[-50:]}")
print(f"  g = {g}")
print(f"  y = {str(y)[:50]}...{str(y)[-50:]}")
print("\nCheia privată: x")
print(f"  x = {str(x)[:50]}...{str(x)[-50:]}")
print("=" * 70)

# ================== PASUL 3: CRIPTAREA ==================
print("\n>>> PASUL 3: CRIPTAREA\n")

# Alegem un număr aleatoriu k pentru criptare
print("Generăm numărul aleatoriu k (1 < k < p-1)...")
k = random.randint(2, p - 2)
print(f"Valoarea aleatoare k:")
print(f"  Primii 50 caractere: {str(k)[:50]}...")
print(f"  Ultimii 50 caractere: ...{str(k)[-50:]}")

# Calculăm c1 = g^k mod p
print("\nCalculăm c1 = g^k mod p...")
c1 = pow(g, k, p)
print(f"c1:")
print(f"  Primii 50 caractere: {str(c1)[:50]}...")
print(f"  Ultimii 50 caractere: ...{str(c1)[-50:]}")

# Calculăm c2 = m * y^k mod p
print("\nCalculăm c2 = m * y^k mod p...")
c2 = (m * pow(y, k, p)) % p
print(f"c2:")
print(f"  Primii 50 caractere: {str(c2)[:50]}...")
print(f"  Ultimii 50 caractere: ...{str(c2)[-50:]}")

print("\n" + "=" * 70)
print("MESAJUL CRIPTAT: (c1, c2)")
print(f"  c1 = {str(c1)[:50]}...{str(c1)[-50:]}")
print(f"  c2 = {str(c2)[:50]}...{str(c2)[-50:]}")
print("=" * 70)

# ================== PASUL 4: DECRIPTAREA ==================
print("\n>>> PASUL 4: DECRIPTAREA\n")

# Calculăm s = c1^x mod p
print("Calculăm s = c1^x mod p...")
s = pow(c1, x, p)
print(f"Valoarea s = c1^x mod p:")
print(f"  Primii 50 caractere: {str(s)[:50]}...")
print(f"  Ultimii 50 caractere: ...{str(s)[-50:]}")

# Calculăm inversul modular al lui s
print("\nCalculăm inversul modular al lui s...")
inverse_s = pow(s, -1, p)  # Python 3.8+ suportă pow(a, -1, m) pentru invers modular
print(f"Inversul modular al lui s:")
print(f"  Primii 50 caractere: {str(inverse_s)[:50]}...")
print(f"  Ultimii 50 caractere: ...{str(inverse_s)[-50:]}")

# Calculăm m_decrypted = c2 * inverse_s mod p
print("\nCalculăm m_decrypted = c2 * inverse_s mod p...")
m_decrypted = (c2 * inverse_s) % p
print(f"Mesajul decriptat (număr): {m_decrypted}")

# ================== PASUL 5: VERIFICAREA ==================
print("\n>>> PASUL 5: VERIFICAREA\n")

print(f"Numărul inițial (m):    {m}")
print(f"Numărul decriptat:      {m_decrypted}")

if m == m_decrypted:
    print("\n✓ Cele două numere coincid!")
else:
    print("\n✗ EROARE: Numerele NU coincid!")

# ================== PASUL 6: RECONSTITUIREA TEXTULUI ==================
print("\n>>> PASUL 6: RECONSTITUIREA TEXTULUI\n")

# Convertim numărul înapoi în text
hex_result = format(m_decrypted, 'x')
print(f"Reprezentare hexazecimală decriptată: {hex_result}")

# Asigurăm lungimea pară
if len(hex_result) % 2 != 0:
    hex_result = '0' + hex_result
    print(f"Hex ajustat (adăugat 0): {hex_result}")

# Convertim hex în text
text_result = number_to_string(m_decrypted)
print(f"\nText reconstituit: '{text_result}'")

# Verificare finală
if text_result == message:
    print(f"\n{'=' * 70}")
    print("✓✓✓ SUCCES! Textul reconstituit coincide cu originalul!")
    print(f"    Original:      '{message}'")
    print(f"    Reconstituit:  '{text_result}'")
    print(f"{'=' * 70}")
else:
    print("\n✗ EROARE: Textul reconstituit NU coincide cu originalul!")
    print(f"  Original:      '{message}'")
    print(f"  Reconstituit:  '{text_result}'")

print("\n" + "=" * 70)
print("ALGORITMUL ELGAMAL FINALIZAT CU SUCCES!")
print("=" * 70)

# ================== EXPLICAȚIE MATEMATICĂ ==================
print("\n" + "=" * 70)
print("EXPLICAȚIE MATEMATICĂ")
print("=" * 70)
print("\nDe ce funcționează decriptarea?")
print("\nÎn criptare, am calculat:")
print("  c1 = g^k mod p")
print("  c2 = m * y^k mod p = m * (g^x)^k mod p = m * g^(xk) mod p")
print("\nÎn decriptare, am calculat:")
print("  s = c1^x mod p = (g^k)^x mod p = g^(kx) mod p")
print("  inverse_s = s^(-1) mod p = (g^(kx))^(-1) mod p")
print("  m_decrypted = c2 * inverse_s mod p")
print("              = (m * g^(xk)) * (g^(kx))^(-1) mod p")
print("              = m * g^(xk) * g^(-xk) mod p")
print("              = m * g^0 mod p")
print("              = m mod p")
print("              = m (deoarece m < p)")
print("\nAstfel, mesajul original m este recuperat cu succes!")
print("=" * 70)
