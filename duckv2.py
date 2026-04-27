import tkinter as tk
import threading
import random
import time
import ctypes
import math
import winsound

# ─── Palette ───────────────────────────────────────────────────────────────
GREEN       = "#00ff41"
RED         = "#ff0040"
ORANGE      = "#ff8c00"
DARK        = "#0d0d1a"
DARKER      = "#1a1a2e"
TRANSPARENT = "#f0f0f0"
WIN_W, WIN_H = 140, 180
FPS          = 30

# ─── Messages bulles ───────────────────────────────────────────────────────
TIPS = [
    "⚠️  Ton mot de passe 'azerty123'\n    vient d'être trouvé en 0.3s !",
    "🔍  Je scanne tes fichiers...\n    (démo — un vrai malware ferait pareil)",
    "📧  Cet email semblait légitime ?\n    C'était du phishing !",
    "🔑  Utilise un gestionnaire\n    de mots de passe (Bitwarden, etc.)",
    "🔒  Active le 2FA sur tes comptes !",
    "💾  Dernière sauvegarde ?\n    Un ransomware peut tout chiffrer.",
    "🕵️  Un keylogger s'installe\n    en branchant une simple clé USB.",
    "🌐  WiFi public sans VPN =\n    trafic lisible en clair.",
    "🚨  Mise à jour ignorée =\n    vecteur d'attaque ouvert.",
    "👾  DEMO ! Verrouille ton PC\n    avec Win+L quand tu pars.",
]

# ─── Alertes popup ─────────────────────────────────────────────────────────
FAKE_ALERTS = [
    ("🚨 ALERTE SÉCURITÉ",
     "Connexion suspecte détectée\ndepuis 185.220.101.42\n(Russie, Moscou)",
     RED),
    ("💀 RANSOMWARE DÉTECTÉ",
     "Chiffrement en cours...\n[████████░░] 80%\nFichiers affectés : 1 337",
     RED),
    ("🔓 MOT DE PASSE VOLÉ",
     "Votre mot de passe Gmail\na été exfiltré vers\nun serveur distant.",
     ORANGE),
    ("📡 RÉSEAU COMPROMIS",
     "Attaque Man-in-the-Middle\ndétectée sur votre WiFi.\nTrafic intercepté.",
     ORANGE),
    ("💻 ACCÈS DISTANT",
     "Session RDP ouverte par\nun utilisateur inconnu.\nAdresse : 10.0.0.69",
     RED),
    ("🗂️ EXFILTRATION",
     "892 fichiers copiés vers\nun serveur FTP anonyme.\n(démo pédagogique)",
     ORANGE),
]

# ─── Lignes terminal fake ──────────────────────────────────────────────────
TERMINAL_LINES = [
    "[*] Initializing payload...",
    "[*] Scanning open ports: 22, 80, 443, 3389",
    "[+] Vulnerability found: CVE-2024-21338",
    "[*] Establishing reverse shell...",
    "[+] Shell access granted: NT AUTHORITY\\SYSTEM",
    "[*] Dumping LSASS credentials...",
    "[+] Hash found: admin:aad3b435b51404eeaad3b435b51404ee",
    "[*] Lateral movement: 192.168.1.{2..254}",
    "[+] 3 hosts compromised",
    "[*] Exfiltrating documents... 892 files",
    "[!] ================================",
    "[!]  CECI EST UNE DEMONSTRATION",
    "[!]  Verrouillez votre PC: Win+L",
    "[!] ================================",
]


# ─── Helpers Windows (ctypes) ──────────────────────────────────────────────
class _POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def _get_cursor():
    pt = _POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def _set_cursor(x, y):
    ctypes.windll.user32.SetCursorPos(int(x), int(y))

def _beep(freq=800, dur=100):
    try:
        winsound.Beep(max(37, min(32767, freq)), dur)
    except Exception:
        pass


