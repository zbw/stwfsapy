# Configuration file for the Sphinx documentation builder.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

# -- Path setup --------------------------------------------------------------

import os
import re
import sys

sys.path.insert(0, os.path.abspath("../.."))

# -- Project information

project = 'stwfsapy'
copyright = '2020-2025, AutoSE'
author = 'AutoSE'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    "sphinx_autodoc_typehints",
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

# -- autodoc

autoclass_content = "both" 
autodoc_typehints = "none"
