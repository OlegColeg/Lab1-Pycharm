"""
LUCRAREA DE LABORATOR NR. 5 - SARCINA 2.1
ALGORITMUL RSA
Student: Oală Oleg, Varianta 15
"""

import random
from math import gcd

def is_prime(n, k=5):
    """Test de primalitate Miller-Rabin"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Scriem n-1 ca 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Testăm de k ori
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    
    return True

def generate_prime(bits):
    """Generează un număr prim de 'bits' biți"""
    while True:
        # Generăm un număr aleatoriu de bits biți
        num = random.getrandbits(bits)
        # Ne asigurăm că are exact bits biți (primul bit = 1)
        num |= (1 << bits - 1) | 1
        
        if is_prime(num):
            return num

def extended_gcd(a, b):
    """Algoritmul extins al lui Euclid"""
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(e, phi):
    """Calculează inversul modular al lui e modulo phi"""
    gcd_val, x, _ = extended_gcd(e, phi)
    if gcd_val != 1:
        raise Exception("Inversul modular nu există")
    return (x % phi + phi) % phi

def string_to_number(text):
    """Convertește text în număr (UTF-8 -> HEX -> DEC)"""
    # Convertim textul în bytes folosind UTF-8
    text_bytes = text.encode('utf-8')
    # Convertim bytes în hexazecimal
    hex_string = text_bytes.hex()
    # Convertim hexazecimal în zecimal
    decimal = int(hex_string, 16)
    return hex_string, decimal

def number_to_string(num):
    """Convertește număr înapoi în text"""
    # Convertim numărul în hexazecimal
    hex_string = format(num, 'x')
    # Dacă lungimea este impară, adăugăm un 0 la început
    if len(hex_string) % 2 != 0:
        hex_string = '0' + hex_string
    
    # Convertim hexazecimal în bytes
    text_bytes = bytes.fromhex(hex_string)
    # Convertim bytes în text folosind UTF-8
    text = text_bytes.decode('utf-8')
    return text

# ================== PASUL 1: GENERAREA CHEILOR ==================
print("=" * 70)
print("SARCINA 2.1 - ALGORITMUL RSA")
print("=" * 70)
print("\n>>> PASUL 1: GENERAREA CHEILOR RSA\n")

# Generăm două numere prime mari p și q (fiecare 1024 biți)
print("Generăm numărul prim p (1024 biți)...")
p = generate_prime(1024)
print(f"p generat cu succes!")
print(f"Primii și ultimii 50 de caractere: {str(p)[:50]}...{str(p)[-50:]}")
print(f"Lungime p în biți: {p.bit_length()}")

print("\nGenerăm numărul prim q (1024 biți)...")
q = generate_prime(1024)
print(f"q generat cu succes!")
print(f"Primii și ultimii 50 de caractere: {str(q)[:50]}...{str(q)[-50:]}")
print(f"Lungime q în biți: {q.bit_length()}")

# Verificăm că p și q sunt diferite
if p == q:
    print("\nATENȚIE: p și q sunt egale! Regenerăm q...")
    q = generate_prime(1024)

# Calculăm n = p * q
n = p * q
print(f"\nCalculăm n = p * q")
print(f"Lungime n în biți: {n.bit_length()}")
print(f"Primii și ultimii 50 de caractere ale lui n: {str(n)[:50]}...{str(n)[-50:]}")

# Calculăm funcția Euler φ(n) = (p-1)(q-1)
phi = (p - 1) * (q - 1)
print(f"\nCalculăm φ(n) = (p-1) * (q-1)")
print(f"φ(n) calculat cu succes!")

# Alegem exponentul public e = 65537 (standard)
e = 65537
print(f"\nExponentul public e = {e}")

# Verificăm că gcd(e, φ(n)) = 1
if gcd(e, phi) != 1:
    print("EROARE: e și φ(n) nu sunt coprime!")
    exit(1)
print(f"Verificare: gcd(e, φ(n)) = {gcd(e, phi)} ✓")

# Calculăm exponentul privat d = e^(-1) mod φ(n)
print("\nCalculăm exponentul privat d = e^(-1) mod φ(n)...")
d = mod_inverse(e, phi)
print(f"d calculat cu succes!")
print(f"Primii și ultimii 50 de caractere ale lui d: {str(d)[:50]}...{str(d)[-50:]}")

print("\n" + "=" * 70)
print("CHEILE GENERATE:")
print("Cheia publică: (e, n)")
print(f"  e = {e}")
print(f"  n = {str(n)[:50]}...{str(n)[-50:]}")
print("\nCheia privată: (d, n)")
print(f"  d = {str(d)[:50]}...{str(d)[-50:]}")
print(f"  n = {str(n)[:50]}...{str(n)[-50:]}")
print("=" * 70)

# ================== PASUL 2: TRANSFORMAREA MESAJULUI ==================
print("\n>>> PASUL 2: TRANSFORMAREA MESAJULUI\n")

message = "Oală Oleg"
print(f"Mesajul original: '{message}'")

# Convertim mesajul în număr
hex_message, decimal_message = string_to_number(message)
print(f"\nReprezentare hexazecimală: {hex_message}")
print(f"Reprezentare zecimală: {decimal_message}")
print(f"Lungime mesaj în biți: {decimal_message.bit_length()}")

# Verificăm că mesajul este mai mic decât n
if decimal_message >= n:
    print("\nERRORE: Mesajul este prea lung pentru acest modul RSA!")
    exit(1)
print(f"\nVerificare: mesaj < n? {decimal_message < n} ✓")

# ================== PASUL 3: CRIPTAREA ==================
print("\n>>> PASUL 3: CRIPTAREA\n")

print("Calculăm c = m^e mod n...")
cipher = pow(decimal_message, e, n)
print(f"Mesajul criptat (c):")
print(f"  Primii 50 caractere: {str(cipher)[:50]}...")
print(f"  Ultimii 50 caractere: ...{str(cipher)[-50:]}")
print(f"  Lungime în biți: {cipher.bit_length()}")

# ================== PASUL 4: DECRIPTAREA ==================
print("\n>>> PASUL 4: DECRIPTAREA\n")

print("Calculăm m = c^d mod n...")
decrypted = pow(cipher, d, n)
print(f"Mesajul decriptat (număr): {decrypted}")

# Verificăm că mesajul decriptat este egal cu originalul
if decrypted == decimal_message:
    print("✓ Verificare: mesajul decriptat coincide cu originalul!")
else:
    print("✗ EROARE: mesajul decriptat NU coincide cu originalul!")

# ================== PASUL 5: TRANSFORMAREA INVERSĂ ==================
print("\n>>> PASUL 5: TRANSFORMAREA INVERSĂ\n")

# Convertim numărul înapoi în text
final_message = number_to_string(decrypted)
print(f"Hexazecimal decriptat: {format(decrypted, 'x')}")
print(f"Mesaj reconstituit: '{final_message}'")

# Verificare finală
if final_message == message:
    print(f"\n{'=' * 70}")
    print("✓✓✓ SUCCES! Mesajul reconstituit coincide cu originalul!")
    print(f"    Original:      '{message}'")
    print(f"    Reconstituit:  '{final_message}'")
    print(f"{'=' * 70}")
else:
    print("\n✗ EROARE: Mesajul reconstituit NU coincide cu originalul!")
    print(f"  Original:      '{message}'")
    print(f"  Reconstituit:  '{final_message}'")

print("\n" + "=" * 70)
print("ALGORITMUL RSA FINALIZAT CU SUCCES!")
print("=" * 70)
