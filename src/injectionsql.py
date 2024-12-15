import customtkinter as ctk
from tkinter import Text
import requests
import json
import urllib.parse
import webbrowser
from datetime import datetime
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox


# Fonction pour charger les payloads à partir d'un fichier JSON
def load_payloads(file_path):
    """Charge les payloads depuis un fichier JSON."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)  # Charger le contenu JSON
            # Assurez-vous que vous récupérez la liste sous la clé 'payloads'
            return data.get("payloads", [])  # Retourne la liste des payloads
    except FileNotFoundError:
        print(f"Le fichier {file_path} est introuvable.")
        return []
    except json.JSONDecodeError:
        print("Erreur lors du chargement du fichier JSON.")
        return []

# Fonction pour enregistrer les vulnérabilités détectées
def save_vulnerability(data, file_path="vulnerabilities.json"):
    """Enregistre une vulnérabilité dans un fichier JSON."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            vulnerabilities = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        vulnerabilities = []

    vulnerabilities.append(data)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(vulnerabilities, file, ensure_ascii=False, indent=4)

# Fonction pour encoder le payload SQL
def encode_sql_payload(payload):
    """Encode les caractères spéciaux dans un payload SQL."""
    return urllib.parse.quote(payload)

# Fonction pour afficher les choix d'injection SQL et effectuer les tests
def display_injection_choices(results_text, vuln_list, choice_entry, test_button, url, db_type):
    """Affiche les résultats dans la fenêtre des résultats (results_text), sans modifier l'historique des vulnérabilités."""
    
    # Effacer le texte "[INFO] En attente des résultats..."
    results_text.configure(state="normal")
    results_text.delete("1.0", "end")  # Vider la zone de texte des anciens résultats

    # Liste des types d'injection avec leurs descriptions
    injection_types = {
        1: "In-band SQLi (Classic SQLi)",
        2: "Error-based SQLi",
        3: "Time-based SQLi",
        4: "Union-based SQLi (Blind SQLi)",
        5: "Auth bypass SQLi"
    }

    # On récupère le choix de l'utilisateur
    choice = choice_entry.get()

    try:
        choice = int(choice)
        if choice < 1 or choice > 5:
            raise ValueError
    except ValueError:
        results_text.configure(state="normal")
        results_text.insert("end", "[!] Choix invalide. Veuillez entrer un numéro entre 1 et 5.\n")
        results_text.configure(state="disabled")
        return

    # Désactiver l'entrée et le bouton après le choix
    choice_entry.configure(state="disabled")
    test_button.configure(state="normal")

    # Définir le fichier JSON des payloads en fonction du type d'injection choisi
    payload_files = {
        1: "payloads/SQLInj/inband_sql.json",
        2: "payloads/SQLInj/error_based.json",
        3: "payloads/SQLInj/time_based_sql.json",
        4: "payloads/SQLInj/union_based_sql.json",
        5: "payloads/SQLInj/authbypass.json"
    }

    payload_file = payload_files.get(choice)
    if not payload_file:
        results_text.configure(state="normal")
        results_text.insert("end", "[!] Type d'injection non trouvé.\n")
        results_text.configure(state="disabled")
        return

    # Charger les payloads
    payloads = load_payloads(payload_file)

    if not payloads:
        results_text.configure(state="normal")
        results_text.insert("end", f"[!] Aucun payload disponible pour ce type d'injection.\n")
        results_text.configure(state="disabled")
        return

    # Liste pour enregistrer les vulnérabilités détectées
    successful_tests = []

    for payload_data in payloads:
        if isinstance(payload_data, dict):  # Vérifier que c'est un dictionnaire
            payload = payload_data.get("payload")
            description = payload_data.get("description")
        else:
            continue  # Ignore les éléments qui ne sont pas des dictionnaires

        # Encoder le payload (pour SQL uniquement, NoSQL n'a pas besoin d'encodage)
        encoded_payload = encode_sql_payload(payload) if db_type == "sql" else payload
        test_url = f"{url}{encoded_payload}"

        try:
            # Envoyer la requête GET à l'URL de test
            response = requests.get(test_url, timeout=5)

            # Analyse différente pour SQL et NoSQL
            if db_type == "sql":
                detected = any(
                    keyword in response.text.lower() for keyword in ["sql syntax", "mysql", "syntax error"]
                )
            else:  # NoSQL (MongoDB, par exemple)
                detected = any(
                    keyword in response.text.lower() for keyword in ["mongodb", "no sql", "bson"]
                )

            if detected:
                results_text.insert("end", f"[!] Vulnérabilité détectée : {description}\n")
                successful_tests.append(description)
            else:
                results_text.insert("end", "[-] Pas de vulnérabilité détectée.\n")

        except requests.exceptions.RequestException as e:
            results_text.insert("end", f"[!] Erreur lors du test : {str(e)}\n")

    # Afficher un résumé des résultats dans la zone des résultats
    if successful_tests:
        results_text.insert("end", f"\n[+] {len(successful_tests)} vulnérabilité(s) détectée(s).\n")
    else:
        results_text.insert("end", "\n[-] Aucune vulnérabilité détectée.\n")

    # Désactiver la zone de texte pour empêcher les modifications
    results_text.configure(state="disabled")
    

