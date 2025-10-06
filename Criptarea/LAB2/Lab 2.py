import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib

matplotlib.use('TkAgg')  # Important pentru macOS
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import Counter
import string


class FrequencyAnalysisTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Analiză Frecvențe - Criptanaliză Monoalfabetică")

        # Dimensiuni optimizate pentru Mac
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = min(1400, screen_width - 100)
        window_height = min(900, screen_height - 100)

        self.root.geometry(f"{window_width}x{window_height}")
        self.root.configure(bg='#f0f0f0')

        # Frecvențele în limba engleză (din document)
        self.english_freq = {
            'E': 12.7, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
            'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
            'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.01, 'Y': 1.97,
            'P': 1.93, 'B': 1.49, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
            'Q': 0.09, 'Z': 0.07
        }

        self.substitutions = {}
        self.create_widgets()

    def create_widgets(self):
        # Canvas principal cu scroll
        main_canvas = tk.Canvas(self.root, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)

        main_frame = tk.Frame(main_canvas, bg='#f0f0f0', padx=10, pady=10)

        main_frame.bind("<Configure>",
                        lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))

        main_canvas.create_window((0, 0), window=main_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Titlu
        title_label = tk.Label(main_frame, text="Analiză Frecvențe - Criptanaliză",
                               font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)

        # Frame pentru texte
        text_frame = tk.Frame(main_frame, bg='#f0f0f0')
        text_frame.pack(fill='both', expand=True, pady=5)

        # Text criptat
        cipher_frame = tk.Frame(text_frame, bg='#f0f0f0')
        cipher_frame.pack(side='left', fill='both', expand=True, padx=5)

        tk.Label(cipher_frame, text="Text Criptat:", font=('Arial', 12, 'bold'),
                 bg='#f0f0f0').pack(anchor='w')

        self.cipher_text = scrolledtext.ScrolledText(cipher_frame, width=50, height=12,
                                                     font=('Courier', 10), wrap=tk.WORD,
                                                     bg='white')
        self.cipher_text.pack(fill='both', expand=True, pady=5)
        self.cipher_text.bind('<KeyRelease>', self.on_text_change)

        # Text decriptat
        plain_frame = tk.Frame(text_frame, bg='#f0f0f0')
        plain_frame.pack(side='left', fill='both', expand=True, padx=5)

        tk.Label(plain_frame, text="Text Decriptat:", font=('Arial', 12, 'bold'),
                 bg='#f0f0f0').pack(anchor='w')

        self.plain_text = scrolledtext.ScrolledText(plain_frame, width=50, height=12,
                                                    font=('Courier', 10), wrap=tk.WORD,
                                                    bg='#fffacd', state='disabled')
        self.plain_text.pack(fill='both', expand=True, pady=5)

        # Butoane
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(pady=10)

        btn_style = {'font': ('Arial', 10), 'padx': 10, 'pady': 5}

        tk.Button(button_frame, text="Analizează Frecvențe",
                  command=self.analyze_frequency, bg='#4CAF50', fg='white',
                  **btn_style).pack(side='left', padx=3)
        tk.Button(button_frame, text="Sugestii Auto (Top 5)",
                  command=self.auto_suggest, bg='#2196F3', fg='white',
                  **btn_style).pack(side='left', padx=3)
        tk.Button(button_frame, text="Șterge Substituții",
                  command=self.clear_substitutions, bg='#f44336', fg='white',
                  **btn_style).pack(side='left', padx=3)
        tk.Button(button_frame, text="Exemplu V1",
                  command=self.load_example, bg='#FF9800', fg='white',
                  **btn_style).pack(side='left', padx=3)

        # Frame pentru grafic
        self.graph_frame = tk.LabelFrame(main_frame, text="Grafic Frecvențe",
                                         font=('Arial', 11, 'bold'),
                                         bg='white', padx=10, pady=10)
        self.graph_frame.pack(fill='both', expand=True, pady=10)

        # Frame pentru substituții
        sub_outer_frame = tk.LabelFrame(main_frame, text="Substituții (Criptat → Clar)",
                                        font=('Arial', 11, 'bold'),
                                        bg='white', padx=10, pady=10)
        sub_outer_frame.pack(fill='x', pady=10)

        # Grid pentru substituții (fără scroll intern)
        self.sub_frame = tk.Frame(sub_outer_frame, bg='white')
        self.sub_frame.pack(fill='x')

        self.sub_entries = {}
        self.create_substitution_entries()

        # Sfaturi
        tips_frame = tk.LabelFrame(main_frame, text="Sfaturi",
                                   font=('Arial', 11, 'bold'),
                                   bg='#e3f2fd', padx=10, pady=10)
        tips_frame.pack(fill='x', pady=10)

        tips_text = """• Cea mai frecventă literă în engleză: E (12.7%), urmată de T (9.06%)
• Cuvinte de o literă: A sau I
• Cuvinte frecvente de 3 litere: THE, AND, FOR
• Digrame frecvente: TH, HE, AN, IN, ER, ON, RE
• Trigrame frecvente: THE, AND, THA, ENT, ION
• Litere duble comune: SS, EE, TT, OO, FF"""

        tk.Label(tips_frame, text=tips_text, justify='left',
                 font=('Arial', 9), bg='#e3f2fd').pack(anchor='w')

    def create_substitution_entries(self):
        """Creează câmpurile pentru substituții"""
        letters = string.ascii_uppercase

        for i, letter in enumerate(letters):
            row = i // 6
            col = i % 6

            frame = tk.Frame(self.sub_frame, bg='white')
            frame.grid(row=row, column=col, padx=8, pady=5, sticky='w')

            tk.Label(frame, text=f"{letter} →", font=('Courier', 11, 'bold'),
                     bg='white').pack(side='left')

            entry = tk.Entry(frame, width=3, font=('Courier', 11), justify='center')
            entry.pack(side='left', padx=3)
            entry.bind('<KeyRelease>', lambda e, l=letter: self.on_substitution_change(l))

            self.sub_entries[letter] = entry

            freq_label = tk.Label(frame, text="0%", font=('Arial', 8),
                                  fg='gray', bg='white')
            freq_label.pack(side='left', padx=3)
            self.sub_entries[f"{letter}_freq"] = freq_label

    def calculate_frequency(self, text):
        """Calculează frecvența literelor"""
        letters = ''.join(c.upper() for c in text if c.isalpha())
        if not letters:
            return {}

        counter = Counter(letters)
        total = len(letters)

        freq = {letter: (count / total * 100) for letter, count in counter.items()}
        return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

    def on_text_change(self, event=None):
        """Handler când se schimbă textul criptat"""
        self.update_decrypted_text()

    def on_substitution_change(self, letter):
        """Handler când se schimbă o substituție"""
        entry = self.sub_entries[letter]
        value = entry.get().upper()

        if len(value) > 1:
            entry.delete(0, tk.END)
            entry.insert(0, value[-1])
            value = value[-1]

        if value and value in string.ascii_uppercase:
            self.substitutions[letter] = value
        elif letter in self.substitutions:
            del self.substitutions[letter]

        self.update_decrypted_text()

    def update_decrypted_text(self):
        """Actualizează textul decriptat"""
        cipher = self.cipher_text.get("1.0", tk.END)

        result = []
        for char in cipher:
            if char.isupper():
                result.append(self.substitutions.get(char, char))
            elif char.islower():
                upper = char.upper()
                subst = self.substitutions.get(upper, upper)
                result.append(subst.lower())
            else:
                result.append(char)

        self.plain_text.config(state='normal')
        self.plain_text.delete("1.0", tk.END)
        self.plain_text.insert("1.0", ''.join(result))
        self.plain_text.config(state='disabled')

    def analyze_frequency(self):
        """Analizează frecvențele și afișează graficul"""
        cipher = self.cipher_text.get("1.0", tk.END)
        freq = self.calculate_frequency(cipher)

        if not freq:
            messagebox.showwarning("Avertisment", "Introduce text criptat mai întâi!")
            return

        # Actualizează etichetele de frecvență
        for letter in string.ascii_uppercase:
            freq_label = self.sub_entries[f"{letter}_freq"]
            if letter in freq:
                freq_label.config(text=f"{freq[letter]:.1f}%")
            else:
                freq_label.config(text="0%")

        # Creează graficul
        self.plot_frequency(freq)

    def plot_frequency(self, cipher_freq):
        """Afișează graficul de frecvențe"""
        # Curăță frame-ul anterior
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Top 15 litere cele mai frecvente
        top_letters = list(cipher_freq.keys())[:15]
        cipher_values = [cipher_freq.get(l, 0) for l in top_letters]
        english_values = [self.english_freq.get(l, 0) for l in top_letters]

        # Creează figura cu fundal alb
        fig, ax = plt.subplots(figsize=(11, 4), facecolor='white')
        ax.set_facecolor('white')

        x = range(len(top_letters))
        width = 0.35

        ax.bar([i - width / 2 for i in x], cipher_values, width,
               label='Text Criptat', color='#3b82f6')
        ax.bar([i + width / 2 for i in x], english_values, width,
               label='Limba Engleză', color='#10b981')

        ax.set_xlabel('Litere', fontsize=10)
        ax.set_ylabel('Frecvență (%)', fontsize=10)
        ax.set_title('Comparație Frecvențe: Text Criptat vs Limba Engleză', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(top_letters)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        # Adaugă graficul în interfață
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def auto_suggest(self):
        """Sugerează automat substituții pentru top 5 litere"""
        cipher = self.cipher_text.get("1.0", tk.END)
        freq = self.calculate_frequency(cipher)

        if not freq:
            messagebox.showwarning("Avertisment", "Introduce text criptat mai întâi!")
            return

        cipher_top = list(freq.keys())[:5]
        english_top = sorted(self.english_freq.items(), key=lambda x: x[1], reverse=True)[:5]

        for i, cipher_letter in enumerate(cipher_top):
            english_letter = english_top[i][0]
            self.substitutions[cipher_letter] = english_letter
            self.sub_entries[cipher_letter].delete(0, tk.END)
            self.sub_entries[cipher_letter].insert(0, english_letter)

        self.update_decrypted_text()
        messagebox.showinfo("Succes", f"S-au aplicat {len(cipher_top)} substituții automate!")

    def clear_substitutions(self):
        """Șterge toate substituțiile"""
        self.substitutions.clear()
        for letter in string.ascii_uppercase:
            self.sub_entries[letter].delete(0, tk.END)
        self.update_decrypted_text()

    def load_example(self):
        """Încarcă un exemplu (V1 din document)"""
        example = """NG T OTF gvtisf 4,000 fvtip tjn, xg t wnrg htssvo Zvgvw Lqdcdaniovixgj wqv wqxg ixaang nc wqv
Gxsv, t ztpwvi phixav plvwhqvo ndw wqvqxvinjsfuqp wqtw wnso wqv pwnif nc qxp snio'p sxcv—
tgo xg pn onxgj qvnuvgvo wqv ivhniovo qxpwnif nc hifuwnsnjf."""

        self.cipher_text.delete("1.0", tk.END)
        self.cipher_text.insert("1.0", example)
        self.analyze_frequency()


if __name__ == "__main__":
    root = tk.Tk()
    # Fix pentru macOS
    try:
        root.tk.call('tk', 'scaling', 2.0)
    except:
        pass

    app = FrequencyAnalysisTool(root)
    root.mainloop()