import string
from collections import Counter
import sys


class FrequencyAnalysisTool:
    def __init__(self):
        # Frecvențele în limba engleză
        self.english_freq = {
            'E': 12.7, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
            'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
            'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.01, 'Y': 1.97,
            'P': 1.93, 'B': 1.49, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
            'Q': 0.09, 'Z': 0.07
        }
        self.substitutions = {}
        self.cipher_text = ""

    def calculate_frequency(self, text):
        """Calculează frecvența literelor"""
        letters = ''.join(c.upper() for c in text if c.isalpha())
        if not letters:
            return {}

        counter = Counter(letters)
        total = len(letters)

        freq = {letter: (count / total * 100) for letter, count in counter.items()}
        return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

    def display_frequency(self, freq):
        """Afișează frecvențele în terminal"""
        print("\n" + "=" * 70)
        print("ANALIZA FRECVENȚELOR".center(70))
        print("=" * 70)

        if not freq:
            print("Nu există date pentru analiză!")
            return

        print(f"\n{'Litera':<10} {'Frecvență Text':<20} {'Frecvență EN':<20} {'Diferență':<15}")
        print("-" * 70)

        for letter in sorted(freq.keys(), key=lambda x: freq[x], reverse=True):
            cipher_f = freq[letter]
            english_f = self.english_freq.get(letter, 0)
            diff = abs(cipher_f - english_f)

            bar_cipher = '█' * int(cipher_f / 2)
            print(f"{letter:<10} {cipher_f:>6.2f}% {bar_cipher:<20} {english_f:>6.2f}%    Δ{diff:>5.2f}%")

    def display_top_comparison(self, freq):
        """Compară top literele din text cu cele din engleză"""
        print("\n" + "=" * 70)
        print("TOP 10 LITERE - COMPARAȚIE".center(70))
        print("=" * 70)

        cipher_top = list(freq.keys())[:10]
        english_top = [item[0] for item in sorted(self.english_freq.items(),
                                                  key=lambda x: x[1], reverse=True)][:10]

        print(f"\n{'Poziție':<12} {'Text Criptat':<25} {'Limba Engleză':<25}")
        print("-" * 70)

        for i in range(10):
            c_letter = cipher_top[i] if i < len(cipher_top) else '-'
            c_freq = freq.get(c_letter, 0) if c_letter != '-' else 0
            e_letter = english_top[i]
            e_freq = self.english_freq[e_letter]

            print(f"{i + 1:<12} {c_letter} ({c_freq:>5.2f}%){'':>14} {e_letter} ({e_freq:>5.2f}%)")

    def decrypt_text(self):
        """Decriptează textul cu substituțiile curente"""
        if not self.cipher_text:
            return ""

        result = []
        for char in self.cipher_text:
            if char.isupper():
                result.append(self.substitutions.get(char, char))
            elif char.islower():
                upper = char.upper()
                subst = self.substitutions.get(upper, upper)
                result.append(subst.lower())
            else:
                result.append(char)

        return ''.join(result)

    def display_texts(self):
        """Afișează textul criptat și decriptat"""
        print("\n" + "=" * 70)
        print("TEXT CRIPTAT".center(70))
        print("=" * 70)
        print(self.cipher_text)

        decrypted = self.decrypt_text()
        print("\n" + "=" * 70)
        print("TEXT DECRIPTAT".center(70))
        print("=" * 70)
        print(decrypted)

    def display_substitutions(self):
        """Afișează substituțiile curente"""
        print("\n" + "=" * 70)
        print("SUBSTITUȚII CURENTE".center(70))
        print("=" * 70)

        if not self.substitutions:
            print("Nu există substituții definite.")
            return

        sorted_subs = sorted(self.substitutions.items())
        for i in range(0, len(sorted_subs), 6):
            row = sorted_subs[i:i + 6]
            print("  ".join([f"{k} → {v}" for k, v in row]))

    def auto_suggest(self, top_n=5):
        """Sugerează automat substituții pentru top N litere"""
        freq = self.calculate_frequency(self.cipher_text)

        if not freq:
            print("Nu există text pentru analiză!")
            return

        cipher_top = list(freq.keys())[:top_n]
        english_top = [item[0] for item in sorted(self.english_freq.items(),
                                                  key=lambda x: x[1], reverse=True)][:top_n]

        for i, cipher_letter in enumerate(cipher_top):
            english_letter = english_top[i]
            self.substitutions[cipher_letter] = english_letter

        print(f"\nS-au aplicat {len(cipher_top)} substituții automate:")
        for i, cipher_letter in enumerate(cipher_top):
            print(f"  {cipher_letter} → {english_top[i]}")

    def manual_substitution(self):
        """Permite utilizatorului să introducă substituții manual"""
        print("\nIntroduceți substituții (format: C=P, unde C=criptat, P=plain)")
        print("Exemple: A=E, B=T, C=A")
        print("Pentru a termina, apăsați Enter fără a introduce nimic.")

        while True:
            sub = input("\nSubstituție (sau Enter pentru a termina): ").strip().upper()

            if not sub:
                break

            if '=' not in sub or len(sub) != 3:
                print("Format invalid! Folosiți formatul: C=P")
                continue

            cipher_letter, plain_letter = sub.split('=')

            if cipher_letter not in string.ascii_uppercase or plain_letter not in string.ascii_uppercase:
                print("Ambele litere trebuie să fie din alfabetul englez!")
                continue

            self.substitutions[cipher_letter] = plain_letter
            print(f"✓ Substituție adăugată: {cipher_letter} → {plain_letter}")

    def show_tips(self):
        """Afișează sfaturi pentru criptanaliză"""
        print("\n" + "=" * 70)
        print("SFATURI PENTRU CRIPTANALIZĂ".center(70))
        print("=" * 70)
        print("""
- Cea mai frecventă literă în engleză: E (12.7%), urmată de T (9.06%)
- Cuvinte de o literă: A sau I
- Cuvinte frecvente de 3 litere: THE, AND, FOR
- Digrame frecvente: TH, HE, AN, IN, ER, ON, RE
- Trigrame frecvente: THE, AND, THA, ENT, ION
- Litere duble comune: SS, EE, TT, OO, FF
- Articolul definit THE este cel mai frecvent cuvânt de 3 litere
- Căutați pattern-uri repetitive în text
        """)

    def load_example(self):
        """Încarcă un exemplu de text criptat"""
        self.cipher_text = """NG T OTF gvtisf 4,000 fvtip tjn, xg t wnrg htssvo Zvgvw Lqdcdaniovixgj wqv wqxg ixaang nc wqv
Gxsv, t ztpwvi phixav plvwhqvo ndw wqvqxvinjsfuqp wqtw wnso wqv pwnif nc qxp snio'p sxcv—
tgo xg pn onxgj qvnuvgvo wqv ivhniovo qxpwnif nc hifuwnsnjf."""
        print("✓ Exemplul a fost încărcat!")

    def clear_substitutions(self):
        """Șterge toate substituțiile"""
        self.substitutions.clear()
        print("✓ Toate substituțiile au fost șterse!")

    def run(self):
        """Rulează aplicația în mod interactiv"""
        print("\n" + "=" * 70)
        print("ANALIZĂ FRECVENȚE - CRIPTANALIZĂ MONOALFABETICĂ".center(70))
        print("=" * 70)

        while True:
            print("\n" + "-" * 70)
            print("MENIU PRINCIPAL")
            print("-" * 70)
            print("1. Introduceți text criptat")
            print("2. Încărcați exemplul V1")
            print("3. Analizați frecvențele")
            print("4. Afișați comparație top litere")
            print("5. Sugestii automate (top 5)")
            print("6. Adăugați substituții manual")
            print("7. Afișați substituțiile curente")
            print("8. Afișați textele (criptat + decriptat)")
            print("9. Ștergeți substituțiile")
            print("10. Afișați sfaturi")
            print("0. Ieșire")

            choice = input("\nAlegeți o opțiune: ").strip()

            if choice == '1':
                print("\nIntroduceți textul criptat (apăsați Enter de două ori pentru a termina):")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        if lines and lines[-1] == "":
                            break
                        lines.append(line)
                    else:
                        lines.append(line)

                self.cipher_text = '\n'.join(lines[:-1] if lines else [])
                print("✓ Text încărcat!")

            elif choice == '2':
                self.load_example()

            elif choice == '3':
                if not self.cipher_text:
                    print("⚠ Introduceți mai întâi un text criptat!")
                    continue
                freq = self.calculate_frequency(self.cipher_text)
                self.display_frequency(freq)

            elif choice == '4':
                if not self.cipher_text:
                    print("⚠ Introduceți mai întâi un text criptat!")
                    continue
                freq = self.calculate_frequency(self.cipher_text)
                self.display_top_comparison(freq)

            elif choice == '5':
                self.auto_suggest()

            elif choice == '6':
                self.manual_substitution()

            elif choice == '7':
                self.display_substitutions()

            elif choice == '8':
                if not self.cipher_text:
                    print("⚠ Introduceți mai întâi un text criptat!")
                    continue
                self.display_texts()

            elif choice == '9':
                self.clear_substitutions()

            elif choice == '10':
                self.show_tips()

            elif choice == '0':
                print("\nLa revedere!")
                sys.exit(0)

            else:
                print("⚠ Opțiune invalidă! Alegeți un număr din meniu.")


if __name__ == "__main__":
    tool = FrequencyAnalysisTool()
    tool.run()
#PENTRU VARIANTA 15 W→T, Q→H, V→E, X→I, G→N, Z→M, U→P, T→A, N→O, P→S, I→R, H→C, F→Y, O→D, S→L, J→G, K→V, Y→X, A→B, C→F, R→W, L→K, E→J, D→U, M→Z, B→Q