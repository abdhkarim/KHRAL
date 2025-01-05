import customtkinter as ctk
import socket
import nmap
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from tkinter import messagebox
from shared import clear_container

# Initialisation du thread pool pour exécuter le scan de manière asynchrone
executor = ThreadPoolExecutor()

class NmapScannerApp:
    def __init__(self, container):
        self.container = container
        self.executor = executor
        self.create_widgets()

    def create_widgets(self):
        """ Crée tous les widgets pour la page de scan Nmap. """
        clear_container(self.container)

        # Conteneur principal
        self.main_frame = ctk.CTkFrame(self.container, fg_color="#2e2e2e")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Section pour entrer la cible
        self.target_frame = ctk.CTkFrame(self.main_frame, fg_color="#2e2e2e")
        self.target_frame.pack(pady=5, padx=20, anchor="n", fill="x")

        self.target_label = ctk.CTkLabel(self.target_frame, text="Cible (IP ou Nom d'hôte) :", text_color="white", font=("Helvetica", 14))
        self.target_label.pack(side="left", padx=5)

        self.target_entry = ctk.CTkEntry(self.target_frame, font=("Helvetica", 14), width=400)
        self.target_entry.pack(side="left", padx=5, fill="x", expand=True)

        # Section pour entrer la plage de ports
        self.ports_frame = ctk.CTkFrame(self.main_frame, fg_color="#2e2e2e")
        self.ports_frame.pack(pady=5, padx=20, anchor="n", fill="x")

        self.ports_label = ctk.CTkLabel(self.ports_frame, text="Plage de ports (ex : 1-1024) :", text_color="white", font=("Helvetica", 14))
        self.ports_label.pack(side="left", padx=5)

        self.start_port_label = ctk.CTkLabel(self.ports_frame, text="Port de début :", text_color="white", font=("Helvetica", 12))
        self.start_port_label.pack(side="left", padx=5)

        self.start_port_entry = ctk.CTkEntry(self.ports_frame, font=("Helvetica", 14), width=100)
        self.start_port_entry.insert(0, "1")
        self.start_port_entry.pack(side="left", padx=5)

        self.end_port_label = ctk.CTkLabel(self.ports_frame, text="Port de fin :", text_color="white", font=("Helvetica", 12))
        self.end_port_label.pack(side="left", padx=5)

        self.end_port_entry = ctk.CTkEntry(self.ports_frame, font=("Helvetica", 14), width=100)
        self.end_port_entry.insert(0, "1024")
        self.end_port_entry.pack(side="left", padx=5)

        # Zone des résultats
        self.results_frame = ctk.CTkFrame(self.main_frame, fg_color="#2e2e2e")
        self.results_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.results_textbox = ctk.CTkTextbox(self.results_frame, fg_color="#1e1e1e", text_color="white", font=("Helvetica", 14), wrap="word")
        self.results_textbox.pack(fill="both", pady=10, padx=20, expand=True)

        # Zone du bouton
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="#2e2e2e")
        self.button_frame.pack(side="bottom", fill="x", pady=10, padx=20)

        self.scan_button = ctk.CTkButton(self.button_frame, text="Scanner", command=self.start_nmap_scan, fg_color="#4CAF50", hover_color="#388E3C", text_color="white", corner_radius=10, font=("Helvetica", 16), height=40)
        self.scan_button.pack(side="right", padx=5)

    def validate_target(self, target):
        """ Valide que la cible est une adresse IP ou un nom d'hôte valide. """
        try:
            ipaddress.ip_address(target)
            return True
        except ValueError:
            pass

        # Si ce n'est pas une adresse IP, essaie de résoudre le nom d'hôte
        try:
            socket.gethostbyname(target)
            return True
        except socket.gaierror:
            return False

    def validate_ports(self, start_port, end_port):
        """ Valide que les ports sont dans les limites valides. """
        try:
            start_port = int(start_port)
            end_port = int(end_port)
            if 1 <= start_port <= 65535 and 1 <= end_port <= 65535 and start_port <= end_port:
                return True
            else:
                return False
        except ValueError:
            return False

    def start_nmap_scan(self):
        """ Lance un scan de type Nmap après avoir validé les entrées. """
        target = self.target_entry.get()
        start_port = self.start_port_entry.get()
        end_port = self.end_port_entry.get()

        # Valider la cible
        if not self.validate_target(target):
            self.update_results("[Erreur] Cible invalide. Veuillez entrer une adresse IP ou un nom d'hôte valide.\n")
            print("[Erreur] Cible invalide.")
            return

        # Valider les ports
        if not self.validate_ports(start_port, end_port):
            self.update_results("[Erreur] Plage de ports invalide. Assurez-vous que les ports sont entre 1 et 65535 et dans le bon format.\n")
            print("[Erreur] Plage de ports invalide.")
            return

        # Désactiver le bouton pendant le scan
        self.scan_button.configure(state="disabled")

        # Lancer le scan dans un thread séparé
        self.executor.submit(self.nmap_scan, target, start_port, end_port)

    def nmap_scan(self, target, start_port, end_port):
        """ Fonction principale pour effectuer un scan de ports avec nmap. """
        nm = nmap.PortScanner()
        results = []

        try:
            print(f"Début du scan pour {target} sur les ports {start_port}-{end_port}...")
            nm.scan(hosts=target, arguments=f'-p {start_port}-{end_port}')

            if nm.all_hosts():
                for host in nm.all_hosts():
                    for proto in nm[host].all_protocols():
                        lport = nm[host][proto].keys()
                        for port in sorted(lport):
                            state = nm[host][proto][port]['state']
                            results.append(f"Port {port} : {state.upper()}")
                            print(f"Port {port} : {state.upper()}")

            if not results:
                results.append("Aucun port ouvert trouvé.")
            results.insert(0, "Scan terminé.\n")
        except Exception as e:
            results.append(f"[Erreur] {str(e)}")
            print(f"[Erreur] {str(e)}")

        # Mettre à jour les résultats dans la zone de texte
        self.container.after(0, self.update_results, "\n".join(results))
        self.container.after(0, self.enable_scan_button)

    def update_results(self, message):
        """ Met à jour la zone de texte avec un message final. """
        self.results_textbox.delete("1.0", "end")  # Effacer le texte précédent
        self.results_textbox.insert("end", message)  # Ajouter le nouveau message

    def enable_scan_button(self):
        """ Réactive le bouton de scan après la fin du scan. """
        self.scan_button.configure(state="normal")