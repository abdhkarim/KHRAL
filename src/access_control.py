import customtkinter as ctk
import requests
from tkinter import messagebox
import webbrowser

# Fonction pour afficher la page des tests Broken Access Control
def show_access_control_page(container):
    """Affiche la page pour vérifier les Broken Access Control."""
    # Effacer le contenu existant dans le conteneur
    for widget in container.winfo_children():
        widget.destroy()

    # Colonne pour l'historique
    vuln_list_frame = ctk.CTkFrame(container, fg_color="#1e1e1e", width=300)
    vuln_list_frame.pack(side="left", fill="y", padx=10, pady=10)

    vuln_list_label = ctk.CTkLabel(vuln_list_frame, text="Historique des vulnérabilités", text_color="white", font=("Helvetica", 16))
    vuln_list_label.pack(pady=10)

    vuln_list = ctk.CTkTextbox(vuln_list_frame, fg_color="#2e2e2e", text_color="white", font=("Helvetica", 14), wrap="none", state="disabled")
    vuln_list.pack(fill="both", expand=True)

    # Zone principale
    main_frame = ctk.CTkFrame(container, fg_color="#2e2e2e")
    main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # Barre pour entrer l'URL
    url_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    url_frame.pack(pady=5, padx=20, anchor="n", fill="x")

    url_label = ctk.CTkLabel(url_frame, text="Entrez l'URL :", text_color="white", font=("Helvetica", 14))
    url_label.pack(side="left", padx=5)

    url_entry = ctk.CTkEntry(url_frame, font=("Helvetica", 14), width=400)
    url_entry.pack(side="left", padx=5, fill="x", expand=True)

    # Section pour les choix d'accès
    choices_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    choices_frame.pack(pady=5, padx=20, anchor="n", fill="x")

    # Texte d'instructions et options
    choices_label = ctk.CTkLabel(
        choices_frame,
        text="Choisir un type d'accès (horizontal, vertical, ou non authentifié) en défilant la liste ci-dessous :",
        text_color="white",
        font=("Helvetica", 14),
    )
    choices_label.pack(anchor="nw", padx=5, pady=5)

    choices_textbox = ctk.CTkTextbox(
        choices_frame,
        fg_color="#1e1e1e",
        text_color="white",
        font=("Helvetica", 14),
        height=5,  # Hauteur pour afficher toutes les options
        wrap="word",
        state="normal",  # Permet d'insérer le texte
    )
    choices_textbox.pack(fill="x", pady=5)  # Remplissage horizontal
    choices_textbox.insert(
        "end",
        "1. Accès Horizontal\n"
        "2. Accès Vertical\n"
        "3. Accès Non Authentifié",
    )
    choices_textbox.configure(state="disabled")  # Désactivé pour empêcher les modifications

    # Entrée pour le choix
    choice_entry = ctk.CTkEntry(
        choices_frame,
        font=("Helvetica", 14),
        width=100,
        placeholder_text="Ex: 1",  # Indication pour l'utilisateur
    )
    choice_entry.pack(anchor="nw", pady=5, padx=5)  # Placé directement après le texte

    # Zone des résultats
    results_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    results_frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Fenêtre vierge pour afficher les résultats
    results_textbox = ctk.CTkTextbox(
        results_frame,
        fg_color="#1e1e1e",
        text_color="white",
        font=("Helvetica", 14),
        wrap="word",
        state="normal",
    )
    results_textbox.pack(fill="both", pady=10, padx=20, expand=True)
    results_textbox.configure(state="disabled")  # Initialement désactivé pour être vide

    # Boutons en bas
    bottom_frame = ctk.CTkFrame(main_frame, fg_color="#2e2e2e")
    bottom_frame.pack(side="bottom", fill="x", pady=10, padx=20)

    # Documentation bouton
    def open_documentation():
        webbrowser.open("https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/06-Testing_for_Broken_Access_Control")

    doc_button = ctk.CTkButton(bottom_frame, text="Documentation", command=open_documentation, width=150, height=40)
    doc_button.pack(side="left", padx=5)

    # Bouton pour lancer le test
    test_button = ctk.CTkButton(
        bottom_frame,
        text="Tester",
        command=lambda: display_access_control_choices(results_textbox, vuln_list, choice_entry, test_button, url_entry.get()),
        fg_color="#4CAF50",
        hover_color="#388E3C",
        text_color="white",
        corner_radius=10,
        font=("Helvetica", 16),
        height=40,
    )
    test_button.pack(side="right", padx=5)


def display_access_control_choices(results_textbox, vuln_list, choice_entry, test_button, url, choice):
    """Affiche les résultats du test d'accès en fonction du choix de l'utilisateur."""
    results_textbox.configure(state="normal")
    results_textbox.delete("1.0", "end")
    
    try:
        if choice == "1":  # Accès Horizontal
            results = test_horizontal_access(url)
        elif choice == "2":  # Accès Vertical
            results = test_vertical_access(url)
        elif choice == "3":  # Accès Non Authentifié
            results = test_unauthenticated_access(url)
        else:
            results = "Choix invalide. Veuillez entrer 1, 2 ou 3."

        results_textbox.insert("end", results + "\n")
        vuln_list.insert("end", results + "\n")
    except Exception as e:
        results_textbox.insert("end", f"Erreur lors du test : {str(e)}\n")
    results_textbox.configure(state="disabled")


def test_horizontal_access(url):
    user_ids = [123, 124, 125, 126]  # Liste des IDs à tester
    results = []

    for user_id in user_ids:
        # Modifier l'URL pour tester chaque ID
        test_url = f"{url}?id={user_id}"
        response = requests.get(test_url)

        # Si la réponse indique que l'utilisateur n'est pas autorisé à accéder à cette page
        if "Unauthorized" in response.text or response.status_code == 403:
            results.append(f"Accès bloqué pour l'ID {user_id}.")
        else:
            results.append(f"Accès autorisé pour l'ID {user_id} (problème d'accès horizontal).")
    
    return "\n".join(results)


def test_vertical_access(url):
    """Test d'accès vertical."""
    # Logique pour tester l'accès vertical
    return f"Test d'accès vertical effectué sur {url}."


def test_unauthenticated_access(url):
    """Test d'accès non authentifié."""
    # Logique pour tester l'accès non authentifié
    return f"Test d'accès non authentifié effectué sur {url}."