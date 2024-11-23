import tkinter as tk
import requests
import json
from datetime import datetime
import customtkinter as ctk
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


def load_vulnerabilities(file_path="vulnerabilities.json"):
    """Charge les vulnérabilités enregistrées depuis un fichier JSON."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def test_sql_injection(url, results_text, vuln_list):
    """Teste les injections SQL et sauvegarde les vulnérabilités détectées."""
    payloads = load_payloads("payloads/payloadSQL.json")

    if not payloads:
        results_text.insert(tk.END, "Aucun payload disponible.\n")
        return

    successful_tests = []  # Liste des tests réussis

    # Effacer l'ancien contenu
    results_text.delete("1.0", tk.END)

    for payload_data in payloads:
        payload = payload_data["payload"]
        description = payload_data["description"]

        test_url = f"{url}{payload}"
        results_text.insert(tk.END, f"[+] Test avec {description}...\n")

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
                vuln_list.insert(tk.END, f"{vulnerability['time']} - {vulnerability['description']}\n")

                successful_tests.append(description)
        except Exception as e:
            results_text.insert(tk.END, f"Erreur lors de la requête : {e}\n")

    if successful_tests:
        results_text.insert(tk.END, f"{len(successful_tests)} vulnérabilité(s) détectée(s).\n")
    else:
        results_text.insert(tk.END, "Aucune vulnérabilité détectée.\n")


def show_sql_page(back_to_menu=None):
    """Affiche la page de test d'injections SQL avec un label Documentation fixe tout à droite."""
    sql_window = tk.Tk()
    sql_window.title("KHRAL - Injection SQL")

    # Taille et positionnement de la fenêtre
    sql_window.geometry("1200x800")
    sql_window.config(bg="#2e2e2e")

    # Colonne pour l'historique
    vuln_list_frame = tk.Frame(sql_window, bg="#1e1e1e", width=300)
    vuln_list_frame.pack(side="left", fill="y")

    vuln_list_label = tk.Label(vuln_list_frame, text="Historique des vulnérabilités", bg="#1e1e1e", fg="white", font=("Helvetica", 16))
    vuln_list_label.pack(pady=10)

    vuln_list = tk.Listbox(vuln_list_frame, bg="#2e2e2e", fg="white", font=("Helvetica", 14))
    vuln_list.pack(fill="both", expand=True)

    # Zone principale
    main_frame = tk.Frame(sql_window, bg="#2e2e2e")
    main_frame.pack(side="right", fill="both", expand=True)

    # Barre pour entrer l'URL
    url_frame = tk.Frame(main_frame, bg="#2e2e2e")
    url_frame.pack(pady=5, padx=20, anchor="n", fill="x")

    url_label = tk.Label(url_frame, text="Entrez l'URL :", bg="#2e2e2e", fg="white", font=("Helvetica", 14))
    url_label.pack(side="left", padx=5)

    url_entry = tk.Entry(url_frame, font=("Helvetica", 14), width=80)
    url_entry.pack(side="left", padx=5, fill="x", expand=True)

    # Documentation Label fixe tout à droite
    def open_documentation():
        webbrowser.open("https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection")

    try:
        # Charger l'image
        doc_image = Image.open("images/documentation.png")
        doc_image = doc_image.resize((20, 20), Image.ANTIALIAS)
        doc_image_tk = ImageTk.PhotoImage(doc_image)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image : {e}")
        doc_image_tk = None

    doc_label_frame = tk.Frame(sql_window, bg="#2e2e2e")
    doc_label_frame.pack(side="top", anchor="ne", padx=20, pady=10)

    doc_label = tk.Label(doc_label_frame, text=" Documentation", image=doc_image_tk, compound="left", fg="#4CAF50",
                         bg="#2e2e2e", cursor="hand2", font=("Helvetica", 14))
    doc_label.image = doc_image_tk  # Référencer l'image pour éviter le garbage collection
    doc_label.pack(side="right")
    doc_label.bind("<Button-1>", lambda e: open_documentation())

    # Zone de résultats
    results_text = tk.Text(main_frame, bg="#1e1e1e", fg="white", font=("Helvetica", 14), height=20)
    results_text.pack(pady=10, padx=20, fill="both", expand=True)

    # Bouton pour lancer le test
    test_button = ctk.CTkButton(main_frame, text="Tester", command=lambda: print("Test en cours..."))  # Ajoutez votre fonction ici
    test_button.pack(pady=10)

    # Bouton de retour au menu principal
    if back_to_menu:
        back_button = ctk.CTkButton(main_frame, text="Retour", command=lambda: [sql_window.destroy(), back_to_menu()])
        back_button.pack(pady=10)

    sql_window.mainloop()