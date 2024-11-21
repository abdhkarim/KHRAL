import tkinter as tk
import requests
import urllib.parse
import json
import customtkinter as ctk
import requests
import webbrowser
from PIL import Image

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
    
def test_sql_injection(url, results_text):
    """
    Test d'une injection SQL en envoyant une série de charges utiles malveillantes à l'URL fournie.
    """
    payloads = load_payloads("payloads/payloadSQL.json")  # Charger les payloads depuis un fichier JSON.

    if not payloads:
        results_text.insert(tk.END, "Aucun payload disponible.\n")
        return

    successful_tests = []  # Liste pour stocker les tests réussis

    # Efface le contenu précédent affiché dans le widget Text.
    results_text.delete("1.0", tk.END)

    # Boucle sur chaque payload pour tester les vulnérabilités.
    for payload_data in payloads:
        payload = payload_data["payload"]
        description = payload_data["description"]

        # Affiche le message indiquant quel test est en cours
        results_text.insert(tk.END, f"{description}...\n")
        test_url = f"{url}{payload}"

        try:
            # Envoie une requête HTTP GET à l'URL construite
            response = requests.get(test_url)

            # Vérifie si la réponse contient des messages d'erreur typiques liés à une injection SQL.
            if any(err in response.text.lower() for err in ["sql syntax", "mysql", "syntax error"]):
                # Si un message d'erreur SQL est détecté, cela signifie que le site est vulnérable
                successful_tests.append(description)  # Ajoute le test à la liste des tests réussis
        except Exception as e:
            # Capture et affiche toute erreur rencontrée lors de la requête HTTP.
            results_text.insert(tk.END, f"Erreur lors de la requête : {e}\n")
            return

    # Résumé des tests
    if not successful_tests:
        results_text.insert(tk.END, "Aucune vulnérabilité détectée.\n")
    else:
        results_text.insert(tk.END, f"{len(successful_tests)} injection(s) réussie(s) :\n")
        for test in successful_tests:
            results_text.insert(tk.END, f"- {test}\n")


def get_ip():
    try:
        response = requests.get("https://api.ipify.org")
        ip = response.text
        return ip
    except requests.exceptions.RequestException:
        return "IP non disponible"



def show_sql_page(back_to_menu):
    """Show the SQL Injection page."""
    sql_window = tk.Tk()
    sql_window.title("KHRAL - Injection SQL")
    
    # Définir la taille de la fenêtre
    window_width = 1000
    window_height = 700
    
    # Récupérer les dimensions de l'écran
    screen_width = sql_window.winfo_screenwidth()
    screen_height = sql_window.winfo_screenheight()

    # Calculer les coordonnées pour centrer la fenêtre
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)

    # Positionner la fenêtre au centre de l'écran
    sql_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    sql_window.config(bg="#2e2e2e")  # Fond sombre pour un look moderne

    # Configurer les colonnes et lignes
    sql_window.grid_columnconfigure(0, weight=1)
    sql_window.grid_rowconfigure(6, weight=1)  # Espace entre contenu et label en bas
    sql_window.grid_rowconfigure(7, weight=0)  # Dernière ligne fixe

    # Titre au centre
    title_label = tk.Label(sql_window, text="Injection SQL", font=("Helvetica", 32, "bold"), fg="white", bg="#2e2e2e")
    title_label.grid(row=0, column=0, pady=20, sticky="n")

    # Zone d'entrée pour l'URL
    url_label = tk.Label(sql_window, text="Entrez l'URL à tester :", font=("Helvetica", 14), fg="white", bg="#2e2e2e")
    url_label.grid(row=1, column=0, pady=10, sticky="n")

    url_entry = tk.Entry(sql_window, font=("Helvetica", 14), width=40)
    url_entry.grid(row=2, column=0, pady=10, sticky="n")

    # Zone de texte pour afficher les résultats
    results_text = tk.Text(sql_window, height=15, width=70, font=("Helvetica", 14))
    results_text.grid(row=3, column=0, pady=10, sticky="n")

    # Bouton pour tester les injections SQL
    test_button = ctk.CTkButton(sql_window, 
                                text="Tester les injections SQL", 
                                font=("Helvetica", 14), 
                                fg_color="#4CAF50",  # Couleur de fond
                                hover_color="#45a049",  # Couleur au survol
                                text_color="black",  # Couleur du texte
                                command=lambda: test_sql_injection(url_entry.get(), results_text),
                                width=200,  # Largeur du bouton
                                height=50,  # Hauteur du bouton
                                corner_radius=10)  # Coins arrondis
    test_button.grid(row=4, column=0, pady=10, sticky="n")

    # Bouton pour revenir au menu principal
    back_button = ctk.CTkButton(sql_window, 
                                text="Retour", 
                                font=("Helvetica", 14), 
                                fg_color="#4CAF50", 
                                hover_color="#45a049", 
                                text_color="black", 
                                command=lambda: [sql_window.destroy(), back_to_menu()],
                                width=200, 
                                height=50, 
                                corner_radius=10)
    back_button.grid(row=5, column=0, pady=10, sticky="n")

    # Ajouter un label "Documentation" avec une image cliquable en bas à gauche
    def open_documentation():
        webbrowser.open("https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection")  # Ouvre le lien dans le navigateur

    # Charger l'image pour le label
    try:
        doc_image_image = Image.open("image/documentation.png")
        doc_image = doc_image.resize((20, 20))
        doc_image = ctk.CTkImage(doc_image, size=(20, 20))
    except tk.TclError:
        print("L'image 'documentation.png' est introuvable.")
        doc_image = None  # Gérer le cas où l'image est absente

    # Label cliquable
    doc_label = tk.Label(sql_window, 
                         text=" Documentation",  # Espace avant le texte pour l'image
                         font=("Helvetica", 14), 
                         fg="white", 
                         bg="#2e2e2e", 
                         cursor="hand2", 
                         image=doc_image, 
                         compound="left")  # Positionner l'image à gauche du texte
    doc_label.grid(row=7, column=0, padx=20, pady=10, sticky="w")  # Positionner tout à gauche

    # Lier l'action d'ouverture du lien
    doc_label.bind("<Button-1>", lambda e: open_documentation())

    sql_window.mainloop()
