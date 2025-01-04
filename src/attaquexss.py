import customtkinter as ctk
from tkinter import Text
import requests
import json
import webbrowser
from datetime import datetime
from PIL import Image, ImageTk
from shared import navigate_to_page


class XSSApp:
    def __init__(self, container):
        self.container = container
        self.payloads_file = "src/payloads/XSS/payloadXSS.json"
        self.vuln_file = "vulnerabilities.json"
        self.create_widgets()

    def create_widgets(self):
        """Crée tous les widgets pour la page XSS."""
        # Effacer le contenu existant dans le conteneur
        self.clear_container()

        # Colonne pour l'historique
        vuln_list_frame = ctk.CTkFrame(self.container, fg_color="#1e1e1e", width=300)
        vuln_list_frame.pack(side="left", fill="y", padx=10, pady=10)

        vuln_list_label = ctk.CTkLabel(vuln_list_frame, text="Historique des vulnérabilités", text_color="white", font=("Helvetica", 16))
        vuln_list_label.pack(pady=10)

        self.vuln_list = ctk.CTkTextbox(vuln_list_frame, fg_color="#2e2e2e", text_color="white", font=("Helvetica", 14), wrap="none", state="normal")
        self.vuln_list.pack(fill="both", expand=True)

        # Zone principale
        main_frame = ctk.CTkFrame(self.container, fg_color="#2e2e2e")
        main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Barre pour entrer l'URL
        url_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
        url_frame.pack(pady=5, padx=20, anchor="n", fill="x")

        url_label = ctk.CTkLabel(url_frame, text="Entrez l'URL :", text_color="white", font=("Helvetica", 14))
        url_label.pack(side="left", padx=5)

        self.url_entry = ctk.CTkEntry(url_frame, font=("Helvetica", 14), width=400)
        self.url_entry.pack(side="left", padx=5, fill="x", expand=True)

        # Zone de résultats
        self.results_text = ctk.CTkTextbox(main_frame, fg_color="#1e1e1e", text_color="white", font=("Helvetica", 14), height=20, wrap="word", state="normal")
        self.results_text.pack(pady=10, padx=20, fill="both", expand=True)

        # Boutons en bas
        bottom_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
        bottom_frame.pack(side="bottom", fill="x", pady=10, padx=20)

        # Documentation bouton
        doc_button = ctk.CTkButton(bottom_frame, text="Documentation", command=self.open_documentation, width=150, height=40)
        doc_button.pack(side="left", padx=5)

        # Bouton pour lancer le test
        test_button = ctk.CTkButton(
            bottom_frame,
            text="Tester",
            command=self.test_xss,
            fg_color="#4CAF50",  # Vert
            hover_color="#388E3C",  # Vert plus foncé au survol
            text_color="white",
            corner_radius=10,
            font=("Helvetica", 16),
            height=40
        )
        test_button.pack(side="right", padx=5)

    def open_documentation(self):
        """Ouvre la documentation OWASP XSS dans le navigateur."""
        webbrowser.open("https://owasp.org/www-community/attacks/xss/")

    def load_payloads(self):
        """Charge les payloads depuis un fichier JSON."""
        try:
            with open(self.payloads_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Le fichier {self.payloads_file} est introuvable.")
            return []
        except json.JSONDecodeError:
            print("Erreur lors du chargement du fichier JSON.")
            return []

    def save_vulnerability(self, data):
        """Enregistre une vulnérabilité dans un fichier JSON."""
        try:
            with open(self.vuln_file, "r", encoding="utf-8") as file:
                vulnerabilities = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            vulnerabilities = []

        vulnerabilities.append(data)

        with open(self.vuln_file, "w", encoding="utf-8") as file:
            json.dump(vulnerabilities, file, ensure_ascii=False, indent=4)

    def test_xss(self):
        """Teste les injections XSS et sauvegarde les vulnérabilités détectées."""
        url = self.url_entry.get()
        payloads = self.load_payloads()

        if not payloads:
            self.results_text.configure(state="normal")
            self.results_text.insert("end", "Aucun payload disponible.\n")
            self.results_text.configure(state="disabled")
            return

        successful_tests = []  # Liste des tests réussis

        # Effacer l'ancien contenu
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")

        for payload_data in payloads:
            payload = payload_data["Payload"]
            description = payload_data.get("Description", "N/A")

            # Construire l'URL avec le payload
            test_url = f"{url}{payload}"
            self.results_text.insert("end", f"[+] Test avec {description}...\n")

            try:
                response = requests.get(test_url)

                if payload in response.text:
                    # Enregistre les vulnérabilités
                    vulnerability = {
                        "url": url,
                        "payload": payload,
                        "description": description,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    self.save_vulnerability(vulnerability)

                    # Mettre à jour la liste des vulnérabilités dans l'interface
                    self.vuln_list.insert("end", f"{vulnerability['time']} - {vulnerability['description']}\n")

                    successful_tests.append(description)
            except Exception as e:
                self.results_text.insert("end", f"Erreur lors de la requête : {e}\n")

        if successful_tests:
            self.results_text.insert("end", f"{len(successful_tests)} vulnérabilité(s) détectée(s).\n")
        else:
            self.results_text.insert("end", "Aucune vulnérabilité détectée.\n")

        self.results_text.configure(state="disabled")

    def clear_container(self):
        """Efface tous les widgets dans le conteneur."""
        for widget in self.container.winfo_children():
            widget.destroy()


def show_xss_page(container):
    """Affiche la page d'attaque XSS dans le conteneur donné."""
    XSSApp(container)