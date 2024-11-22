import customtkinter as ctk
from PIL import Image, ImageTk
import psutil  # Pour les informations système
from attaquexss import show_xss_page
from apropos import show_about_page
from parametres import show_settings_page
from injectionsql import show_sql_page

# Fonction pour fermer l'application
def quit_application():
    root.quit()

# Fonction pour créer un bouton avec image et texte
def create_button(frame, text, row, column, command, image_path=None):
    button = ctk.CTkButton(frame, 
                           text=text, 
                           font=("Helvetica", 14), 
                           fg_color="#4CAF50", 
                           hover_color="#45a049", 
                           command=command,
                           width=200, 
                           height=50, 
                           corner_radius=10)

    if image_path:
        image = Image.open(image_path)
        image = image.resize((20, 20))
        image = ctk.CTkImage(image, size=(20, 20))
        button.configure(image=image, compound="left")
        button.image = image

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

# Fonction pour récupérer les informations système
def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)  # Pourcentage d'utilisation du CPU
    memory = psutil.virtual_memory()
    memory_usage = memory.percent  # Pourcentage d'utilisation de la RAM
    return f"CPU: {cpu_usage}% | RAM: {memory_usage}%"

# Mettre à jour les informations système dynamiquement
def update_system_info(label):
    label.configure(text=get_system_info())  # Utilisation de 'configure' au lieu de 'config'
    label.after(1000, update_system_info, label)  # Mettre à jour toutes les secondes


# Fenêtre principale
def main_menu():
    global root
    root = ctk.CTk()
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
    root.grid_columnconfigure(0, weight=1, minsize=100)  
    root.grid_columnconfigure(1, weight=3, minsize=400)  
    root.grid_columnconfigure(2, weight=1, minsize=100)  

    root.grid_rowconfigure(0, weight=1)  
    root.grid_rowconfigure(1, weight=2)  
    root.grid_rowconfigure(2, weight=3)  
    root.grid_rowconfigure(3, weight=1)  

    # Logo en haut à gauche avec CTkImage
    logo_image = Image.open("image/logo.png")
    logo_image = logo_image.resize((100, 100))
    logo_image = ctk.CTkImage(logo_image, size=(100, 100))
    logo_label = ctk.CTkLabel(root, image=logo_image, fg_color="#2e2e2e", text="")
    logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    # Affichage des informations système
    system_info_label = ctk.CTkLabel(root, text=get_system_info(), font=("Helvetica", 14), text_color="white", fg_color="#2e2e2e")
    system_info_label.grid(row=0, column=2, padx=10, pady=10, sticky="ne")
    update_system_info(system_info_label)  # Met à jour les informations en temps réel

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
