"""
LUCRAREA DE LABORATOR NR. 5 - SARCINA 3
DIFFIE-HELLMAN ȘI AES-256
Student: Oală Oleg, Varianta 15
"""

import random
import hashlib

# ================== PARAMETRII DAȚI ==================
print("=" * 70)
print("SARCINA 3 - DIFFIE-HELLMAN ȘI AES-256")
print("=" * 70)
print("\n>>> PARAMETRII DIFFIE-HELLMAN\n")

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

# ================== PASUL 1: GENERAREA NUMERELOR SECRETE ==================
print("\n>>> PASUL 1: GENERAREA NUMERELOR SECRETE\n")

# Alice alege numărul secret a
print("Alice generează numărul secret a (1 < a < p-1)...")
a = random.randint(2, p - 2)
print(f"Secretul lui Alice (a):")
print(f"  Primii 50 caractere: {str(a)[:50]}...")
print(f"  Ultimii 50 caractere: ...{str(a)[-50:]}")
print(f"  Lungime în biți: {a.bit_length()}")

# Bob alege numărul secret b
print("\nBob generează numărul secret b (1 < b < p-1)...")
b = random.randint(2, p - 2)
print(f"Secretul lui Bob (b):")
print(f"  Primii 50 caractere: {str(b)[:50]}...")
print(f"  Ultimii 50 caractere: ...{str(b)[-50:]}")
print(f"  Lungime în biți: {b.bit_length()}")

# Verificări
print(f"\nVerificare: 1 < a < p-1? {1 < a < p - 1} ✓")
print(f"Verificare: 1 < b < p-1? {1 < b < p - 1} ✓")

# ================== PASUL 2: CALCULUL VALORILOR PUBLICE ==================
print("\n>>> PASUL 2: CALCULUL VALORILOR PUBLICE\n")

# Alice calculează A = g^a mod p
print("Alice calculează A = g^a mod p...")
A = pow(g, a, p)
print(f"Valoarea publică a lui Alice (A):")
print(f"  Primii 50 caractere: {str(A)[:50]}...")
print(f"  Ultimii 50 caractere: ...{str(A)[-50:]}")
print(f"  Lungime în biți: {A.bit_length()}")

# Bob calculează B = g^b mod p
print("\nBob calculează B = g^b mod p...")
B = pow(g, b, p)
print(f"Valoarea publică a lui Bob (B):")
print(f"  Primii 50 caractere: {str(B)[:50]}...")
print(f"  Ultimii 50 caractere: ...{str(B)[-50:]}")
print(f"  Lungime în biți: {B.bit_length()}")

print("\n" + "=" * 70)
print("SCHIMBUL DE VALORI PUBLICE")
print("=" * 70)
print("Alice trimite lui Bob: A (valoarea publică)")
print("Bob trimite lui Alice: B (valoarea publică)")
print("\nAceste valori pot fi trimise prin canale nesecurizate!")
print("=" * 70)

# ================== PASUL 3: CALCULUL SECRETULUI COMUN ==================
print("\n>>> PASUL 3: CALCULUL SECRETULUI COMUN\n")

# Alice calculează secretul comun K = B^a mod p
print("Alice calculează secretul comun: K_alice = B^a mod p...")
K_alice = pow(B, a, p)
print(f"Secretul comun calculat de Alice:")
print(f"  Primii 50 caractere: {str(K_alice)[:50]}...")
print(f"  Ultimii 50 caractere: ...{str(K_alice)[-50:]}")
print(f"  Lungime în biți: {K_alice.bit_length()}")

# Bob calculează secretul comun K = A^b mod p
print("\nBob calculează secretul comun: K_bob = A^b mod p...")
K_bob = pow(A, b, p)
print(f"Secretul comun calculat de Bob:")
print(f"  Primii 50 caractere: {str(K_bob)[:50]}...")
print(f"  Ultimii 50 caractere: ...{str(K_bob)[-50:]}")
print(f"  Lungime în biți: {K_bob.bit_length()}")

# Verificăm că ambele părți au obținut același secret
print("\n" + "=" * 70)
print("VERIFICAREA SECRETULUI COMUN")
print("=" * 70)
if K_alice == K_bob:
    print("✓ Cele două valori coincid!")
    print("\nDemonstrație matematică:")
    print("  B^a = (g^b)^a = g^(ba) = g^(ab) = (g^a)^b = A^b")
    print("\nPrin urmare: K_alice = K_bob = g^(ab) mod p")
else:
    print("✗ EROARE: Valorile NU coincid!")
    exit(1)
print("=" * 70)

# Folosim secretul comun
K = K_alice

# ================== PASUL 4: GENERAREA CHEII AES-256 ==================
print("\n>>> PASUL 4: GENERAREA CHEII AES-256\n")

print("Generăm cheia AES-256 din secretul comun...")
print("\nMetoda: Aplicăm funcția de hash SHA-256 pe secretul comun")
print("SHA-256 produce exact 256 biți, perfect pentru AES-256!")

