import customtkinter as ctk
from tkinter import Text
import requests
import json
import urllib.parse
import webbrowser
from datetime import datetime
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from shared import clear_container  # Import de la fonction pour effacer le conteneur

class SQLInjectionTester:
    """
    Cette classe gère les tests d'injection SQL. Elle permet de charger des payloads,
    de les encoder et de tester une URL cible avec différents types d'injections SQL.
    """
    
    def __init__(self, url, db_type):
        """
        Initialise un testeur d'injection SQL pour une URL donnée.
        
        Args:
            url (str): L'URL de l'application web à tester.
            db_type (str): Le type de base de données utilisé ("sql" pour SQL ou "nosql" pour NoSQL).
        """
        self.url = url
        self.db_type = db_type

    @staticmethod
    def load_payloads(file_path):
        """
        Charge les payloads SQL à partir d'un fichier JSON. Chaque payload représente 
        une tentative d'injection pour tester la vulnérabilité SQL de l'application.

        Args:
            file_path (str): Le chemin vers le fichier JSON contenant les payloads.

        Returns:
            list: Une liste de payloads chargés depuis le fichier JSON. Si le fichier n'est pas trouvé 
                  ou s'il y a une erreur lors du chargement, retourne une liste vide.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data.get("payloads", [])
        except FileNotFoundError:
            print(f"Le fichier {file_path} est introuvable.")
            return []
        except json.JSONDecodeError:
            print("Erreur lors du chargement du fichier JSON.")
            return []

    @staticmethod
    def encode_sql_payload(payload):
        """
        Encode les caractères spéciaux dans un payload SQL pour les rendre sûrs à inclure dans une URL.

        Args:
            payload (str): Le payload SQL à encoder.

        Returns:
            str: Le payload encodé dans un format sûr pour une URL.
        """
        return urllib.parse.quote(payload)

    def test_injection(self, payload, description):
        """
        Teste un payload d'injection SQL contre l'URL spécifiée. Vérifie si la réponse de l'application 
        indique une vulnérabilité.

        Args:
            payload (str): Le payload SQL à tester.
            description (str): Une description du type d'injection pour le rapport.

        Returns:
            tuple: Un tuple contenant un booléen indiquant si une vulnérabilité a été détectée 
                   et une description du résultat.
        """
        encoded_payload = self.encode_sql_payload(payload) if self.db_type == "sql" else payload
        test_url = f"{self.url}{encoded_payload}"

        try:
            response = requests.get(test_url, timeout=5)

            if self.db_type == "sql":
                detected = any(
                    keyword in response.text.lower() for keyword in ["sql syntax", "mysql", "syntax error"]
                )
            else:  # NoSQL (MongoDB, par exemple)
                detected = any(
                    keyword in response.text.lower() for keyword in ["mongodb", "no sql", "bson"]
                )

            return detected, description
        except requests.exceptions.RequestException as e:
            print(f"[!] Erreur lors du test : {str(e)}")
            return False, str(e)


class VulnerabilityManager:
    """
    Cette classe gère l'historique des vulnérabilités détectées. Elle permet de sauvegarder 
    de nouvelles vulnérabilités et de charger les vulnérabilités précédemment enregistrées.
    """

    def __init__(self, vuln_file="vulnerabilities.json"):
        """
        Initialise un gestionnaire de vulnérabilités avec un fichier JSON pour stocker les résultats.

        Args:
            vuln_file (str): Le chemin vers le fichier JSON où les vulnérabilités sont enregistrées.
        """
        self.vuln_file = vuln_file

    def save_vulnerability(self, data):
        """
        Enregistre une nouvelle vulnérabilité dans un fichier JSON.

        Args:
            data (dict): Un dictionnaire contenant les détails de la vulnérabilité, comme l'URL, 
                         la description et le type d'injection.

        Cette méthode lit le fichier JSON, ajoute la nouvelle vulnérabilité et sauvegarde 
        les changements dans le fichier.
        """
        try:
            with open(self.vuln_file, "r", encoding="utf-8") as file:
                vulnerabilities = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            vulnerabilities = []

        vulnerabilities.append(data)

        with open(self.vuln_file, "w", encoding="utf-8") as file:
            json.dump(vulnerabilities, file, ensure_ascii=False, indent=4)

    def load_vulnerabilities(self):
        """
        Charge l'historique des vulnérabilités détectées depuis le fichier JSON.

        Returns:
            list: Une liste de vulnérabilités enregistrées dans le fichier. Si le fichier n'existe pas 
                  ou s'il est vide, retourne une liste vide.
        """
        try:
            with open(self.vuln_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []


class SQLInjectionApp:
    """
    Cette classe gère l'application graphique pour tester les injections SQL. Elle utilise 
    tkinter et customtkinter pour afficher une interface utilisateur, permet à l'utilisateur 
    de saisir l'URL à tester et d'exécuter les tests d'injection SQL avec différents types 
    de payloads.
    """
    
    def __init__(self, root):
        """
        Initialise l'application en créant une fenêtre principale et en configurant les 
        différents composants de l'interface graphique.

        Args:
            root (Tk): La fenêtre principale de l'application tkinter.
        """
        self.root = root
        self.vuln_manager = VulnerabilityManager()
        self.sql_tester = None

        # Nettoyage et initialisation de l'interface
        clear_container(self.root)
        self.create_widgets()

    def create_widgets(self):
        """
        Crée tous les widgets nécessaires pour l'application. Cela inclut les cadres, 
        les étiquettes, les champs de saisie, et les boutons nécessaires pour tester 
        les injections SQL et afficher les résultats.
        """
        # Colonne pour l'historique
        self.vuln_list_frame = ctk.CTkFrame(self.root, fg_color="#1e1e1e", width=300)
        self.vuln_list_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.vuln_list_label = ctk.CTkLabel(
            self.vuln_list_frame, 
            text="Historique des vulnérabilités", 
            text_color="white", 
            font=("Helvetica", 16)
        )
        self.vuln_list_label.pack(pady=10)

        self.vuln_list = ctk.CTkTextbox(
            self.vuln_list_frame, 
            fg_color="#2e2e2e", 
            text_color="white", 
            font=("Helvetica", 14), 
            wrap="none", 
            state="disabled"
        )
        self.vuln_list.pack(fill="both", expand=True)

        # Zone principale
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#2e2e2e")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Barre pour entrer l'URL
        self.url_frame = ctk.CTkFrame(self.main_frame, fg_color="#2e2e2e")
        self.url_frame.pack(pady=5, padx=20, anchor="n", fill="x")

        self.url_label = ctk.CTkLabel(
            self.url_frame, 
            text="Entrez l'URL :", 
            text_color="white", 
            font=("Helvetica", 14)
        )
        self.url_label.pack(side="left", padx=5)

        self.url_entry = ctk.CTkEntry(self.url_frame, font=("Helvetica", 14), width=400)
        self.url_entry.pack(side="left", padx=5, fill="x", expand=True)

        # Section pour les choix d'injection
        self.choices_frame = ctk.CTkFrame(self.main_frame, fg_color="#2e2e2e")
        self.choices_frame.pack(pady=5, padx=20, anchor="n", fill="x")

        self.choices_label = ctk.CTkLabel(
            self.choices_frame, 
            text="Choisir un type d'injection (1-5) en défilant la liste ci-dessous :", 
            text_color="white", 
            font=("Helvetica", 14)
        )
        self.choices_label.pack(anchor="nw", padx=5, pady=5)

        self.choices_textbox = ctk.CTkTextbox(
            self.choices_frame, 
            fg_color="#1e1e1e", 
            text_color="white", 
            font=("Helvetica", 14), 
            height=5, 
            wrap="word", 
            state="normal"
        )
        self.choices_textbox.pack(fill="x", pady=5)
        self.choices_textbox.insert(
            "end",
            "1. In-band SQLi (Classic SQLi)\n"
            "2. Error-based SQLi\n"
            "3. Time-based SQLi\n"
            "4. Union-based SQLi (Blind SQLi)\n"
            "5. Auth bypass SQLi",
        )
        self.choices_textbox.configure(state="disabled")

        # Entrée pour le choix
        self.choice_entry = ctk.CTkEntry(
            self.choices_frame, font=("Helvetica", 14), width=100, placeholder_text="Ex: 1"
        )
        self.choice_entry.pack(anchor="nw", pady=5, padx=5)

        # Zone des résultats
        self.results_frame = ctk.CTkFrame(self.main_frame, fg_color="#2e2e2e")
        self.results_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.results_textbox = ctk.CTkTextbox(
            self.results_frame, 
            fg_color="#1e1e1e", 
            text_color="white", 
            font=("Courier", 12),  # Police de style monospace
            wrap="word", 
            state="normal"
        )
        self.results_textbox.pack(fill="both", pady=10, padx=20, expand=True)

        # Ajouter le contenu initial
        initial_message = r""" 
        ___  __    ___  ___  ________  ________  ___          
        |\  \|\  \ |\  \|\  \|\   __  \|\   __  \|\  \         
        \ \  \/  /|\ \  \\\  \ \  \|\  \ \  \|\  \ \  \        
        \ \   ___  \ \   __  \ \   _  _\ \   __  \ \  \       
        \ \  \\ \  \ \  \ \  \ \  \\  \\ \  \ \  \ \  \____  
        \ \__\\ \__\ \__\ \__\ \__\\ _\\ \__\ \__\ \_______\
            \|__| \|__|\|__|\|__|\|__|\|__|\|__|\|__|\|_______|
        """
        self.results_textbox.insert("end", initial_message)
        self.results_textbox.configure(state="disabled")

        # Boutons en bas
        self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="#2e2e2e")
        self.bottom_frame.pack(side="bottom", fill="x", pady=10, padx=20)

        self.doc_button = ctk.CTkButton(
            self.bottom_frame, 
            text="Documentation", 
            command=self.open_documentation, 
            width=150, 
            height=40
        )
        self.doc_button.pack(side="left", padx=5)

        self.test_button = ctk.CTkButton(
            self.bottom_frame, 
            text="Tester", 
            command=self.start_testing, 
            fg_color="#4CAF50", 
            hover_color="#388E3C", 
            text_color="white", 
            corner_radius=10, 
            font=("Helvetica", 16), 
            height=40
        )
        self.test_button.pack(side="right", padx=5)

    def open_documentation(self):
        """
        Ouvre la documentation de l'application dans un navigateur web. 
        Cela permet à l'utilisateur de lire les instructions et informations concernant les tests SQL.
        """
        webbrowser.open("https://example.com")

    def start_testing(self):
        """
        Démarre le processus de test d'injection SQL. Elle recueille les informations de l'utilisateur 
        (URL cible, type de vulnérabilité), effectue les tests et affiche les résultats.
        """
        url = self.url_entry.get()
        choice = self.choice_entry.get()

        if not url:
            messagebox.showerror("Erreur", "Veuillez entrer une URL valide.")
            return

        if choice not in ["1", "2", "3", "4", "5"]:
            messagebox.showerror("Erreur", "Veuillez entrer un choix valide pour le type d'injection.")
            return

        # Définir le fichier de payloads et tester l'injection
        payload_file = "sql_payloads.json"
        payloads = SQLInjectionTester.load_payloads(payload_file)
        
        if not payloads:
            messagebox.showerror("Erreur", "Aucun payload trouvé dans le fichier.")
            return
        
        test_results = []
        for payload in payloads:
            test_result, description = self.sql_tester.test_injection(payload, description)

            if test_result:
                test_results.append(f"[+] Vulnérabilité trouvée: {description}")

        if test_results:
            self.results_textbox.configure(state="normal")
            self.results_textbox.delete(1.0, "end")
            self.results_textbox.insert("end", "\n".join(test_results))
            self.results_textbox.configure(state="disabled")