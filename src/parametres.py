import customtkinter as ctk
from PIL import Image
from apropos import show_about_page

def show_settings_page(return_to_menu):
    # Initialisation de la fenêtre
    settings_window = ctk.CTk()
    settings_window.title("Paramètres")

    # Dimensions de la fenêtre
    window_width, window_height = 500, 400
    screen_width, screen_height = settings_window.winfo_screenwidth(), settings_window.winfo_screenheight()
    x_position, y_position = (screen_width // 2) - (window_width // 2), (screen_height // 2) - (window_height // 2)
    settings_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Couleur de fond
    settings_window.config(bg="#2e2e2e")

    # Titre principal
    title_label = ctk.CTkLabel(settings_window, text="Paramètres", font=("Helvetica", 24, "bold"), text_color="white")
    title_label.grid(row=0, column=0, columnspan=2, pady=20)

    # Ligne de séparation
    separator = ctk.CTkFrame(settings_window, height=2, fg_color="#4CAF50")
    separator.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

    # Option 1 : Changer le thème (clair/sombre)
    theme_label = ctk.CTkLabel(settings_window, text="Changer le thème :", font=("Helvetica", 16), text_color="white")
    theme_label.grid(row=2, column=0, sticky="w", padx=20, pady=10)

    theme_button = ctk.CTkSwitch(settings_window, text="Thème sombre", onvalue="dark", offvalue="light",
                                  command=lambda: ctk.set_appearance_mode("dark" if theme_button.get() == "dark" else "light"))
    theme_button.grid(row=2, column=1, sticky="e", padx=20)

    # Option 2 : Changer la taille de la police
    font_label = ctk.CTkLabel(settings_window, text="Taille de la police :", font=("Helvetica", 16), text_color="white")
    font_label.grid(row=3, column=0, sticky="w", padx=20, pady=10)

    font_size_slider = ctk.CTkSlider(settings_window, from_=12, to=24, command=lambda value: update_font_size(value))
    font_size_slider.set(14)  # Taille par défaut
    font_size_slider.grid(row=3, column=1, sticky="e", padx=20)

    # Fonction pour mettre à jour la taille de la police
    def update_font_size(size):
        new_font = ("Helvetica", int(size))
        title_label.configure(font=new_font)
        theme_label.configure(font=new_font)
        font_label.configure(font=new_font)

    # Option 3 : À propos
    about_image = Image.open("image/about.png").resize((30, 30))  # Redimensionner l'image
    about_ctk_image = ctk.CTkImage(about_image, size=(30, 30))

    about_label = ctk.CTkButton(settings_window, text="À propos", image=about_ctk_image, compound="left", 
                                command=lambda: [settings_window.destroy(), show_about_page(return_to_menu)],
                                fg_color="#4CAF50", text_color="white", hover_color="#45a049")
    about_label.grid(row=4, column=0, columnspan=2, pady=20)

    # Bouton retour
    back_button = ctk.CTkButton(settings_window, text="Retour", command=lambda: [settings_window.destroy(), return_to_menu()],
                                fg_color="#FF6347", text_color="white", hover_color="#FF4500")
    back_button.grid(row=5, column=0, columnspan=2, pady=20)

    settings_window.mainloop()


"""
def show_settings(content_frame):
    Affiche la page des paramètres.
    for widget in content_frame.winfo_children():
        widget.destroy()

    settings_label = ctk.CTkLabel(
        content_frame,
        text="Page des paramètres",
        font=("Helvetica", 24, "bold"),
        text_color="white",
    )
    settings_label.pack(pady=20)

    back_button = ctk.CTkButton(
        content_frame,
        text="Retour à l'accueil",
        command=lambda: navigate_to_page(content_frame, show_default_page),
        fg_color="#2e2e2e",
        hover_color="#3e3e3e",
        corner_radius=10,
        font=("Helvetica", 16),
        height=40
    )
    back_button.pack(pady=10)

"""