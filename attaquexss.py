import tkinter as tk
from tkinter import messagebox
import requests
import json
import customtkinter as ctk


"""________________________________________________________________________________________________________________"""

def get_ip():
    try:
        response = requests.get("https://api.ipify.org")
        ip = response.text
        return ip
    except requests.exceptions.RequestException:
        return "IP non disponible"
    
def load_payloads(file_path):
    """Charge les payloads depuis un fichier JSON."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Retourne une liste vide si le fichier est introuvable
    except json.JSONDecodeError:
        return []  # Retourne une liste vide si le JSON est invalide
    

"""________________________________________________________________________________________________________________"""

def test_xss(url, results_text):
    """
    Teste la vulnérabilité XSS en injectant des payloads dans l'URL.
    """
    payloads = load_payloads("payloads/payloadXSS.json")  # Charger les payloads depuis un fichier JSON

    if not payloads:
        results_text.insert(tk.END, "Aucun payload disponible.\n")
        return

    results_text.delete("1.0", tk.END)
    vulnerable = False  # Indique si une vulnérabilité a été détectée

    for payload_data in payloads:
        # Récupération des détails du payload
        payload = payload_data.get("Payload", "")
        attributes = payload_data.get("Attribute", [])
        count = payload_data.get("count", 0)
        waf = payload_data.get("waf", None)

        # Construire l'URL de test
        test_url = f"{url}{payload}"

        try:
            # Envoyer une requête HTTP GET
            response = requests.get(test_url)

            # Vérifier si le payload apparaît dans la réponse
            if payload in response.text:
                vulnerable = True
                results_text.insert(
                    tk.END,
                    f"Vulnérable avec le payload : {payload}\n"
                    f"Attributs : {', '.join(attributes)}\n"
                    f"WAF détecté : {waf if waf else 'Non détecté'}\n"
                )
                # Mettre à jour le compteur d'utilisation
                payload_data["count"] = count + 1
            else:
                results_text.insert(tk.END, f"Payload non vulnérable : {payload}\n")

        except Exception as e:
            results_text.insert(tk.END, f"Erreur lors de la requête : {e}\n")
            return

    if not vulnerable:
        results_text.insert(tk.END, "Aucune vulnérabilité détectée.\n")

    # Sauvegarder les mises à jour des payloads
    save_payloads("xss_payloads.json", payloads)


def save_payloads(file_path, payloads):
    """
    Sauvegarde les payloads dans un fichier JSON après mise à jour.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(payloads, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des payloads : {e}")

"""________________________________________________________________________________________________________________"""

def show_xss_page(back_to_menu):
    """Show the XSS Attack page."""
    sql_window = tk.Tk()
    sql_window.title("KHRAL - Attaque XSS")
    
    # Définir la taille de la fenêtre
    window_width = 1000
    window_height = 700
    
    # Récupérer les dimensions de l'écran
    screen_width = sql_window.winfo_screenwidth()
    screen_height = sql_window.winfo_screenheight()

    # Calculer les coordonnées pour centrer la fenêtre
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)

    # Positionner la fenêtre au centre de l'écran
    sql_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    sql_window.config(bg="#2e2e2e")  # Fond sombre pour un look moderne

    # Configurer une seule colonne pour tout centrer
    sql_window.grid_columnconfigure(0, weight=1)

    # Titre au centre
    title_label = tk.Label(sql_window, text="Attaque XSS", font=("Helvetica", 32, "bold"), fg="white", bg="#2e2e2e")
    title_label.grid(row=0, column=0, pady=20, sticky="n")

    # Zone d'entrée pour l'URL
    url_label = tk.Label(sql_window, text="Entrez l'URL à tester :", font=("Helvetica", 14), fg="white", bg="#2e2e2e")
    url_label.grid(row=1, column=0, pady=10, sticky="n")

    url_entry = tk.Entry(sql_window, font=("Helvetica", 14), width=40)
    url_entry.grid(row=2, column=0, pady=10, sticky="n")

    # Zone de texte pour afficher les résultats
    results_text = tk.Text(sql_window, height=15, width=70, font=("Helvetica", 14))
    results_text.grid(row=3, column=0, pady=10, sticky="n")


# Bouton pour tester l'attaque XSS
    test_button = ctk.CTkButton(sql_window, 
                                text="Tester l'attaque XSS", 
                                font=("Helvetica", 14), 
                                fg_color="#4CAF50",  # Couleur de fond
                                hover_color="#45a049",  # Couleur au survol
                                text_color="black",  # Couleur du texte
                                command=lambda: test_xss(url_entry.get(), results_text),
                                width=200,  # Largeur du bouton
                                height=50,  # Hauteur du bouton
                                corner_radius=10)  # Coins arrondis
    test_button.grid(row=4, column=0, pady=10, sticky="n")

# Bouton pour revenir au menu principal (style similaire au premier)
    back_button = ctk.CTkButton(sql_window, 
                                text="Retour", 
                                font=("Helvetica", 14), 
                                fg_color="red",  # Même couleur de fond que pour le premier bouton
                                hover_color="#45a049",  # Même couleur au survol
                                text_color="black",  # Même couleur de texte
                                command=lambda: [sql_window.destroy(), back_to_menu()],
                                width=200,  # Largeur du bouton
                                height=50,  # Hauteur du bouton
                                corner_radius=10)  # Coins arrondis
    back_button.grid(row=5, column=0, pady=10, sticky="n")

    sql_window.mainloop()
