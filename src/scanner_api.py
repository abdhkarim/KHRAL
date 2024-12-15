import customtkinter as ctk

def show_api_scanner_page(return_to_menu):
    window = ctk.CTk()
    window.title("Scanner API")

    label = ctk.CTkLabel(window, text="Scanner API", font=("Helvetica", 20, "bold"))
    label.pack(pady=20)

    # Zone de saisie URL
    url_entry = ctk.CTkEntry(window, placeholder_text="Entrez l'URL de l'API")
    url_entry.pack(pady=10)

    # Zone de résultats
    results_text = ctk.CTkTextbox(window, height=300, width=500)
    results_text.pack(pady=10)

    # Bouton pour scanner
    scan_button = ctk.CTkButton(window, text="Scanner", command=lambda: scan_api(url_entry.get(), results_text))
    scan_button.pack(pady=10)

    # Bouton pour revenir au menu
    back_button = ctk.CTkButton(window, text="Retour", command=lambda: [window.destroy(), return_to_menu()])
    back_button.pack(pady=10)

    window.mainloop()

def scan_api(url, results_text):
    results_text.insert("end", f"Scanning {url}...\n")
