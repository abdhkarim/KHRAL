import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import requests
import time
from injectionsql import show_sql_page
from attaquexss import show_xss_page

# Fonction pour récupérer l'adresse IP de l'utilisateur
def get_ip():
    try:
        response = requests.get("https://api.ipify.org")
        ip = response.text
        return ip
    except requests.exceptions.RequestException:
        return "IP non disponible"

# Fonction pour mettre à jour l'heure
def update_time(label):
    current_time = time.strftime("%H:%M:%S")
    label.config(text=current_time)
    label.after(1000, update_time, label)

# Fonction pour créer un bouton avec image et texte
def create_button(frame, text, row, column, command, image_path=None):
    image = None
    if image_path:
        img = Image.open(image_path)  # Ouvre l'image avec Pillow
        img = img.resize((50, 50))  # Redimensionne l'image si nécessaire
        image = ImageTk.PhotoImage(img)  # Convertit l'image pour tkinter

    button = tk.Button(frame, text=text, font=("Helvetica", 16), bg="#4CAF50", fg="white", 
                       width=20, height=2, relief="flat", borderwidth=2, command=command,
                       image=image, compound="left")  # Image à gauche du texte
    button.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
    button.bind("<Enter>", lambda e: button.config(bg="#45a049"))  # Change couleur au survol
    button.bind("<Leave>", lambda e: button.config(bg="#4CAF50"))  # Rétablit la couleur d'origine

    # Assurer que l'image est associée au bouton
    if image:
        button.image = image

    return button

# Fonction pour aller à une page spécifique
def go_to_page(current_window, page):
    current_window.destroy()
    if page == "sql":
        show_sql_page(main_menu)
    elif page == "xss":
        show_xss_page(main_menu)

# Fenêtre principale
def main_menu():
    root = tk.Tk()
    root.title("KHRAL - Menu Principal")
    
    # Définir la taille de la fenêtre
    window_width = 1000
    window_height = 700
    
    # Récupérer les dimensions de l'écran
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculer les coordonnées pour centrer la fenêtre
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)

    # Positionner la fenêtre au centre de l'écran
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    root.config(bg="#2e2e2e")  # Fond sombre pour un look moderne

    # Configurer le grid de manière flexible
    root.grid_columnconfigure(0, weight=1, minsize=400)  # Colonne gauche (logo)
    root.grid_columnconfigure(1, weight=3, minsize=400)  # Colonne centrale (IP + titre)
    root.grid_columnconfigure(2, weight=1, minsize=200)  # Colonne droite (titre + IP)
    
    root.grid_rowconfigure(0, weight=1)  # Ligne pour le logo
    root.grid_rowconfigure(1, weight=2)  # Ligne pour le titre central
    root.grid_rowconfigure(2, weight=3)  # Ligne pour les boutons

    # Logo en haut à gauche
    logo = PhotoImage(file="image/logo.png").subsample(8, 8)  # Réduire la taille du logo
    logo_label = tk.Label(root, image=logo, bg="#2e2e2e")
    logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    # Message de bienvenue
    welcome_label = tk.Label(root, text="Bienvenue sur KHRAL!", font=("Helvetica", 14), fg="white", bg="#2e2e2e")
    welcome_label.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

    # Affichage de l'adresse IP de l'utilisateur
    user_ip = get_ip()
    ip_label = tk.Label(root, text=f"Votre IP: {user_ip}", font=("Helvetica", 14), fg="white", bg="#2e2e2e")
    ip_label.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

    # Titre au centre
    title_label = tk.Label(root, text="KHRAL", font=("Helvetica", 32, "bold"), fg="white", bg="#2e2e2e")
    title_label.grid(row=1, column=0, columnspan=3, pady=20)

    # Cadre pour les boutons
    button_frame = tk.Frame(root, bg="#2e2e2e")
    button_frame.grid(row=2, column=0, columnspan=3, pady=20)

    # Boutons avec un style moderne et image
    sql_button = create_button(button_frame, "Injection SQL", 0, 0, lambda: go_to_page(root, "sql"), image_path="image/injectionsql.png")
    xss_button = create_button(button_frame, "Attaque XSS", 0, 1, lambda: go_to_page(root, "xss"), image_path="image/attaquexss.png")

    root.mainloop()

if __name__ == "__main__":
    main_menu()
