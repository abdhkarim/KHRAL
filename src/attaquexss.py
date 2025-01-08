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
        """
        Initialise l'application XSSApp.
        
        Cette méthode définit les chemins des fichiers nécessaires pour les payloads 
        et l'historique des vulnérabilités. Elle appelle également la méthode `create_widgets`
        pour créer l'interface utilisateur de l'application.

        Paramètres :
        container (tkinter.Widget) : Le conteneur parent dans lequel les widgets de l'application seront ajoutés.
        """
        self.container = container
        self.payloads_file = "src/payloads/XSS/payloadXSS.txt"  # Fichier texte pour les payloads
        self.vuln_file = "vulnerabilities.json"
        self.create_widgets()

    def create_widgets(self):
        """
        Crée tous les widgets pour l'interface utilisateur de l'application XSSApp.

        Cette méthode construit l'interface graphique de l'application, y compris :
        - La zone d'affichage des vulnérabilités historiques.
        - Un champ de saisie pour l'URL cible.
        - Un bouton pour lancer le test de vulnérabilité XSS.
        - Un bouton pour ouvrir la documentation OWASP XSS.

        Elle configure également les boutons pour interagir avec l'application.
        """
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
        """
        Ouvre la documentation OWASP XSS dans le navigateur par défaut.

        Cette méthode redirige l'utilisateur vers la page officielle OWASP pour l'attaque XSS 
        afin qu'il puisse consulter des informations détaillées sur cette vulnérabilité.

        Aucun paramètre n'est nécessaire et la méthode ne renvoie rien.
        """
        webbrowser.open("https://owasp.org/www-community/attacks/xss/")

    def load_payloads(self):
        """
        Charge les payloads XSS à partir d'un fichier texte.

        Cette méthode lit le fichier spécifié dans `self.payloads_file` (par défaut "src/payloads/XSS/payloadXSS.txt") 
        et retourne une liste de payloads XSS qui seront utilisés pour les tests de vulnérabilité.

        Elle gère les erreurs de fichier manquant ou d'autres exceptions et renvoie une liste vide si une erreur se produit.

        Retours :
        list : Une liste de chaînes représentant les payloads XSS.
        """
        try:
            with open(self.payloads_file, "r", encoding="utf-8") as file:
                # Lire toutes les lignes et les nettoyer des caractères inutiles (par exemple les retours à la ligne)
                payloads = [line.strip() for line in file.readlines()]
            return payloads
        except FileNotFoundError:
            print(f"Le fichier {self.payloads_file} est introuvable.")
            return []
        except Exception as e:
            print(f"Erreur lors du chargement du fichier : {e}")
            return []

    def save_vulnerability(self, data):
        """
        Enregistre une vulnérabilité détectée dans un fichier JSON.

        Cette méthode prend un dictionnaire contenant les informations de la vulnérabilité, 
        puis l'ajoute à un fichier JSON (par défaut "vulnerabilities.json") qui conserve un historique des vulnérabilités détectées.

        Si le fichier JSON n'existe pas ou est vide, il est créé. Si le fichier est corrompu, une nouvelle liste vide est utilisée.

        Paramètres :
        data (dict) : Un dictionnaire contenant les informations de la vulnérabilité. 
                      Exemple : {'url': 'http://example.com', 'payload': '<script>alert(1)</script>', 'description': 'XSS trouvé', 'time': '2025-01-07 10:30:00'}

        Aucun retour.
        """
        try:
            with open(self.vuln_file, "r", encoding="utf-8") as file:
                vulnerabilities = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            vulnerabilities = []

        vulnerabilities.append(data)

        with open(self.vuln_file, "w", encoding="utf-8") as file:
            json.dump(vulnerabilities, file, ensure_ascii=False, indent=4)

    def test_xss(self):
        """
        Teste la vulnérabilité XSS sur une URL donnée en utilisant des payloads.

        Cette méthode récupère l'URL entrée par l'utilisateur, charge les payloads XSS et effectue des requêtes GET sur l'URL 
        pour chaque payload. Si un payload est renvoyé dans la réponse du serveur, cela signifie que l'URL est vulnérable à l'attaque XSS.

        Les résultats des tests sont affichés dans une zone de texte et les vulnérabilités détectées sont enregistrées dans un fichier JSON.

        Aucun paramètre n'est nécessaire et la méthode ne renvoie rien.
        """
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

        for payload in payloads:
            # Construire l'URL avec le payload
            test_url = f"{url}{payload}"

            try:
                response = requests.get(test_url)

                if payload in response.text:
                    # Affiche uniquement le payload vulnérable
                    self.results_text.insert("end", f"{payload}\n")

                    # Enregistre les vulnérabilités
                    vulnerability = {
                        "url": url,
                        "payload": payload,
                        "description": "XSS trouvé",
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    self.save_vulnerability(vulnerability)

                    successful_tests.append(payload)
            except Exception as e:
                self.results_text.insert("end", f"Erreur lors de la requête : {e}\n")

        # Affiche le nombre de vulnérabilités détectées ou aucun
        if successful_tests:
            self.results_text.insert("end", f"\n{len(successful_tests)} vulnérabilité(s) détectée(s).\n")
        else:
            self.results_text.insert("end", "Aucune vulnérabilité détectée.\n")

        self.results_text.configure(state="disabled")

    def clear_container(self):
        """
        Efface tous les widgets contenus dans le conteneur de l'application.

        Cette méthode parcourt tous les widgets dans le conteneur parent et les supprime afin de réinitialiser l'interface 
        avant d'ajouter de nouveaux widgets. Elle est utile pour naviguer entre différentes pages de l'application.

        Aucun paramètre n'est nécessaire et la méthode ne renvoie rien.
        """
        for widget in self.container.winfo_children():
            widget.destroy()

