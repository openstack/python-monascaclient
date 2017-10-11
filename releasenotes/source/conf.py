# -*- coding: utf-8 -*-

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.6'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'openstackdocstheme',
    'reno.sphinxext'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
repository_name = u'openstack/python-monascaclient'
project = u'Monasca Client ReleaseNotes Docs'

# Release notes do not need a version number in the title, they
# cover multiple releases.
version = ''
release = ''
bug_project = u'880'
bug_tag = u''
copyright = u'2014-present, OpenStack Foundation'
author = u'OpenStack Foundation'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'openstackdocs'

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%Y-%m-%d %H:%M'

# Output file base name for HTML help builder.
htmlhelp_basename = 'MonascaClientReleaseNotesDoc'

# -- Options for LaTeX output ---------------------------------------------

latex_documents = [(
     master_doc, 'MonascaClientReleaseNotes.tex',
     u'Monasca Client Release Notes', [author],
     'manual'
)]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'monascaclientreleasenotes',
     u'Monasca Client Release Notes', [author],
     1)
]

# -- Options for Internationalization output ------------------------------
locale_dirs = ['locale/']
