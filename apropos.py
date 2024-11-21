import customtkinter as ctk

def show_about_page(return_to_menu):
    about_window = ctk.CTk()
    about_window.title("À propos - KHRAL")
    
    # Dimensions de la fenêtre
    window_width = 400
    window_height = 200
    
    # Obtenir les dimensions de l'écran
    screen_width = about_window.winfo_screenwidth()
    screen_height = about_window.winfo_screenheight()
    
    # Calculer la position pour centrer la fenêtre
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    
    # Définir la géométrie avec position centrée
    about_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    # Contenu de la fenêtre
    about_label = ctk.CTkLabel(about_window, text="KHRAL - Version 1.0.0\nMerci d'utiliser notre application!",
                               font=("Helvetica", 14), text_color="white")
    about_label.pack(pady=50)

    return_button = ctk.CTkButton(about_window, text="Retour", command=lambda: [about_window.destroy(), return_to_menu()])
    return_button.pack(pady=10)

    about_window.mainloop()
