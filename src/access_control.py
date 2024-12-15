import customtkinter as ctk

def show_access_control_page(return_to_menu):
    window = ctk.CTk()
    window.title("Contrôle des Autorisations")

    label = ctk.CTkLabel(window, text="Contrôle des Autorisations", font=("Helvetica", 20, "bold"))
    label.pack(pady=20)

    # Zone de saisie
    url_entry = ctk.CTkEntry(window, placeholder_text="Entrez l'URL ou chemin à vérifier")
    url_entry.pack(pady=10)

    # Résultats
    results_text = ctk.CTkTextbox(window, height=300, width=500)
    results_text.pack(pady=10)

    # Bouton de vérification
    check_button = ctk.CTkButton(
        window, text="Vérifier", command=lambda: check_access_control(url_entry.get(), results_text)
    )
    check_button.pack(pady=10)

    # Bouton retour
    back_button = ctk.CTkButton(window, text="Retour", command=lambda: [window.destroy(), return_to_menu()])
    back_button.pack(pady=10)

    window.mainloop()

def check_access_control(url, results_text):
    results_text.insert("end", f"Vérification des autorisations pour {url}...\n")
    # Ajoutez ici le code de détection des failles (Broken Access Control).
