from tkinter import messagebox

def navigate_to_page(container, page_function):
    """
    Navigue vers une autre page en effaçant le contenu actuel du conteneur.
    Affiche un message d'erreur si la page échoue à se charger.
    """
    for widget in container.winfo_children():
        widget.destroy()

    try:
        page_function(container)
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de charger la page : {e}")