# Convertim secretul comun în bytes
K_bytes = K.to_bytes((K.bit_length() + 7) // 8, byteorder='big')

# Aplicăm SHA-256 pentru a obține o cheie de exact 256 biți
sha256_hash = hashlib.sha256(K_bytes)
key_bytes = sha256_hash.digest()  # 32 bytes = 256 biți

# Convertim cheia în diferite formate pentru vizualizare
key_hex = key_bytes.hex()
key_binary = ''.join(format(byte, '08b') for byte in key_bytes)

print(f"\nCheia AES-256 generată:")
print(f"\n1. Format HEXAZECIMAL (32 bytes = 64 caractere hex):")
print(f"   {key_hex}")

print(f"\n2. Format BINAR (256 biți):")
print(f"   Primii 64 biți:  {key_binary[:64]}")
print(f"   ...")
print(f"   Ultimii 64 biți: {key_binary[-64:]}")

print(f"\n3. Format BYTES (pentru utilizare în AES):")
print(f"   Primii 16 bytes: {key_bytes[:16].hex()}")
print(f"   Ultimii 16 bytes: {key_bytes[16:].hex()}")

print(f"\n4. LUNGIME:")
print(f"   Lungime în biți: {len(key_binary)} biți")
print(f"   Lungime în bytes: {len(key_bytes)} bytes")
print(f"   Lungime hex: {len(key_hex)} caractere")

# Verificăm lungimea
if len(key_bytes) == 32:
    print("\n✓ Verificare: Cheia are exact 256 biți (32 bytes) - perfect pentru AES-256!")
else:
    print(f"\n✗ EROARE: Lungimea cheii este {len(key_bytes) * 8} biți, nu 256!")

# ================== EXPLICAȚIE ȘI UTILIZARE ==================
print("\n" + "=" * 70)
print("EXPLICAȚIE ȘI UTILIZARE")
print("=" * 70)

print("\n📌 Ce am realizat:")
print("   1. Alice și Bob au generat fiecare câte un număr secret (a, b)")
print("   2. Fiecare a calculat o valoare publică (A, B) și a trimis-o celuilalt")
print("   3. Fiecare a calculat secretul comun folosind valoarea primită și secretul propriu")
print("   4. Ambii au obținut ACELAȘI secret comun, fără a-și trimite secretele!")
print("   5. Din secretul comun am generat o cheie AES-256 sigură")

print("\n📌 Securitate:")
print("   • Un atacator care interceptează A și B nu poate calcula secretul comun")
print("   • Ar trebui să rezolve problema logaritmului discret (foarte greu!)")
print("   • Pentru p de 2048 biți, aceasta este practic imposibilă")

print("\n📌 Utilizare:")
print("   • Această cheie AES-256 poate fi folosită pentru criptare simetrică")
print("   • Algoritmul AES cu această cheie poate cripta/decripta mesaje rapid")
print("   • Alice și Bob pot acum comunica securizat folosind AES-256")

print("\n" + "=" * 70)
print("EXEMPLU DE UTILIZARE A CHEII AES-256")
print("=" * 70)

try:
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    from Crypto.Util.Padding import pad, unpad
    
    print("\n✓ Biblioteca PyCryptodome este disponibilă!")
    print("  Demonstrăm criptarea/decriptarea cu AES-256...\n")
    
    # Mesaj de test
    test_message = b"Acesta este un mesaj secret pentru Alice si Bob!"
    print(f"Mesaj original: {test_message.decode()}")
    
    # Generăm un IV (Initialization Vector) aleatoriu
    iv = get_random_bytes(16)  # AES necesită IV de 16 bytes
    
    # Cream cipher-ul AES în modul CBC
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    
    # Criptăm mesajul (cu padding)
    ciphertext = cipher.encrypt(pad(test_message, AES.block_size))
    print(f"\nMesaj criptat (hex): {ciphertext.hex()}")
    
    # Decriptăm mesajul
    decipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    decrypted_message = unpad(decipher.decrypt(ciphertext), AES.block_size)
    print(f"Mesaj decriptat: {decrypted_message.decode()}")
    
    if test_message == decrypted_message:
        print("\n✓✓✓ Criptarea/Decriptarea AES funcționează perfect!")
    
except ImportError:
    print("\n⚠ Biblioteca PyCryptodome nu este instalată.")
    print("  Pentru a testa criptarea AES, instalează cu: pip install pycryptodome")
    print("\n  Totuși, cheia AES-256 a fost generată cu succes și poate fi folosită!")

print("\n" + "=" * 70)
print("ALGORITMUL DIFFIE-HELLMAN ȘI AES-256 FINALIZAT CU SUCCES!")
print("=" * 70)

# ================== REZUMAT FINAL ==================
print("\n" + "=" * 70)
print("REZUMAT FINAL")
print("=" * 70)
print("\n✓ Parametrii publici: p (2048 biți), g = 2")
print(f"✓ Secretul lui Alice (a): {a.bit_length()} biți")
print(f"✓ Secretul lui Bob (b): {b.bit_length()} biți")
print(f"✓ Valoarea publică A: {A.bit_length()} biți")
print(f"✓ Valoarea publică B: {B.bit_length()} biți")
print(f"✓ Secret comun: {K.bit_length()} biți")
print(f"✓ Cheie AES-256: {len(key_bytes) * 8} biți")
print(f"\n✓ Cheia AES-256 (hex): {key_hex}")
print("\n" + "=" * 70)