# ─── Classe principale ─────────────────────────────────────────────────────
class CyberGoose:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", TRANSPARENT)
        self.root.configure(bg=TRANSPARENT)
        self.root.wm_attributes("-alpha", 0.95)

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.sw, self.sh = sw, sh
        self.x    = float(random.randint(50, sw - WIN_W - 50))
        self.y    = float(sh - WIN_H - 50)
        self.dx   = 3.0 * random.choice([-1, 1])
        self.follow_mouse = False
        self.bubble_win   = None

        self.canvas = tk.Canvas(
            self.root, width=WIN_W, height=WIN_H,
            bg=TRANSPARENT, highlightthickness=0
        )
        self.canvas.pack()
        self._draw_character()

        self.root.bind_all("<Control-Shift-q>", lambda e: self._quit())

        # Lance tout le chaos
        for target in [
            self._move_loop,
            self._bubble_loop,
            self._mouse_troll_loop,
            self._alert_loop,
            self._terminal_loop,
            self._clone_loop,
        ]:
            threading.Thread(target=target, daemon=True).start()

        self.root.mainloop()

    def _quit(self):
        self.root.destroy()

    # ── Dessin personnage amélioré ─────────────────────────────────────
    def _draw_character(self, step=0):
        c = self.canvas
        c.delete("all")
        eye_y = 30 + (2 if step % 2 == 0 else -2)

        # Halo lumineux
        c.create_oval(24, 0, 116, 80, fill="", outline="#003300", width=3)
        # Capuche
        c.create_oval(30, 5, 110, 75, fill=DARKER, outline=GREEN, width=1)
        c.create_arc(30, 5, 110, 75, start=200, extent=140, fill="#0a0a1a", outline="")
        # Glow yeux
        c.create_oval(43, eye_y-2, 64, eye_y+16, fill="#002200", outline="")
        c.create_oval(76, eye_y-2, 97, eye_y+16, fill="#002200", outline="")
        # Yeux (clignement)
        if step % 80 > 76:
            c.create_rectangle(45, eye_y+5, 62, eye_y+9, fill=GREEN, outline="")
            c.create_rectangle(78, eye_y+5, 95, eye_y+9, fill=GREEN, outline="")
        else:
            c.create_oval(45, eye_y,    62, eye_y+14, fill=GREEN, outline="")
            c.create_oval(78, eye_y,    95, eye_y+14, fill=GREEN, outline="")
            c.create_oval(51, eye_y+4,  57, eye_y+10, fill="#000", outline="")
            c.create_oval(84, eye_y+4,  90, eye_y+10, fill="#000", outline="")
        # Corps
        c.create_rectangle(25, 73, 115, 145, fill=DARKER, outline=GREEN, width=1)
        c.create_text(70, 88, text="< / >", fill=GREEN, font=("Courier", 8, "bold"))
        # Laptop
        c.create_rectangle(35, 100, 105, 140, fill="#0a0a0a", outline=GREEN)
        texts = [">_ scan...", ">_ exploit", ">_ [+] OK!", ">_ pwned!"]
        c.create_text(70, 116, text=texts[(step // 20) % 4],
                      fill=GREEN, font=("Courier", 7, "bold"))
        # Barre de progression laptop
        prog = (step % 40) / 40.0
        c.create_rectangle(40, 129, 100, 137, fill="#0a0a0a", outline=GREEN)
        c.create_rectangle(40, 129, 40 + int(60 * prog), 137, fill=GREEN, outline="")
        # Jambes
        lo = 5 if step % 6 < 3 else -5
        c.create_rectangle(35, 143, 60, 172+lo,  fill=DARKER, outline=GREEN)
        c.create_rectangle(80, 143, 105, 172-lo, fill=DARKER, outline=GREEN)
        # Chaussures
        c.create_rectangle(28, 172+lo,  66, 179+lo,  fill=GREEN, outline="")
        c.create_rectangle(74, 172-lo, 112, 179-lo, fill=GREEN, outline="")
        # Badge bas
        c.create_text(70, 167, text="[ CYBER DEMO ]", fill=GREEN, font=("Courier", 6))

    # ── Mouvement + poursuite souris ──────────────────────────────────
    def _move_loop(self):
        step = 0
        while True:
            if self.follow_mouse:
                mx, my = _get_cursor()
                diff    = mx - self.x - WIN_W // 2
                self.dx = max(-10, min(10, diff * 0.12))
                target_y = my - WIN_H
                self.y  += (target_y - self.y) * 0.06
            else:
                self.x += self.dx
                if self.x <= 0 or self.x >= self.sw - WIN_W:
                    self.dx *= -1
                self.y = (self.sh - WIN_H - 50) + 14 * (
                    0.5 - abs((step % 40) / 40.0 - 0.5)
                )

            self.x = max(0, min(self.sw - WIN_W, self.x))
            self.y = max(0, min(self.sh - WIN_H, self.y))
            self.root.geometry(f"{WIN_W}x{WIN_H}+{int(self.x)}+{int(self.y)}")
            self.canvas.after(0, self._draw_character, step)
            step += 1
            time.sleep(1 / FPS)

    # ── Bulles conseils ────────────────────────────────────────────────
    def _bubble_loop(self):
        time.sleep(4)
        while True:
            self.root.after(0, self._show_bubble, random.choice(TIPS))
            time.sleep(random.randint(7, 13))

    def _show_bubble(self, text):
        self._safe_destroy(self.bubble_win)
        bw = tk.Toplevel(self.root)
        bw.overrideredirect(True)
        bw.attributes("-topmost", True)
        bw.configure(bg=DARK, highlightbackground=GREEN, highlightthickness=2)
        tk.Label(bw, text=text, bg=DARK, fg=GREEN,
                 font=("Courier", 9, "bold"), padx=10, pady=8,
                 justify="left", wraplength=240).pack()
        bw.update_idletasks()
        bx = int(self.x) + WIN_W + 5
        if bx + bw.winfo_width() > self.sw:
            bx = int(self.x) - bw.winfo_width() - 5
        bw.geometry(f"+{bx}+{int(self.y)}")
        self.bubble_win = bw
        threading.Timer(6, lambda: self.root.after(0, self._safe_destroy, bw)).start()

    # ── Trolling souris ────────────────────────────────────────────────
    def _mouse_troll_loop(self):
        time.sleep(25)
        while True:
            time.sleep(random.randint(20, 35))
            action = random.choice(["nudge", "circle", "follow"])

            if action == "nudge":
                for _ in range(random.randint(10, 25)):
                    cx, cy = _get_cursor()
                    _set_cursor(cx + random.randint(-20, 20),
                                cy + random.randint(-20, 20))
                    time.sleep(0.04)

            elif action == "circle":
                cx, cy = _get_cursor()
                for i in range(72):
                    angle = (i / 72) * 2 * math.pi
                    _set_cursor(cx + int(70 * math.cos(angle)),
                                cy + int(70 * math.sin(angle)))
                    time.sleep(0.018)
                _set_cursor(cx, cy)

            elif action == "follow":
                self.follow_mouse = True
                time.sleep(10)
                self.follow_mouse = False

    # ── Alertes popup animées ─────────────────────────────────────────
    def _alert_loop(self):
        time.sleep(15)
        while True:
            time.sleep(random.randint(20, 40))
            self.root.after(0, self._spawn_alert)

    def _spawn_alert(self):
        title, msg, color = random.choice(FAKE_ALERTS)
        aw = tk.Toplevel(self.root)
        aw.overrideredirect(True)
        aw.attributes("-topmost", True)
        aw.configure(bg=DARK, highlightbackground=color, highlightthickness=2)
        aw.wm_attributes("-alpha", 0.95)

        # Header coloré
        hdr = tk.Frame(aw, bg=color)
        hdr.pack(fill="x")
        tk.Label(hdr, text=title, bg=color, fg="#000",
                 font=("Courier", 10, "bold"), padx=8, pady=4).pack(side="left")
        tk.Button(hdr, text=" ✕ ", bg=color, fg="#000",
                  font=("Courier", 8, "bold"), relief="flat",
                  command=aw.destroy).pack(side="right")

        tk.Label(aw, text=msg, bg=DARK, fg=color,
                 font=("Courier", 9), padx=12, pady=10,
                 justify="left").pack()

        # Barre de progression si ransomware/exfil
        if any(k in title for k in ("RANSOMWARE", "EXFILTRATION")):
            self._add_progress(aw, color)

        tk.Label(aw, text="[ DÉMO CYBERSÉCURITÉ ]",
                 bg=DARK, fg="#444", font=("Courier", 7)).pack(pady=(0, 6))

        ax = random.randint(50, max(60, self.sw - 320))
        ay = random.randint(50, max(60, self.sh - 200))
        aw.geometry(f"+{ax}+{ay}")
        _beep(1200, 200)
        threading.Timer(12, lambda: self.root.after(0, self._safe_destroy, aw)).start()

    def _add_progress(self, parent, color):
        fr = tk.Frame(parent, bg=DARK)
        fr.pack(fill="x", padx=12, pady=4)
        cv = tk.Canvas(fr, width=240, height=16, bg="#050510",
                       highlightthickness=1, highlightbackground=color)
        cv.pack()

        def anim(v=0):
            cv.delete("all")
            cv.create_rectangle(0, 0, v, 16, fill=color, outline="")
            pct = int(v / 240 * 100)
            cv.create_text(120, 8, text=f"{pct}%",
                           fill="#000" if v > 120 else color,
                           font=("Courier", 8, "bold"))
            if v < 240:
                cv.after(60, anim, v + 5)

        anim()

    # ── Terminal fake ─────────────────────────────────────────────────
    def _terminal_loop(self):
        time.sleep(50)
        while True:
            time.sleep(random.randint(70, 130))
            self.root.after(0, self._spawn_terminal)

    def _spawn_terminal(self):
        tw = tk.Toplevel(self.root)
        tw.overrideredirect(True)
        tw.attributes("-topmost", True)
        tw.configure(bg="#0a0a0a", highlightbackground=GREEN, highlightthickness=2)
        tw.wm_attributes("-alpha", 0.92)

        hdr = tk.Frame(tw, bg="#1a1a1a")
        hdr.pack(fill="x")
        tk.Label(hdr, text="  ● ● ●   cmd.exe — [DEMO]",
                 bg="#1a1a1a", fg="#666", font=("Courier", 8), pady=3).pack(side="left")
        tk.Button(hdr, text=" × ", bg="#1a1a1a", fg="#888",
                  font=("Courier", 9), relief="flat",
                  command=tw.destroy).pack(side="right", padx=4)

        txt = tk.Text(tw, width=55, height=15, bg="#0a0a0a", fg=GREEN,
                      font=("Courier", 8), insertbackground=GREEN,
                      relief="flat", state="disabled")
        txt.pack(padx=4, pady=4)
        txt.tag_config("err", foreground=RED)
        txt.tag_config("ok",  foreground="#88ff88")

        tx = random.randint(50, max(50, self.sw - 460))
        ty = random.randint(50, max(50, self.sh - 280))
        tw.geometry(f"+{tx}+{ty}")

        def type_line(idx=0):
            if idx >= len(TERMINAL_LINES):
                threading.Timer(8, lambda: self.root.after(0, self._safe_destroy, tw)).start()
                return
            line = TERMINAL_LINES[idx]
            tag  = "err" if "[!]" in line else ("ok" if "[+]" in line else "")
            txt.config(state="normal")
            txt.insert("end", line + "\n", tag)
            txt.see("end")
            txt.config(state="disabled")
            _beep(random.randint(200, 700), 25)
            tw.after(random.randint(180, 550), type_line, idx + 1)

        tw.after(300, type_line)

    # ── Clones mini ───────────────────────────────────────────────────
    def _clone_loop(self):
        time.sleep(60)
        while True:
            time.sleep(random.randint(80, 140))
            self.root.after(0, self._spawn_clone)

    def _spawn_clone(self):
        cw, ch = 80, 100
        clone = tk.Toplevel(self.root)
        clone.overrideredirect(True)
        clone.attributes("-topmost", True)
        clone.attributes("-transparentcolor", TRANSPARENT)
        clone.configure(bg=TRANSPARENT)
        clone.wm_attributes("-alpha", 0.85)

        cx = random.randint(50, self.sw - cw - 50)
        cy = random.randint(50, self.sh - ch - 50)
        clone.geometry(f"{cw}x{ch}+{cx}+{cy}")

        cv = tk.Canvas(clone, width=cw, height=ch, bg=TRANSPARENT,
                       highlightthickness=0)
        cv.pack()

        def draw_mini(step=0):
            cv.delete("all")
            cv.create_oval(15, 3, 65, 45, fill=DARKER, outline=GREEN, width=1)
            ey = 18 + (1 if step % 2 == 0 else -1)
            cv.create_oval(22, ey, 34, ey+9, fill=GREEN, outline="")
            cv.create_oval(46, ey, 58, ey+9, fill=GREEN, outline="")
            cv.create_rectangle(12, 44, 68, 88, fill=DARKER, outline=GREEN, width=1)
            cv.create_text(40, 96, text="[CLONE]", fill=GREEN, font=("Courier", 5))
            cv.after(100, draw_mini, step + 1)

        draw_mini()

        speed = [random.choice([-2, 2]), random.choice([-1, 1])]
        pos   = [float(cx), float(cy)]

        def move():
            pos[0] += speed[0]
            pos[1] += speed[1]
            if pos[0] <= 0 or pos[0] >= self.sw - cw:
                speed[0] *= -1
            if pos[1] <= 0 or pos[1] >= self.sh - ch:
                speed[1] *= -1
            try:
                clone.geometry(f"{cw}x{ch}+{int(pos[0])}+{int(pos[1])}")
                clone.after(33, move)
            except Exception:
                pass

        move()
        threading.Timer(45, lambda: self.root.after(0, self._safe_destroy, clone)).start()

    # ── Utils ─────────────────────────────────────────────────────────
    def _safe_destroy(self, win):
        try:
            if win:
                win.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    CyberGoose()