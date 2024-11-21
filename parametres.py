import customtkinter as ctk
from PIL import Image
from apropos import show_about_page  # Import de la fonction pour afficher la page "À propos"

def show_settings_page(return_to_menu):
    settings_window = ctk.CTk()
    settings_window.title("Paramètres")
    
    # Centrer la fenêtre
    window_width = 400
    window_height = 300
    screen_width = settings_window.winfo_screenwidth()
    screen_height = settings_window.winfo_screenheight()
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    settings_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    # Arrière-plan
    settings_window.config(bg="#2e2e2e")

    # Label Titre
    title_label = ctk.CTkLabel(settings_window, text="Paramètres", font=("Helvetica", 20, "bold"), text_color="white")
    title_label.pack(pady=20)

    # Label "À propos" avec le logo
    about_image = Image.open("image/about.png")
    about_image = about_image.resize((40, 40))  # Redimensionner l'image
    about_ctk_image = ctk.CTkImage(about_image, size=(40, 40))  # Créer l'image CTk

    # Création du label avec image et texte
    about_label = ctk.CTkLabel(settings_window, text=" À propos ", font=("Helvetica", 14), text_color="white", 
                               fg_color="#2e2e2e", cursor="hand2", compound="left", image=about_ctk_image)
    about_label.pack(pady=10)

    # Rediriger vers la page "À propos" lorsque l'utilisateur clique sur le label
    about_label.bind("<Button-1>", lambda e: [settings_window.destroy(), show_about_page(return_to_menu)])

    settings_window.mainloop()
