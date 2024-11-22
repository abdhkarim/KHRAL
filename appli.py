import customtkinter as ctk
from PIL import Image, ImageTk
import requests
from attaquexss import show_xss_page
from apropos import show_about_page  # Import de la fonction de la page apropos.py
from parametres import show_settings_page
from injectionsql import show_sql_page


# Fonction pour récupérer l'adresse IP de l'utilisateur
def get_ip():
    try:
        response = requests.get("https://api.ipify.org")
        ip = response.text
        return ip
    except requests.exceptions.RequestException:
        return "IP non disponible"

# Fonction pour fermer l'application
def quit_application():
    root.quit()

# Fonction pour créer un bouton avec image et texte
def create_button(frame, text, row, column, command, image_path=None):
    # Création du bouton avec une image si elle est fournie
    button = ctk.CTkButton(frame, 
                           text=text, 
                           font=("Helvetica", 14), 
                           fg_color="#4CAF50", 
                           hover_color="#45a049",  # Couleur au survol
                           command=command,
                           width=200,  # Largeur du bouton
                           height=50,  # Hauteur du bouton
                           corner_radius=10)  # Coins arrondis

    if image_path:
        image = Image.open(image_path)  # Ouvrir l'image
        image = image.resize((20, 20))  # Redimensionner l'image
        image = ctk.CTkImage(image, size=(20, 20))  # Créer l'image pour CustomTkinter
        button.configure(image=image, compound="left")  # Ajouter l'image au bouton à gauche du texte
        button.image = image  # Garder une référence à l'image pour éviter qu'elle ne soit supprimée

    button.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
    return button

# Fonction pour aller à une page spécifique
def go_to_page(current_window, page):
    current_window.destroy()
    if page == "sql":
        show_sql_page(main_menu)
    elif page == "xss":
        show_xss_page(main_menu)
    elif page == "apropos":
        show_about_page(main_menu)
    elif page == "parametres":
        show_settings_page(main_menu)


# Fenêtre principale
def main_menu():
    global root  # Pour rendre root accessible dans la fonction quit_application
    root = ctk.CTk()  # Utilisation de CustomTkinter pour la fenêtre
    root.title("KHRAL - Menu Principal")
    
    window_width = 1000
    window_height = 700
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    root.config(bg="#2e2e2e")

    # Configurer la grille pour s'adapter au redimensionnement de la fenêtre
    root.grid_columnconfigure(0, weight=1, minsize=100)  # Colonne pour le logo
    root.grid_columnconfigure(1, weight=3, minsize=400)  # Colonne pour le titre et l'IP
    root.grid_columnconfigure(2, weight=1, minsize=100)  # Colonne pour l'IP
    
    root.grid_rowconfigure(0, weight=1)  # Ligne pour le logo
    root.grid_rowconfigure(1, weight=2)  # Ligne pour le titre
    root.grid_rowconfigure(2, weight=3)  # Ligne pour les boutons
    root.grid_rowconfigure(3, weight=1)  # Ligne pour le bouton quitter

    # Logo en haut à gauche avec CTkImage
    logo_image = Image.open("image/logo.png")
    logo_image = logo_image.resize((100, 100))  # Taille initiale du logo
    logo_image = ctk.CTkImage(logo_image, size=(100, 100))  # Utilisation de CTkImage pour une gestion améliorée de l'image
    logo_label = ctk.CTkLabel(root, image=logo_image, fg_color="#2e2e2e", text="")  # Ajoute text="" pour ne pas afficher de texte
    logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")


    # Affichage de l'adresse IP de l'utilisateur
    user_ip = get_ip()
    ip_label = ctk.CTkLabel(root, text=f"Votre IP: {user_ip}", font=("Helvetica", 14), text_color="white", fg_color="#2e2e2e")
    ip_label.grid(row=0, column=2, padx=10, pady=10, sticky="ne")

    # Titre au centre
    title_label = ctk.CTkLabel(root, text="BIENVENUE SUR KHRAL", font=("Helvetica", 32, "bold"), text_color="white", fg_color="#2e2e2e")
    title_label.grid(row=1, column=0, columnspan=3, pady=20)

    # Cadre pour les boutons
    button_frame = ctk.CTkFrame(root, fg_color="#2e2e2e")
    button_frame.grid(row=2, column=0, columnspan=3, pady=20)

    # Boutons avec un style moderne et images
    sql_button = create_button(button_frame, "Injection SQL", 0, 0, lambda: go_to_page(root, "sql"), "image/sqlinjection.png")
    xss_button = create_button(button_frame, "Attaque XSS", 0, 1, lambda: go_to_page(root, "xss"), "image/attaquexss.png")

    # Label Quitter
    logout_image = Image.open("image/logout.png")
    logout_image = logout_image.resize((20, 20))
    logout_image = ctk.CTkImage(logout_image, size=(20, 20))
    logout_label = ctk.CTkLabel(root, text=" Quitter ", font=("Helvetica", 14), text_color="white", fg_color="#2e2e2e",
                                cursor="hand2", compound="right", image=logout_image)
    logout_label.grid(row=3, column=2, pady=20, padx=20, sticky="se")
    logout_label.bind("<Button-1>", lambda e: quit_application())
    logout_label.image = logout_image

    # Label Paramètres
    about_image = Image.open("image/settings.png")
    about_image = about_image.resize((20, 20))
    about_image = ctk.CTkImage(about_image, size=(20, 20))
    about_label = ctk.CTkLabel(root, text=" Paramètres ", font=("Helvetica", 14), text_color="white", fg_color="#2e2e2e",
                               cursor="hand2", compound="left", image=about_image)
    about_label.grid(row=3, column=0, pady=20, padx=20, sticky="sw")
    about_label.bind("<Button-1>", lambda e: go_to_page(root, "parametres"))
    about_label.image = about_image

    root.mainloop()

if __name__ == "__main__":
    main_menu()