import customtkinter as ctk
import requests
from tkinter import messagebox


def show_access_control_page(content_frame):
    """Affiche la page pour vérifier les Broken Access Control."""
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Titre de la page
    label = ctk.CTkLabel(
        content_frame,
        text="Vérification des Broken Access Control",
        font=("Helvetica", 24, "bold"),
        text_color="white"
    )
    label.pack(pady=20)

    # URL cible
    url_label = ctk.CTkLabel(content_frame, text="Entrez l'URL cible :", font=("Helvetica", 14), text_color="lightgray")
    url_label.pack(pady=5)
    url_entry = ctk.CTkEntry(content_frame, width=400, font=("Helvetica", 14))
    url_entry.pack(pady=5)

    # Sélection du type de test
    test_type_label = ctk.CTkLabel(content_frame, text="Choisissez le type de test :", font=("Helvetica", 14), text_color="lightgray")
    test_type_label.pack(pady=5)

    test_type_var = ctk.StringVar(value="horizontal")
    horizontal_radio = ctk.CTkRadioButton(content_frame, text="Accès Horizontal", variable=test_type_var, value="horizontal")
    vertical_radio = ctk.CTkRadioButton(content_frame, text="Accès Vertical", variable=test_type_var, value="vertical")
    unauth_radio = ctk.CTkRadioButton(content_frame, text="Accès Non Authentifié", variable=test_type_var, value="unauth")

    horizontal_radio.pack(pady=5)
    vertical_radio.pack(pady=5)
    unauth_radio.pack(pady=5)

    # Résultats
    results_textbox = ctk.CTkTextbox(content_frame, height=200, font=("Helvetica", 14))
    results_textbox.pack(pady=10, padx=10, fill="both", expand=True)

    # Bouton pour lancer le test
    def run_test():
        url = url_entry.get()
        test_type = test_type_var.get()

        if not url:
            messagebox.showerror("Erreur", "Veuillez entrer une URL valide.")
            return

        results_textbox.delete("1.0", "end")
        results_textbox.insert("end", f"Test en cours sur {url}...\n")

        try:
            if test_type == "horizontal":
                results = test_horizontal_access(url)
            elif test_type == "vertical":
                results = test_vertical_access(url)
            elif test_type == "unauth":
                results = test_unauthenticated_access(url)
            else:
                results = "Type de test invalide."

            results_textbox.insert("end", results + "\n")
        except Exception as e:
            results_textbox.insert("end", f"Erreur lors du test : {str(e)}\n")

    test_button = ctk.CTkButton(
        content_frame, text="Lancer le Test", command=run_test, fg_color="#4CAF50", hover_color="#388E3C", font=("Helvetica", 16)
    )
    test_button.pack(pady=10)
