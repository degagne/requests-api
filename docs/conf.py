import os
import sys
import datetime as dt

sys.path.insert(0, os.path.abspath(".."))

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
    "sphinx_rtd_theme"
]

source_suffix = ".rst"
master_doc = "index"

project = u"requests-api"
copyright = "{}, Deric Degagne".format(dt.date.today().year)

exclude_patterns = ["_build"]

html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]

html_css_files = [
    "custom.css"
]