def navigate_to_page(container, page_function):
    """
    Navigue vers une autre page en effaçant le contenu actuel du conteneur.
    """
    for widget in container.winfo_children():
        widget.destroy()
    page_function(container)