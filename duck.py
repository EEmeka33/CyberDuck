import tkinter as tk
import threading
import random
import time
import sys

# ─── Messages de sensibilisation ───────────────────────────────────────────
TIPS = [
    "⚠️  Ton mot de passe 'azerty123'\n    vient d'être trouvé en 0.3s !",
    "🔍  Je scanne tes fichiers...\n    (démo — un vrai malware ferait pareil)",
    "📧  Cet email semblait légitime ?\n    C'était du phishing !",
    "🔑  Utilise un gestionnaire\n    de mots de passe (Bitwarden, etc.)",
    "🔒  Active le 2FA sur tes comptes !",
    "💾  Dernière sauvegarde ?\n    Un ransomware peut tout chiffrer.",
    "🕵️  Un keylogger peut s'installer\n    en branchant une simple clé USB.",
    "🌐  WiFi public sans VPN =\n    trafic lisible en clair.",
    "🚨  Mise à jour critique ignorée =\n    vecteur d'attaque ouvert.",
    "👾  Je suis une démonstration !\n    Verrouille ton PC (Win+L) quand tu pars.",
]

HACKER_COLOR  = "#0a0a0a"
GREEN         = "#00ff41"
TRANSPARENT   = "#f0f0f0"   # couleur rendue transparente
WIN_W, WIN_H  = 140, 180
SPEED         = 3
FPS           = 30

class CyberGoose:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("")
        self.root.overrideredirect(True)                   # sans bordure
        self.root.attributes("-topmost", True)             # toujours devant
        self.root.attributes("-transparentcolor", TRANSPARENT)
        self.root.configure(bg=TRANSPARENT)
        self.root.wm_attributes("-alpha", 0.93)

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.sw, self.sh = sw, sh
        self.x = float(random.randint(50, sw - WIN_W - 50))
        self.y = float(sh - WIN_H - 50)
        self.dx = SPEED * random.choice([-1, 1])
        self.dy = 0.0

        self.root.geometry(f"{WIN_W}x{WIN_H}+{int(self.x)}+{int(self.y)}")

        # Canvas principal
        self.canvas = tk.Canvas(
            self.root, width=WIN_W, height=WIN_H,
            bg=TRANSPARENT, highlightthickness=0
        )
        self.canvas.pack()
        self._draw_character()

        # Bulle de dialogue séparée
        self.bubble_win = None

        # Threads
        threading.Thread(target=self._move_loop, daemon=True).start()
        threading.Thread(target=self._bubble_loop, daemon=True).start()

        # Quitter avec Ctrl+Shift+Q
        self.root.bind_all("<Control-Shift-q>", lambda e: self.root.destroy())

        self.root.mainloop()

    # ── Dessin du personnage ─────────────────────────────────────────────
    def _draw_character(self, step=0):
        c = self.canvas
        c.delete("all")

        # Capuche
        c.create_oval(30, 5, 110, 75, fill="#1a1a2e", outline=GREEN, width=1)
        # Ombre capuche
        c.create_arc(30, 5, 110, 75, start=200, extent=140,
                     fill="#0d0d1a", outline="")
        # Yeux lumineux
        eye_y = 30 + (2 if step % 2 == 0 else -2)
        c.create_oval(45, eye_y, 62, eye_y+14, fill=GREEN, outline="")
        c.create_oval(78, eye_y, 95, eye_y+14, fill=GREEN, outline="")
        # Pupilles
        c.create_oval(51, eye_y+4, 57, eye_y+10, fill="#000", outline="")
        c.create_oval(84, eye_y+4, 90, eye_y+10, fill="#000", outline="")
        # Corps (sweat)
        c.create_rectangle(25, 73, 115, 145, fill="#1a1a2e", outline=GREEN, width=1)
        # Laptop
        c.create_rectangle(38, 105, 102, 140, fill="#0d0d1a", outline=GREEN)
        c.create_text(70, 122, text=">_ hack", fill=GREEN,
                      font=("Courier", 7, "bold"))
        # Jambes
        leg_off = 4 if step % 4 < 2 else -4
        c.create_rectangle(35, 145, 60, 178+leg_off,
                            fill="#1a1a2e", outline=GREEN)
        c.create_rectangle(80, 145, 105, 178-leg_off,
                            fill="#1a1a2e", outline=GREEN)
        # Texte cybersec en bas
        c.create_text(70, 170, text="[ CYBER DEMO ]",
                      fill=GREEN, font=("Courier", 6))

    # ── Mouvement ────────────────────────────────────────────────────────
    def _move_loop(self):
        step = 0
        while True:
            self.x += self.dx
            # Rebond sur les bords
            if self.x <= 0 or self.x >= self.sw - WIN_W:
                self.dx *= -1
            # Légère oscillation verticale
            self.y = (self.sh - WIN_H - 50) + 12 * (
                0.5 - abs((step % 40) / 40.0 - 0.5)
            )
            self.root.geometry(
                f"{WIN_W}x{WIN_H}+{int(self.x)}+{int(self.y)}"
            )
            self.canvas.after(0, self._draw_character, step)
            step += 1
            time.sleep(1 / FPS)

    # ── Bulles de message ────────────────────────────────────────────────
    def _bubble_loop(self):
        time.sleep(3)
        while True:
            tip = random.choice(TIPS)
            self._show_bubble(tip)
            time.sleep(random.randint(8, 15))

    def _show_bubble(self, text):
        if self.bubble_win:
            try:
                self.bubble_win.destroy()
            except Exception:
                pass

        bw = tk.Toplevel(self.root)
        bw.overrideredirect(True)
        bw.attributes("-topmost", True)
        bw.configure(bg="#0d0d1a")

        lbl = tk.Label(
            bw, text=text, bg="#0d0d1a", fg=GREEN,
            font=("Courier", 9, "bold"),
            padx=10, pady=8,
            relief="flat", justify="left",
            wraplength=230,
        )
        lbl.pack()

        # Bordure verte simulée
        bw.configure(highlightbackground=GREEN, highlightthickness=2)

        bw.update_idletasks()
        bx = int(self.x) + WIN_W + 5
        by = int(self.y)
        if bx + bw.winfo_width() > self.sw:
            bx = int(self.x) - bw.winfo_width() - 5
        bw.geometry(f"+{bx}+{by}")

        self.bubble_win = bw

        # Disparaît après 6s
        threading.Timer(6, lambda: self._safe_destroy(bw)).start()

    def _safe_destroy(self, win):
        try:
            win.destroy()
        except Exception:
            pass

if __name__ == "__main__":
    CyberGoose()