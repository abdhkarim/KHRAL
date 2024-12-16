from tkinter import messagebox  # Ajout pour les confirmations
import customtkinter as ctk
from PIL import Image, ImageTk
from shared import navigate_to_page
from injectionsql import show_sql_page
from attaquexss import show_xss_page
from scanner_api import show_api_scanner_page
from access_control import show_access_control_page
from general_scanner import show_general_scanner_page
from apropos import show_about_page
from parametres import show_settings_page
import os


def quit_application():
    """Ferme l'application proprement."""
    root.quit()


def show_default_page(content_frame):
    """Affiche une page par défaut avec des informations interactives."""
    for widget in content_frame.winfo_children():
        widget.destroy()

    welcome_label = ctk.CTkLabel(
        content_frame,
        text="Bienvenue dans KHRAL",
        font=("Helvetica", 24, "bold"),
        text_color="white",
    )
    welcome_label.pack(pady=20)

    description_label = ctk.CTkLabel(
        content_frame,
        text="Choisissez une fonctionnalité dans le menu à gauche pour commencer.\n\n"
             "Explorez les outils avancés pour la sécurité informatique :\n"
             " • Scanner les vulnérabilités\n"
             " • Tester les injections SQL\n"
             " • Analyser les failles XSS\n\n",
        font=("Helvetica", 16),
        text_color="lightgray",
        justify="left"
    )
    description_label.pack(pady=10)

    # Ajout d'une image (par exemple, un logo interactif ou une icône liée au projet)
    image_path = "/Users/etudiant/Documents/Ecole/Polytech/4ème année/1er Semestre/ProjetS7/assets/kh-logo.png"
    if os.path.exists(image_path):  # Vérifiez si l'image existe
        image = Image.open(image_path).resize((200, 200))
        image_ctk = ctk.CTkImage(image)
        image_label = ctk.CTkLabel(content_frame, text="", image=image_ctk)
        image_label.pack(pady=20)

    # Bouton interactif qui redirige vers une page par exemple "À Propos"
    about_button = ctk.CTkButton(
        content_frame,
        text="En savoir plus",
        command=lambda: navigate_to_page(content_frame, show_about_page),
        fg_color="#2e2e2e",
        hover_color="#3e3e3e",
        corner_radius=10,
        font=("Helvetica", 16),
        height=40
    )
    about_button.pack(pady=10)


def navigate_to_page(content_frame, page_function):
    """Change de page et restaure la page par défaut si la fenêtre est fermée."""
    for widget in content_frame.winfo_children():
        widget.destroy()

    try:
        # Affiche la nouvelle page
        page_function(content_frame)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'ouvrir la page : {e}")
        show_default_page(content_frame)  # Affiche la page par défauts


def main_menu():
    """Affiche le menu principal avec un menu persistant."""
    global root
    root = ctk.CTk()
    root.title("KHRAL - Menu Principal")

    # Centrer la fenêtre sur l'écran
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 1200
    window_height = 800
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    root.configure(bg="#1e1e1e")

    # Bandeau supérieur
    top_frame = ctk.CTkFrame(root, fg_color="#2e2e2e", height=80)
    top_frame.pack(fill="x", side="top")

    # Logo
    logo_image = Image.open("/Users/etudiant/Documents/Ecole/Polytech/4ème année/1er Semestre/ProjetS7/assets/kh-logo.png").resize((50, 50))
    logo_ctk = ctk.CTkImage(logo_image, size=(50, 50))
    logo_label = ctk.CTkLabel(top_frame, text="", image=logo_ctk)
    logo_label.pack(side="left", padx=20, pady=5)

    # Conteneur principal
    main_frame = ctk.CTkFrame(root, fg_color="#1e1e1e")
    main_frame.pack(fill="both", expand=True)

    # Menu latéral
    menu_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e", width=200)
    menu_frame.pack(side="left", fill="y", padx=10, pady=10)

    # Contenu dynamique
    content_frame = ctk.CTkFrame(main_frame, fg_color="#1e1e1e")
    content_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    # Fonctionnalités principales
    features = [
        ("Injection SQL", lambda: navigate_to_page(content_frame, show_sql_page)),
        ("Attaque XSS", lambda: navigate_to_page(content_frame, show_xss_page)),
        ("Scanner API", lambda: navigate_to_page(content_frame, show_api_scanner_page)),
        ("Contrôle des Autorisations", lambda: navigate_to_page(content_frame, show_access_control_page)),
        ("Scanner Général", lambda: navigate_to_page(content_frame, show_general_scanner_page)),
        ("À Propos", lambda: navigate_to_page(content_frame, show_about_page)),
        ("Paramètres", lambda: navigate_to_page(content_frame, show_settings_page)),
    ]


    # Ajout des boutons pour les fonctionnalités dans le menu latéral
    for idx, (title, command) in enumerate(features):
        button = ctk.CTkButton(
            menu_frame,
            text=title,
            command=command,
            fg_color="#2e2e2e",
            hover_color="#3e3e3e",
            corner_radius=10,
            font=("Helvetica", 14),
            height=40
        )
        button.pack(pady=10, padx=10, fill="x")

    # Bouton "Quitter" dans le menu latéral
    quit_button = ctk.CTkButton(
        menu_frame,
        text="Quitter",
        fg_color="#D32F2F",
        hover_color="#C62828",
        text_color="white",
        corner_radius=10,
        font=("Helvetica", 14),
        command=quit_application,
        height=40
    )
    quit_button.pack(side="bottom", pady=10, padx=10)

    # Afficher une page par défaut avec des éléments interactifs
    show_default_page(content_frame)

    root.mainloop()


if __name__ == "__main__":
    main_menu()