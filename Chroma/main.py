import tkinter as tk
from tkinter import scrolledtext
import threading
import socket
import requests
import subprocess
import platform
import speedtest
import concurrent.futures
import os
import sys

# IP locale + publique
def get_ip_info():
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        public_ip = requests.get("https://api.ipify.org", timeout=5).text
        return f"IP Locale : {local_ip}\nIP Publique : {public_ip}"
    except Exception as e:
        return f"Erreur IP : {e}"

# Speedtest avec timeout via ThreadPoolExecutor
def run_speedtest():
    def do_speedtest():
        st = speedtest.Speedtest()
        st.get_servers([])
        best = st.get_best_server()
        download = st.download()
        upload = st.upload()
        return (f"Ping : {best['latency']} ms\n"
                f"Download : {download / 1_000_000:.2f} Mbps\n"
                f"Upload : {upload / 1_000_000:.2f} Mbps\n"
                f"Serveur : {best['sponsor']} ({best['name']}, {best['country']})")
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(do_speedtest)
            return future.result(timeout=30)  # timeout 30 secondes
    except concurrent.futures.TimeoutError:
        return "Erreur Speedtest : Le test a pris trop de temps (timeout)."
    except Exception as e:
        return f"Erreur Speedtest : {e}"

# Ping générique
def ping_host(host="8.8.8.8"):
    try:
        count_flag = "-n" if platform.system().lower() == "windows" else "-c"
        result = subprocess.run(["ping", count_flag, "4", host],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                timeout=10)
        return result.stdout if result.returncode == 0 else result.stderr
    except subprocess.TimeoutExpired:
        return "Ping timeout."
    except Exception as e:
        return f"Erreur Ping : {e}"

# Fonction pour scanner un seul port, avec timeout
def scan_port(host, port, results):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            results.append(f"Port {port} ouvert")
        sock.close()
    except Exception:
        pass

# Scan ports locaux avec threads
def scan_ports(host="localhost"):
    open_ports = []
    threads = []
    for port in range(20, 1025):
        t = threading.Thread(target=scan_port, args=(host, port, open_ports))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    if open_ports:
        return "\n".join(sorted(open_ports, key=lambda x: int(x.split()[1])))
    else:
        return "Aucun port ouvert détecté."

# Génération rapport réseau dans un fichier
def generate_report():
    try:
        ip = get_ip_info()
        speed = run_speedtest()
        ping = ping_host("8.8.8.8")
        ports = scan_ports("localhost")

        content = (
            "==== RAPPORT RÉSEAU ====\n\n"
            f"[IP INFO]\n{ip}\n\n"
            f"[SPEEDTEST]\n{speed}\n\n"
            f"[PING Google]\n{ping}\n\n"
            f"[PORTS OUVERTS]\n{ports}\n"
        )

        filename = "rapport.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return filename
    except Exception as e:
        return f"Erreur rapport : {e}"

# Ouvre le fichier rapport dans l'éditeur par défaut puis supprime le fichier après fermeture
def open_report_and_delete(filename):
    try:
        system_name = platform.system().lower()
        if system_name == "windows":
            # Lance le bloc-notes et attend la fermeture
            subprocess.run(["notepad.exe", filename])
        elif system_name == "darwin":  # macOS
            # Ouvre TextEdit (commande open attend pas la fermeture donc on utilise AppleScript)
            subprocess.run(["open", "-W", "-a", "TextEdit", filename])
        else:
            # Linux: utilise xdg-open (ne bloque pas forcément, mais on ne gère pas ici)
            subprocess.run(["xdg-open", filename])
            # Ici, on ne peut pas garantir la suppression après fermeture
            # Donc on met un délai raisonnable (exemple 10s) ou on ne supprime pas automatiquement
            import time
            time.sleep(10)  # délai arbitraire
        os.remove(filename)
        return "Rapport affiché et supprimé."
    except Exception as e:
        return f"Erreur lors de l'ouverture/suppression du rapport : {e}"

# Interface graphique sombre avec boutons qui lancent les fonctions dans un thread
def create_gui():
    root = tk.Tk()
    root.title("ChromaX - Outil Réseau")
    root.geometry("750x600")

    bg_color = "#2e2e2e"
    fg_color = "#ffffff"
    btn_bg = "#3a3a3a"
    btn_fg = "#ffffff"
    btn_hover = "#505050"
    output_bg = "#1e1e1e"
    output_fg = "#ffffff"

    root.configure(bg=bg_color)

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=25,
                                          bg=output_bg, fg=output_fg, insertbackground=fg_color)
    text_area.pack(pady=10)

    def show_output(data):
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, data)

    def run_threaded(func, *args):
        def task():
            result = func(*args)
            # Si le résultat est un fichier rapport.txt, ouvre le fichier, attend fermeture, puis supprime
            if isinstance(result, str) and result.endswith(".txt"):
                message = open_report_and_delete(result)
                root.after(0, lambda: show_output(message))
            else:
                root.after(0, lambda: show_output(result))
        threading.Thread(target=task, daemon=True).start()

    def action_ping_custom():
        popup = tk.Toplevel(root)
        popup.title("Ping personnalisé")
        popup.geometry("400x150")
        popup.configure(bg=bg_color)

        label = tk.Label(popup, text="Adresse IP ou domaine :", fg=fg_color, bg=bg_color, font=("Helvetica", 12))
        label.pack(pady=10)

        entry = tk.Entry(popup, width=30, font=("Helvetica", 12))
        entry.pack(pady=5)
        entry.focus()

        def submit_ping(event=None):
            host = entry.get().strip()
            if not host:
                show_output("Veuillez entrer une adresse IP ou un domaine valide.")
                popup.destroy()
                return
            popup.destroy()
            run_threaded(ping_host, host)

        entry.bind("<Return>", submit_ping)

        btn_ping = tk.Button(popup, text="Lancer le ping", command=submit_ping,
                             bg=btn_bg, fg=btn_fg, activebackground=btn_hover,
                             font=("Helvetica", 11))
        btn_ping.pack(pady=10)

    buttons = [
        ("Afficher IP locale/publique", lambda: run_threaded(get_ip_info)),
        ("Lancer Speedtest", lambda: run_threaded(run_speedtest)),
        ("Ping Google (8.8.8.8)", lambda: run_threaded(ping_host)),
        ("Ping personnalisé", action_ping_custom),
        ("Scanner les ports locaux", lambda: run_threaded(scan_ports)),
        ("Générer Rapport Réseau", lambda: run_threaded(generate_report)),
    ]

    for text, cmd in buttons:
        btn = tk.Button(root, text=text, command=cmd, width=40,
                        bg=btn_bg, fg=btn_fg, activebackground=btn_hover,
                        font=("Helvetica", 11), relief=tk.RAISED)
        btn.pack(pady=5)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=btn_hover))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=btn_bg))

    root.mainloop()

if __name__ == "__main__":
    create_gui()
