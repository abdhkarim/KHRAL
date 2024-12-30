import customtkinter as ctk
import socket
from concurrent.futures import ThreadPoolExecutor
from tkinter import messagebox

executor = ThreadPoolExecutor()

def validate_target(target):
    """
    Valide que la cible est une adresse IP ou un nom d'hôte valide.
    """
    try:
        socket.gethostbyname(target)
        return True
    except socket.gaierror:
        return False

def validate_port_range(port_range):
    """
    Valide que la plage de ports est au bon format et que les valeurs sont valides.
    """
    try:
        start_port, end_port = map(int, port_range.split('-'))
        return 1 <= start_port <= 65535 and 1 <= end_port <= 65535 and start_port <= end_port
    except (ValueError, IndexError):
        return False

def start_nmap_scan(target, port_range, results_text, scan_button):
    """ Lance un scan de type Nmap après avoir validé les entrées. """
    results_text.delete("1.0", "end")

    # Valider la cible
    if not validate_target(target):
        results_text.insert("end", "[Erreur] Cible invalide. Veuillez entrer une adresse IP ou un nom d'hôte valide.\n")
        return

    # Valider la plage de ports
    if not validate_port_range(port_range):
        results_text.insert("end", "[Erreur] Plage de ports invalide. Utilisez le format '1-1024'.\n")
        return

    # Lancer le scan
    results_text.insert("end", f"Début du scan pour {target} sur les ports {port_range}...\n")
    scan_button.configure(state="disabled")
    executor.submit(nmap_scan, target, port_range, results_text, scan_button)

def nmap_scan(target, port_range, results_text, scan_button):
    """
    Fonction principale pour effectuer un scan de ports.
    """
    try:
        # Résolution de l'adresse IP
        ip_address = socket.gethostbyname(target)
        results_text.after(0, lambda: results_text.insert("end", f"Adresse IP résolue : {ip_address}\n"))
    except socket.gaierror:
        results_text.after(0, lambda: results_text.insert("end", f"[Erreur] Impossible de résoudre l'adresse {target}.\n"))
        results_text.after(0, lambda: scan_button.configure(state="normal"))
        return

    # Déterminer la plage de ports
    start_port, end_port = map(int, port_range.split('-'))
    results_text.after(0, lambda: results_text.insert("end", "Scan des ports en cours...\n"))
    open_ports = []

    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((ip_address, port)) == 0:
                    open_ports.append(port)
                    service_name = get_service_name(port)
                    results_text.after(0, lambda: results_text.insert("end", f"Port {port} ouvert - Service : {service_name}\n"))
        except Exception:
            pass

    # Résultats finaux
    if open_ports:
        results_text.after(0, lambda: results_text.insert("end", f"\nPorts ouverts détectés : {', '.join(map(str, open_ports))}\n"))
    else:
        results_text.after(0, lambda: results_text.insert("end", "Aucun port ouvert détecté.\n"))

    results_text.after(0, lambda: results_text.insert("end", "Scan terminé.\n"))
    results_text.after(0, lambda: scan_button.configure(state="normal"))

def get_service_name(port):
    """
    Retourne le nom du service associé à un port, si disponible.
    """
    try:
        return socket.getservbyport(port)
    except OSError:
        return "Inconnu"

def show_nmap_page(container):
    """
    Affiche la page Nmap-like dans le conteneur donné.
    """
    # Efface les widgets existants
    for widget in container.winfo_children():
        widget.destroy()

    # Conteneur principal
    main_frame = ctk.CTkFrame(container, fg_color="#2e2e2e")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Section pour entrer la cible
    target_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    target_frame.pack(pady=5, padx=20, anchor="n", fill="x")

    target_label = ctk.CTkLabel(target_frame, text="Cible (IP ou Nom d'hôte) :", text_color="white", font=("Helvetica", 14))
    target_label.pack(side="left", padx=5)

    target_entry = ctk.CTkEntry(target_frame, font=("Helvetica", 14), width=400)
    target_entry.pack(side="left", padx=5, fill="x", expand=True)

    # Section pour entrer la plage de ports
    ports_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    ports_frame.pack(pady=5, padx=20, anchor="n", fill="x")

    ports_label = ctk.CTkLabel(ports_frame, text="Plage de ports (ex : 1-1024) :", text_color="white", font=("Helvetica", 14))
    ports_label.pack(side="left", padx=5)

    ports_entry = ctk.CTkEntry(ports_frame, font=("Helvetica", 14), width=200)
    ports_entry.insert(0, "1-1024")
    ports_entry.pack(side="left", padx=5)

    # Zone des résultats
    results_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    results_frame.pack(pady=10, padx=20, fill="both", expand=True)

    results_textbox = ctk.CTkTextbox(
        results_frame,
        fg_color="#1e1e1e",
        text_color="white",
        font=("Helvetica", 14),
        wrap="word",
    )
    results_textbox.pack(fill="both", pady=10, padx=20, expand=True)
    results_textbox.configure(state="normal")

    # Boutons
    bottom_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    bottom_frame.pack(side="bottom", fill="x", pady=10, padx=20)

    scan_button = ctk.CTkButton(
        bottom_frame,
        text="Scanner",
        command=lambda: start_nmap_scan(target_entry.get(), ports_entry.get(), results_textbox, scan_button),
        fg_color="#4CAF50",
        hover_color="#388E3C",
        text_color="white",
        corner_radius=10,
        font=("Helvetica", 16),
        height=40,
    )
    scan_button.pack(side="right", padx=5)
