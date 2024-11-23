import customtkinter as ctk
from PIL import Image
import psutil

from attaquexss import show_xss_page
from apropos import show_about_page
from parametres import show_settings_page
from injectionsql import show_sql_page
from scanner_api import show_api_scanner_page
from access_control import show_access_control_page
from general_scanner import show_general_scanner_page

# Fonction pour quitter l'application
def quit_application():
    root.quit()

# Fonction pour récupérer les informations système
def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    return f"CPU: {cpu_usage}% | RAM: {memory_usage}%"

# Mise à jour dynamique des infos système
def update_system_info(label):
    label.configure(text=get_system_info())
    label.after(1000, update_system_info, label)

# Fonction pour aller à une page spécifique
def go_to_page(current_window, page):
    current_window.destroy()
    if page == "sql":
        show_sql_page(main_menu)
    elif page == "xss":
        show_xss_page(main_menu)
    elif page == "api_scanner":
        show_api_scanner_page(main_menu)
    elif page == "access_control":
        show_access_control_page(main_menu)
    elif page == "general_scanner":
        show_general_scanner_page(main_menu)
    elif page == "apropos":
        show_about_page(main_menu)
    elif page == "parametres":
        show_settings_page(main_menu)

# Fonction principale
def main_menu():
    global root
    root = ctk.CTk()
    root.title("KHRAL - Menu Principal")
    root.geometry("1200x800")
    root.configure(bg="#1e1e1e")

    # Bandeau supérieur
    top_frame = ctk.CTkFrame(root, fg_color="#2e2e2e", height=80)
    top_frame.pack(fill="x", side="top")

    # Logo
    logo_image = Image.open("image/logo.png").resize((50, 50))
    logo_ctk = ctk.CTkImage(logo_image, size=(50, 50))
    logo_label = ctk.CTkLabel(top_frame, text="", image=logo_ctk)
    logo_label.pack(side="left", padx=20, pady=5)

    # Informations système
    system_info_label = ctk.CTkLabel(top_frame, text=get_system_info(), font=("Helvetica", 14), text_color="white")
    system_info_label.pack(side="right", padx=20)
    update_system_info(system_info_label)

    # Contenu principal
    content_frame = ctk.CTkFrame(root, fg_color="#1e1e1e")
    content_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Cartes avec boutons
    features = [
        ("Injection SQL", "image/sqlinjection.png", lambda: go_to_page(root, "sql")),
        ("Attaque XSS", "image/attaquexss.png", lambda: go_to_page(root, "xss")),
        ("Scanner API", "image/api_scanner.png", lambda: go_to_page(root, "api_scanner")),
        ("Contrôle des Autorisations", "image/access_control.png", lambda: go_to_page(root, "access_control")),
        ("Scanner Général", "image/general_scanner.png", lambda: go_to_page(root, "general_scanner")),
        ("Paramètres", "image/settings.png", lambda: go_to_page(root, "parametres")),
        ("À Propos", "image/about.png", lambda: go_to_page(root, "apropos")),
    ]

    for idx, (title, icon, command) in enumerate(features):
        card = ctk.CTkFrame(content_frame, fg_color="#2e2e2e", corner_radius=15)
        card.grid(row=idx // 2, column=idx % 2, padx=20, pady=20, sticky="nsew")

        card_image = Image.open(icon).resize((50, 50))
        card_image_ctk = ctk.CTkImage(card_image, size=(50, 50))
        card_label = ctk.CTkLabel(card, image=card_image_ctk, text="", fg_color="#2e2e2e")
        card_label.pack(pady=10)

        card_button = ctk.CTkButton(
            card, text=title, fg_color="#4CAF50", hover_color="#45a049",
            text_color="black", font=("Helvetica", 16), command=command,
            corner_radius=10, width=200, height=40
        )
        card_button.pack(pady=10)

    # Bouton "Quitter"
    quit_button = ctk.CTkButton(
        root, text="Quitter", fg_color="#D32F2F", hover_color="#C62828",
        text_color="white", corner_radius=10, font=("Helvetica", 14),
        command=quit_application, width=150, height=40
    )
    quit_button.pack(side="bottom", pady=20)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