# Fonction pour afficher l'historique des vulnérabilités
def display_vulnerability_history(vuln_list):
    """Affiche l'historique des vulnérabilités détectées depuis le fichier JSON."""
    try:
        with open("vulnerabilities.json", "r", encoding="utf-8") as file:
            vulnerabilities = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        vulnerabilities = []

    # Vider la liste de l'historique
    vuln_list.configure(state="normal")
    vuln_list.delete("1.0", "end")  # Effacer les éléments existants

    # Ajouter chaque vulnérabilité au widget
    for vuln in vulnerabilities:
        vuln_list.insert("end", f"URL: {vuln['url']}\n")
        vuln_list.insert("end", f"Payload: {vuln['payload']}\n")
        vuln_list.insert("end", f"Description: {vuln['description']}\n")
        vuln_list.insert("end", f"Type: {vuln['type']}\n")
        vuln_list.insert("end", f"Time: {vuln['time']}\n")
        vuln_list.insert("end", "-" * 50 + "\n")

    vuln_list.configure(state="disabled")

# À chaque fois que l'utilisateur entre son choix, effacer "[INFO] En attente des résultats..."
def show_sql_page(container):
    """Affiche la page Injection SQL dans le conteneur donné."""
    # Effacer le contenu existant dans le conteneur
    for widget in container.winfo_children():
        widget.destroy()

    # Colonne pour l'historique
    vuln_list_frame = ctk.CTkFrame(container, fg_color="#1e1e1e", width=300)
    vuln_list_frame.pack(side="left", fill="y", padx=10, pady=10)

    vuln_list_label = ctk.CTkLabel(vuln_list_frame, text="Historique des vulnérabilités", text_color="white", font=("Helvetica", 16))
    vuln_list_label.pack(pady=10)

    vuln_list = ctk.CTkTextbox(vuln_list_frame, fg_color="#2e2e2e", text_color="white", font=("Helvetica", 14), wrap="none", state="disabled")
    vuln_list.pack(fill="both", expand=True)

    # Zone principale
    main_frame = ctk.CTkFrame(container, fg_color="#2e2e2e")
    main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # Barre pour entrer l'URL
    url_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    url_frame.pack(pady=5, padx=20, anchor="n", fill="x")

    url_label = ctk.CTkLabel(url_frame, text="Entrez l'URL :", text_color="white", font=("Helvetica", 14))
    url_label.pack(side="left", padx=5)

    url_entry = ctk.CTkEntry(url_frame, font=("Helvetica", 14), width=400)
    url_entry.pack(side="left", padx=5, fill="x", expand=True)

    # Section pour les choix d'injection
    choices_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    choices_frame.pack(pady=5, padx=20, anchor="n", fill="x")

    # Texte d'instructions et options
    choices_label = ctk.CTkLabel(
        choices_frame,
        text="Choisir un type d'injection (1-5) en défilant la liste ci-dessous :",
        text_color="white",
        font=("Helvetica", 14),
    )
    choices_label.pack(anchor="nw", padx=5, pady=5)

    choices_textbox = ctk.CTkTextbox(
        choices_frame,
        fg_color="#1e1e1e",
        text_color="white",
        font=("Helvetica", 14),
        height=5,  # Hauteur pour afficher toutes les options
        wrap="word",
        state="normal",  # Permet d'insérer le texte
    )
    choices_textbox.pack(fill="x", pady=5)  # Remplissage horizontal
    choices_textbox.insert(
        "end",
        "1. In-band SQLi (Classic SQLi)\n"
        "2. Error-based SQLi\n"
        "3. Time-based SQLi\n"
        "4. Union-based SQLi (Blind SQLi)\n"
        "5. Auth bypass SQLi",
    )
    choices_textbox.configure(state="disabled")  # Désactivé pour empêcher les modifications

    # Entrée pour le choix
    choice_entry = ctk.CTkEntry(
        choices_frame,
        font=("Helvetica", 14),
        width=100,
        placeholder_text="Ex: 1",  # Indication pour l'utilisateur
    )
    choice_entry.pack(anchor="nw", pady=5, padx=5)  # Placé directement après le texte

    # Zone des résultats
    results_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    results_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Fenêtre vierge pour afficher les résultats
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

    # Documentation bouton
    def open_documentation():
        webbrowser.open("https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection")

    doc_button = ctk.CTkButton(bottom_frame, text="Documentation", command=open_documentation, width=150, height=40)
    doc_button.pack(side="left", padx=5)

    # Bouton pour lancer le test
    test_button = ctk.CTkButton(
        bottom_frame,
        text="Tester",
        command=lambda: display_injection_choices(results_textbox, vuln_list, choice_entry, test_button, url_entry.get(), "sql"),
        fg_color="#4CAF50",
        hover_color="#388E3C",
        text_color="white",
        corner_radius=10,
        font=("Helvetica", 16),
        height=40,
    )
    test_button.pack(side="right", padx=5)


