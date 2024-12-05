import customtkinter as ctk
from tkinter import Text
import requests
import json
from datetime import datetime
from PIL import Image, ImageTk
import webbrowser


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


def test_sql_injection(url, results_text, vuln_list):
    """Teste les injections SQL et sauvegarde les vulnérabilités détectées."""
    payloads = load_payloads("payloads/payloadSQL.json")

    if not payloads:
        results_text.insert("end", "Aucun payload disponible.\n")
        return

    successful_tests = []  # Liste des tests réussis

    # Effacer l'ancien contenu
    results_text.delete("1.0", "end")

    for payload_data in payloads:
        payload = payload_data["payload"]
        description = payload_data["description"]

        test_url = f"{url}{payload}"
        results_text.insert("end", f"[+] Test avec {description}...\n")

        try:
            response = requests.get(test_url)

            if any(err in response.text.lower() for err in ["sql syntax", "mysql", "syntax error"]):
                # Enregistre les vulnérabilités
                vulnerability = {
                    "url": url,
                    "payload": payload,
                    "description": description,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                save_vulnerability(vulnerability)

                # Mettre à jour la liste des vulnérabilités dans l'interface
                vuln_list.insert("end", f"{vulnerability['time']} - {vulnerability['description']}\n")

                successful_tests.append(description)
        except Exception as e:
            results_text.insert("end", f"Erreur lors de la requête : {e}\n")

    if successful_tests:
        results_text.insert("end", f"{len(successful_tests)} vulnérabilité(s) détectée(s).\n")
    else:
        results_text.insert("end", "Aucune vulnérabilité détectée.\n")


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

    vuln_list = ctk.CTkTextbox(vuln_list_frame, fg_color="#2e2e2e", text_color="white", font=("Helvetica", 14), wrap="none")
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

    # Documentation Label fixe tout à droite
    def open_documentation():
        webbrowser.open("https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection")

    doc_button = ctk.CTkButton(main_frame, text="Documentation", command=open_documentation, width=150, height=40)
    doc_button.pack(pady=10)

    # Zone de résultats
    results_text = ctk.CTkTextbox(main_frame, fg_color="#1e1e1e", text_color="white", font=("Helvetica", 14), height=20, wrap="word")
    results_text.pack(pady=10, padx=20, fill="both", expand=True)

    # Bouton pour lancer le test
    test_button = ctk.CTkButton(main_frame, text="Tester", command=lambda: test_sql_injection(url_entry.get(), results_text, vuln_list))
    test_button.pack(pady=10)