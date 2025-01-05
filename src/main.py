from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
import os

# Import des pages spécifiques
from shared import navigate_to_page
from injectionsql import SQLInjectionApp
from attaquexss import XSSApp
from access_control import AccessControlApp
from general_scanner import NmapScannerApp
from passwordgen import show_password_generator_page
from bruteforce import BruteForcePage
from apropos import show_about_page

class App:
    def __init__(self):
        """Initialise l'application et ses éléments."""
        self.root = ctk.CTk()
        self.root.title("KHRAL")

        # Dimensions de la fenêtre
        window_width, window_height = 1200, 800
        x_position = (self.root.winfo_screenwidth() - window_width) // 2
        y_position = (self.root.winfo_screenheight() - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.configure(bg="#1e1e1e")

        # Appels des méthodes pour initialiser l'interface
        self.create_top_frame()
        self.create_main_frame()
        self.show_default_page()

    def create_top_frame(self):
        """Crée la barre de titre et le logo."""
        top_frame = ctk.CTkFrame(self.root, fg_color="#2e2e2e", height=80)
        top_frame.pack(fill="x", side="top")

        # Logo
        assets_path = os.path.join(os.path.dirname(__file__), "assets")
        logo_path = os.path.join(assets_path, "kh-logo.png")
        if os.path.exists(logo_path):
            logo_image = Image.open(logo_path).resize((50, 50))
            logo_ctk = ctk.CTkImage(logo_image, size=(50, 50))
            logo_label = ctk.CTkLabel(top_frame, text="", image=logo_ctk)
            logo_label.pack(side="left", padx=20, pady=5)

    def create_main_frame(self):
        """Crée le cadre principal, incluant le menu latéral et le contenu."""
        # Conteneur principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#1e1e1e")
        self.main_frame.pack(fill="both", expand=True)

        # Menu latéral
        self.menu_frame = ctk.CTkFrame(self.main_frame, fg_color="#2e2e2e", width=200)
        self.menu_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Contenu dynamique
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="#1e1e1e")
        self.content_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        # Ajouter les boutons du menu
        self.features = [
            ("Injection SQL", lambda: self.navigate_to_page(self.show_sql_page)),
            ("Attaque XSS", lambda: self.navigate_to_page(self.show_xss_page)),
            ("Contrôle des Autorisations", lambda: self.navigate_to_page(self.show_access_control_page)),
            ("Attaque Brute Force", lambda: self.navigate_to_page(self.show_brute_force_page)),
            ("Scanner des ports", lambda: self.navigate_to_page(self.show_nmap_page)),
            ("Générateur de Mot de passe", lambda: self.navigate_to_page(self.show_crypto_tests_page)),
            ("A propos", lambda: self.navigate_to_page(self.show_about_page)),
        ]
        for title, command in self.features:
            button = ctk.CTkButton(
                self.menu_frame,
                text=title,
                command=command,
                fg_color="#2e2e2e",
                hover_color="#3e3e3e",
                corner_radius=10,
                font=("Helvetica", 14),
                height=40
            )
            button.pack(pady=10, padx=10, fill="x")

        # Bouton "Quitter"
        quit_button = ctk.CTkButton(
            self.menu_frame,
            text="Quitter",
            fg_color="#D32F2F",
            hover_color="#C62828",
            text_color="white",
            corner_radius=10,
            font=("Helvetica", 14),
            command=self.quit_application,
            height=40
        )
        quit_button.pack(side="bottom", pady=10, padx=10)

    def show_default_page(self):
        """Affiche la page par défaut avec des informations interactives."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        welcome_label = ctk.CTkLabel(
            self.content_frame,
            text="Bienvenue dans KHRAL",
            font=("Helvetica", 24, "bold"),
            text_color="white",
        )
        welcome_label.pack(pady=20)

        description_label = ctk.CTkLabel(
            self.content_frame,
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

        # Ajout d'une image (logo du projet)
        assets_path = os.path.join(os.path.dirname(__file__), "assets")
        image_path = os.path.join(assets_path, "kh-logo.png")
        if os.path.exists(image_path):
            image = Image.open(image_path).resize((200, 200))
            image_ctk = ctk.CTkImage(image)
            image_label = ctk.CTkLabel(self.content_frame, text="", image=image_ctk)
            image_label.pack(pady=20)

        # Bouton interactif pour accéder à "À Propos"
        about_button = ctk.CTkButton(
            self.content_frame,
            text="En savoir plus sur les vulnérabilités de l'OWASP Top 10",
            command=lambda: self.navigate_to_page(self.show_about_page),
            fg_color="#2e2e2e",
            hover_color="#3e3e3e",
            corner_radius=10,
            font=("Helvetica", 16),
            height=40
        )
        about_button.pack(pady=10)

    def navigate_to_page(self, page_function):
        """Change de page et restaure la page par défaut en cas d'erreur."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        try:
            page_function(self.content_frame)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir la page : {e}")
            self.show_default_page()

    def quit_application(self):
        """Ferme l'application proprement."""
        self.root.quit()

    # Méthodes pour chaque page spécifique
    def show_sql_page(self, content_frame):
        SQLInjectionApp(content_frame)

    def show_xss_page(self, content_frame):
        XSSApp(content_frame)

    def show_access_control_page(self, content_frame):
        AccessControlApp(content_frame)

    def show_nmap_page(self, content_frame):
        NmapScannerApp(content_frame)

    def show_crypto_tests_page(self, content_frame):
        show_password_generator_page(content_frame)

    def show_brute_force_page(self, content_frame):
        BruteForcePage(content_frame)

    def show_about_page(self, content_frame):
        show_about_page(content_frame)

if __name__ == "__main__":
    app = App()
    app.root.mainloop()