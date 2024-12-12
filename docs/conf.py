# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath('../GULib-master'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'OpenGU'
copyright = '2024, Bowen Fan, Yuming Ai, Zhilin Guo'
author = 'Bowen Fan, Yuming Ai, Zhilin Guo'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

source_suffix = {
    '.rst': 'restructuredtext'
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Autodoc
autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'no-inherited-members': True,
    'show-inheritance': True,
    'property-doc-from-class': True
}


# Napoleon
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_title = "OpenGU Documentation"

# html_logo = "path/to/logo.png"
# html_favicon = "path/to/favicon.ico"
