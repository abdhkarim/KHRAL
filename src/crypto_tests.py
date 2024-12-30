import customtkinter as ctk
from tkinter import messagebox

def show_crypto_tests_page(container):
    """
    Affiche la page pour tester les failles cryptographiques.
    """
    # Nettoyer le conteneur
    for widget in container.winfo_children():
        widget.destroy()

    # Titre de la page
    title_label = ctk.CTkLabel(
        container, text="Tests Cryptographiques", font=("Helvetica", 20, "bold"), text_color="white"
    )
    title_label.pack(pady=20)

    # Description
    description_label = ctk.CTkLabel(
        container,
        text="Cette section teste les failles courantes liées aux pratiques cryptographiques, "
             "comme les clés faibles ou les mauvais algorithmes.",
        font=("Helvetica", 14),
        text_color="lightgray",
        wraplength=600,
        justify="left"
    )
    description_label.pack(pady=10)

    # Bouton pour exécuter les tests
    def run_crypto_test():
        try:
            # Simuler un test cryptographique
            result = "Faille détectée : clé trop courte (64 bits)."
            messagebox.showinfo("Résultat du test", result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

    test_button = ctk.CTkButton(
        container,
        text="Lancer les tests cryptographiques",
        command=run_crypto_test,  # Correctement défini
        fg_color="#0078D7",
        hover_color="#005A9E",
        corner_radius=10,
        font=("Helvetica", 16),
        height=40
    )
    test_button.pack(pady=20)