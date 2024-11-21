import tkinter as tk
from tkinter import messagebox
import requests

def test_xss(url, results_text):
    """Test XSS vulnerability by injecting payloads into the URL."""
    payloads = ["<script>alert('XSS')</script>", "<img src='x' onerror='alert(1)'>", "<svg/onload=alert(1)>"]
    vulnerable = False
    results_text.delete("1.0", tk.END)

    for payload in payloads:
        test_url = f"{url}{payload}"
        try:
            response = requests.get(test_url)
            if payload in response.text:
                results_text.insert(tk.END, f"Vulnérable avec le payload : {payload}\n")
                vulnerable = True
        except Exception as e:
            results_text.insert(tk.END, f"Erreur lors de la requête : {e}\n")
            return

    if not vulnerable:
        results_text.insert(tk.END, "Aucune vulnérabilité détectée.\n")

def show_xss_page(back_to_menu):
    """Show the XSS attack page."""
    xss_window = tk.Tk()
    xss_window.title("KHRAL - Attaque XSS")
    
    # Définir la taille de la fenêtre
    window_width = 1000
    window_height = 700
    
    # Récupérer les dimensions de l'écran
    screen_width = xss_window.winfo_screenwidth()
    screen_height = xss_window.winfo_screenheight()

    # Calculer les coordonnées pour centrer la fenêtre
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)

    # Positionner la fenêtre au centre de l'écran
    xss_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    xss_window.config(bg="#2e2e2e")  # Fond sombre pour un look moderne

    # Configurer le grid de manière flexible
    xss_window.grid_columnconfigure(0, weight=1, minsize=400)  # Colonne gauche (logo)
    xss_window.grid_columnconfigure(1, weight=3, minsize=400)  # Colonne centrale (IP + titre)
    xss_window.grid_columnconfigure(2, weight=1, minsize=200)  # Colonne droite (titre + IP)
    
    xss_window.grid_rowconfigure(0, weight=1)  # Ligne pour le logo
    xss_window.grid_rowconfigure(1, weight=2)  # Ligne pour le titre central
    xss_window.grid_rowconfigure(2, weight=3)  # Ligne pour les boutons

    # Logo en haut à gauche
    logo = tk.PhotoImage(file="image/logo.png").subsample(8, 8)
    logo_label = tk.Label(xss_window, image=logo, bg="#2e2e2e")
    logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    # Message de bienvenue
    welcome_label = tk.Label(xss_window, text="Bienvenue sur KHRAL!", font=("Helvetica", 14), fg="white", bg="#2e2e2e")
    welcome_label.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

    # Affichage de l'adresse IP de l'utilisateur
    user_ip = get_ip()
    ip_label = tk.Label(xss_window, text=f"Votre IP: {user_ip}", font=("Helvetica", 14), fg="white", bg="#2e2e2e")
    ip_label.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

    # Titre au centre
    title_label = tk.Label(xss_window, text="KHRAL", font=("Helvetica", 32, "bold"), fg="white", bg="#2e2e2e")
    title_label.grid(row=1, column=0, columnspan=3, pady=20)

    # Zone d'entrée pour l'URL
    url_label = tk.Label(xss_window, text="Entrez l'URL à tester :", font=("Helvetica", 14), fg="white", bg="#2e2e2e")
    url_label.grid(row=2, column=1, pady=10)

    url_entry = tk.Entry(xss_window, font=("Helvetica", 14), width=40)
    url_entry.grid(row=3, column=1, pady=10)

    # Zone de texte pour afficher les résultats
    results_text = tk.Text(xss_window, height=15, width=70, font=("Helvetica", 14))
    results_text.grid(row=4, column=0, columnspan=3, pady=10)

    # Bouton pour tester l'attaque XSS
    test_button = tk.Button(xss_window, text="Tester l'attaque XSS", font=("Helvetica", 14), bg="#4CAF50", fg="white",
                            command=lambda: test_xss(url_entry.get(), results_text))
    test_button.grid(row=5, column=1, pady=10)

    # Bouton pour revenir au menu principal
    back_button = tk.Button(xss_window, text="Retour", font=("Helvetica", 14), command=lambda: [xss_window.destroy(), back_to_menu()])
    back_button.grid(row=6, column=1, pady=10)

    xss_window.mainloop()

def get_ip():
    try:
        response = requests.get("https://api.ipify.org")
        ip = response.text
        return ip
    except requests.exceptions.RequestException:
        return "IP non disponible"
