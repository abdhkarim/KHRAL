import customtkinter as ctk
from tkinter import Text
import requests
import json
import urllib.parse
import webbrowser
from datetime import datetime
from PIL import Image, ImageTk
from shared import navigate_to_page


def load_payloads(file_path):
    """Charge les payloads depuis un fichier JSON."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Le fichier {file_path} est introuvable.")
        return []
    except json.JSONDecodeError:
        print("Erreur lors du chargement du fichier JSON.")
        return []


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


def encode_sql_payload(payload):
    """Encode les caractères spéciaux dans un payload SQL."""
    return urllib.parse.quote(payload)


def test_sql_injection(url, results_text, vuln_list):
    """
    Teste les injections SQL sur une URL en utilisant des payloads.
    Affiche les résultats dans l'interface graphique.
    """
    # Charger les payloads depuis le fichier JSON
    payloads = load_payloads("payloads/payloadSQL.json")

    # Vérifier si des payloads sont disponibles
    if not payloads:
        results_text.configure(state="normal")
        results_text.insert("end", "[!] Aucun payload disponible. Vérifiez le fichier payloadSQL.json.\n")
        results_text.configure(state="disabled")
        return

    # Préparer l'interface pour afficher les résultats
    results_text.configure(state="normal")
    results_text.delete("1.0", "end")  # Vider la zone de texte pour un nouveau test

    # Liste pour enregistrer les vulnérabilités détectées
    successful_tests = []

    for payload_data in payloads:
        payload = payload_data["payload"]
        description = payload_data["description"]

        # Encoder le payload et construire l'URL de test
        encoded_payload = encode_sql_payload(payload)
        test_url = f"{url}{encoded_payload}"

        results_text.insert("end", f"[+] Test avec payload : {description}\n")

        try:
            # Envoyer la requête GET à l'URL de test
            response = requests.get(test_url, timeout=5)

            # Analyser la réponse pour détecter des erreurs SQL communes
            if response.status_code == 200 and any(
                keyword in response.text.lower() for keyword in ["sql syntax", "mysql", "syntax error"]
            ):
                results_text.insert("end", f"[!] Vulnérabilité détectée : {description}\n")

                # Ajouter la vulnérabilité à l'historique
                vulnerability = {
                    "url": url,
                    "payload": payload,
                    "encoded_payload": encoded_payload,
                    "description": description,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                save_vulnerability(vulnerability)

                # Mettre à jour la liste dans l'interface
                vuln_list.configure(state="normal")
                vuln_list.insert("end", f"{vulnerability['time']} - {vulnerability['description']}\n")
                vuln_list.configure(state="disabled")

                successful_tests.append(description)
            else:
                results_text.insert("end", "[-] Pas de vulnérabilité détectée.\n")

        except requests.exceptions.RequestException as e:
            # Afficher les erreurs réseau ou autres
            results_text.insert("end", f"[!] Erreur lors du test : {str(e)}\n")

    # Afficher un résumé des résultats
    if successful_tests:
        results_text.insert("end", f"\n[+] {len(successful_tests)} vulnérabilité(s) détectée(s).\n")
    else:
        results_text.insert("end", "\n[-] Aucune vulnérabilité détectée.\n")

    # Désactiver la zone de texte pour empêcher les modifications
    results_text.configure(state="disabled")


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

    # Zone de résultats
    results_text = ctk.CTkTextbox(main_frame, fg_color="#1e1e1e", text_color="white", font=("Helvetica", 14), height=20, wrap="word", state="disabled")
    results_text.pack(pady=10, padx=20, fill="both", expand=True)

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
        command=lambda: test_sql_injection(url_entry.get(), results_text, vuln_list),
        fg_color="#4CAF50",  # Vert
        hover_color="#388E3C",  # Vert plus foncé au survol
        text_color="white",
        corner_radius=10,
        font=("Helvetica", 16),
        height=40
    )
    test_button.pack(side="right", padx=5)

    # Bouton "Retour à l'accueil"
    back_button = ctk.CTkButton(
        main_frame,
        text="Retour à l'accueil",
        command=lambda: navigate_to_page(container, show_default_page),
        fg_color="#D32F2F",
        hover_color="#C62828",
        text_color="white",
        corner_radius=10,
        font=("Helvetica", 16),
        height=40
    )
    back_button.pack(side="top", pady=20, padx=20)