import customtkinter as ctk

def show_general_scanner_page(return_to_menu):
    window = ctk.CTk()
    window.title("Scanner Général")

    label = ctk.CTkLabel(window, text="Scanner Général", font=("Helvetica", 20, "bold"))
    label.pack(pady=20)

    # Saisie URL
    url_entry = ctk.CTkEntry(window, placeholder_text="Entrez l'URL cible")
    url_entry.pack(pady=10)

    # Résultats
    results_text = ctk.CTkTextbox(window, height=300, width=500)
    results_text.pack(pady=10)

    # Bouton pour scanner
    scan_button = ctk.CTkButton(
        window, text="Scanner", command=lambda: general_scan(url_entry.get(), results_text)
    )
    scan_button.pack(pady=10)

    # Bouton retour
    back_button = ctk.CTkButton(window, text="Retour", command=lambda: [window.destroy(), return_to_menu()])
    back_button.pack(pady=10)

    window.mainloop()

def general_scan(url, results_text):
    results_text.insert("end", f"Scan général de {url}...\n")
    # Ajoutez ici la logique pour détecter les vulnérabilités (basé sur OWASP ZAP).
