import customtkinter as ctk
from PIL import Image
from apropos import show_about_page

def show_settings_page(container):
    """Affiche la page des paramètres dans le conteneur donné."""
    # Effacer le contenu existant dans le conteneur
    for widget in container.winfo_children():
        widget.destroy()

    # Colonne pour les options
    settings_frame = ctk.CTkFrame(container, fg_color="#1e1e1e", width=300)
    settings_frame.pack(side="left", fill="y", padx=10, pady=10)

    # Titre de la page des paramètres
    title_label = ctk.CTkLabel(settings_frame, text="Paramètres", text_color="white", font=("Helvetica", 24, "bold"))
    title_label.pack(pady=20)

    # Section pour changer le thème (clair/sombre)
    theme_label = ctk.CTkLabel(settings_frame, text="Changer le thème :", text_color="white", font=("Helvetica", 16))
    theme_label.pack(pady=10)

    theme_button = ctk.CTkSwitch(settings_frame, text="Thème sombre", onvalue="dark", offvalue="light",
                                  command=lambda: ctk.set_appearance_mode("dark" if theme_button.get() == "dark" else "light"))
    theme_button.pack(pady=10)

    # Section pour changer la taille de la police
    font_label = ctk.CTkLabel(settings_frame, text="Taille de la police :", text_color="white", font=("Helvetica", 16))
    font_label.pack(pady=10)

    font_size_slider = ctk.CTkSlider(settings_frame, from_=12, to=24, command=lambda value: update_font_size(value))
    font_size_slider.set(14)  # Taille de police par défaut
    font_size_slider.pack(pady=10)

    # Fonction pour mettre à jour la taille de la police
    def update_font_size(size):
        new_font = ("Helvetica", int(size))
        title_label.configure(font=new_font)
        theme_label.configure(font=new_font)
        font_label.configure(font=new_font)

    # Zone de documentation
    documentation_label = ctk.CTkLabel(
        settings_frame,
        text="Documentation des Paramètres :\n\n"
             "1. Changer le thème : Permet de basculer entre un thème clair et un thème sombre.\n"
             "2. Taille de la police : Permet d'ajuster la taille de la police des éléments de l'interface.",
        font=("Helvetica", 12),
        text_color="lightgray",
        anchor="w"
    )
    documentation_label.pack(pady=20)

    # Bouton À propos
    about_image = Image.open("assets/about.png").resize((30, 30))  # Redimensionner l'image
    about_ctk_image = ctk.CTkImage(about_image, size=(30, 30))

    about_button = ctk.CTkButton(settings_frame, text="À propos", image=about_ctk_image, compound="left", 
                                 command=lambda: [container.destroy(), show_about_page],
                                 fg_color="#4CAF50", text_color="white", hover_color="#45a049")
    about_button.pack(pady=20)

    # Bouton de retour au menu principal
    back_button = ctk.CTkButton(settings_frame, text="Retour", command=lambda: [container.destroy()],
                                 fg_color="#FF6347", text_color="white", hover_color="#FF4500")
    back_button.pack(pady=20)