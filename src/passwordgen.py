import os
from cryptography.fernet import Fernet
import customtkinter as ctk
from tkinter import messagebox
import hashlib
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

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
        # Créer le dossier "passwords" dans le répertoire actuel
        passwords_dir = os.path.join(os.getcwd(), "passwords")
        if not os.path.exists(passwords_dir):
            os.makedirs(passwords_dir)

        # Clé pour chiffrer le fichier
        key = Fernet.generate_key()
        cipher = Fernet(key)
        encrypted_password = cipher.encrypt(password.encode())

        # Chemin du fichier
        file_path = os.path.join(passwords_dir, "secure_passwords.txt")

        # Sauvegarde du fichier chiffré
        with open(file_path, "wb") as file:
            file.write(encrypted_password)

        # Demande de mot de passe pour déchiffrer
        decrypt_password_window(key, passwords_dir)

    # Fonction pour créer un mot de passe d'accès au fichier
    def decrypt_password_window(key, passwords_dir):
        window = ctk.CTkToplevel()
        window.geometry("400x300")
        window.title("Mot de passe pour fichier sécurisé")

        def save_access_password():
            access_password = access_password_entry.get()
            if len(access_password) < 8:
                messagebox.showwarning("Erreur", "Le mot de passe doit avoir au moins 8 caractères.")
                return

            # Utiliser PBKDF2 pour dériver une clé de 32 octets à partir du mot de passe
            salt = os.urandom(16)  # Sel aléatoire pour chaque mot de passe
            kdf = PBKDF2HMAC(
                algorithm=hashlib.sha256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            access_key = base64.urlsafe_b64encode(kdf.derive(access_password.encode()))

            # Chiffrer la clé de chiffrement avec la clé d'accès
            fernet_access_key = Fernet(access_key)
            encrypted_key = fernet_access_key.encrypt(key)

            # Sauvegarder la clé chiffrée dans le dossier "passwords"
            key_file_path = os.path.join(passwords_dir, "encryption_key.txt")
            with open(key_file_path, "wb") as key_file:
                key_file.write(encrypted_key)
            window.destroy()
            messagebox.showinfo("Succès", "Le mot de passe a été sauvegardé dans le dossier 'passwords'.")

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