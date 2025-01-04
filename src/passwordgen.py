import os
from cryptography.fernet import Fernet
import customtkinter as ctk
from tkinter import messagebox

def show_password_generator_page(container):
    """
    Affiche une page permettant de générer un mot de passe très sécurisé.
    """
    # Nettoyer le conteneur
    for widget in container.winfo_children():
        widget.destroy()

    # Titre de la page
    title_label = ctk.CTkLabel(
        container, text="Générateur de Mot de Passe Sécurisé", font=("Helvetica", 20, "bold"), text_color="white"
    )
    title_label.pack(pady=20)

    # Zone pour afficher le mot de passe généré
    password_display = ctk.CTkLabel(
        container, text="", font=("Helvetica", 18, "bold"), text_color="lightgray", justify="center", wraplength=600
    )
    password_display.pack(pady=30)

    # Fonction pour générer un mot de passe sécurisé
    def generate_password():
        import random
        import string
        length = 16
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choices(characters, k=length))
        password_display.configure(text=password)

        # Positionner le message en bas après génération
        confirm_label.pack(side="bottom", pady=10)
        confirm_button_yes.pack(side="bottom", pady=5)
        confirm_button_no.pack(side="bottom", pady=5)

    # Bouton pour générer le mot de passe
    generate_button = ctk.CTkButton(
        container,
        text="Générer un mot de passe",
        command=generate_password,
        fg_color="#0078D7",
        hover_color="#005A9E",
        corner_radius=10,
        font=("Helvetica", 16),
        height=40
    )
    generate_button.pack(pady=20)

    # Fonction pour sauvegarder le mot de passe
    def save_password(password):
        # Clé pour chiffrer le fichier
        key = Fernet.generate_key()
        cipher = Fernet(key)
        encrypted_password = cipher.encrypt(password.encode())

        # Chemin du fichier
        file_path = os.path.expanduser("~/secure_passwords.txt")

        # Sauvegarde du fichier chiffré
        with open(file_path, "wb") as file:
            file.write(encrypted_password)

        # Demande de mot de passe pour déchiffrer
        decrypt_password_window(key)

    # Fonction pour créer un mot de passe d'accès au fichier
    def decrypt_password_window(key):
        window = ctk.CTkToplevel()
        window.geometry("400x300")
        window.title("Mot de passe pour fichier sécurisé")

        def save_access_password():
            access_password = access_password_entry.get()
            if len(access_password) < 8:
                messagebox.showwarning("Erreur", "Le mot de passe doit avoir au moins 8 caractères.")
                return
            # Sauvegarder la clé de chiffrement protégée par le mot de passe d'accès
            with open(os.path.expanduser("~/encryption_key.txt"), "wb") as key_file:
                key_file.write(key)
            window.destroy()
            messagebox.showinfo("Succès", "Le mot de passe a été sauvegardé dans un fichier sécurisé.")

        # Widgets
        instruction = ctk.CTkLabel(window, text="Créez un mot de passe d'accès au fichier sécurisé :", font=("Helvetica", 14))
        instruction.pack(pady=10)
        access_password_entry = ctk.CTkEntry(window, show="*", font=("Helvetica", 14))
        access_password_entry.pack(pady=10)
        save_button = ctk.CTkButton(window, text="Enregistrer", command=save_access_password)
        save_button.pack(pady=10)

    # Fonction pour confirmer l'utilisation du mot de passe
    def confirm_use_password():
        password = password_display.cget("text")
        if not password:
            messagebox.showwarning("Erreur", "Aucun mot de passe n'a été généré.")
        else:
            save_password(password)

    # Boutons de confirmation
    confirm_label = ctk.CTkLabel(container, text="Vous utiliserez ce mot de passe ?", font=("Helvetica", 14), text_color="lightgray")
    confirm_button_yes = ctk.CTkButton(container, text="Oui", command=confirm_use_password, fg_color="#4CAF50")
    confirm_button_no = ctk.CTkButton(container, text="Non", command=lambda: messagebox.showinfo("Info", "Mot de passe non sauvegardé."))