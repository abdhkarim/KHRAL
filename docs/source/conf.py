# Configuration file for the Sphinx documentation builder.
# Documentation: https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
project = 'KHRAL'
copyright = '2025, Karim Abdallah'
author = 'Karim Abdallah'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',  # Génération automatique de documentation à partir des docstrings
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for autodoc -----------------------------------------------------
# Ajoutez des options ici si nécessaire, par exemple :
# autodoc_default_options = {
#     'members': True,
#     'undoc-members': True,
#     'private-members': True,
# }

# -- Options for HTML output -------------------------------------------------
import sphinx_pdj_theme
html_theme = 'sphinx_pdj_theme'
html_theme_path = [sphinx_pdj_theme.get_html_theme_path()]

# -- Path setup --------------------------------------------------------------
import os
import sys
# Ajoute le dossier parent du dossier 'src' au chemin d'accès pour que Sphinx puisse importer correctement les modules
sys.path.insert(0, os.path.abspath('../src/'))  # Ajustez ce chemin si nécessaire