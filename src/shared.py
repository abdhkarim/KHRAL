from tkinter import messagebox

def clear_container(container):
    """
    Efface tous les widgets à l'intérieur d'un conteneur donné.
    """
    for widget in container.winfo_children():
        widget.destroy()

def navigate_to_page(container, page_function):
    """
    Navigue vers une autre page en effaçant le contenu actuel du conteneur.
    Affiche un message d'erreur si la page échoue à se charger.
    """
    clear_container(container)  # Utilisation de la fonction clear_container

    try:
        page_function(container)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de charger la page : {e}")