# -*- coding: utf-8 -*-

import os
import sys

from monascaclient.version import version_info

sys.path = [
    os.path.abspath('../..'),
    os.path.abspath('../../bin')
] + sys.path

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.6'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.graphviz',
    'sphinx.ext.viewcode',
    'openstackdocstheme'
]

# geeneral information about project
repository_name = u'openstack/python-monascaclient'
project = u'Monasca Client Dev Docs'
version = version_info.canonical_version_string()
release = version_info.version_string_with_vcs()
bug_project = u'880'
bug_tag = u''
copyright = u'2014-present, OpenStack Foundation'
author = u'OpenStack Foundation'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = [
    'common',
    'doc',
    'documentation',
    'etc',
    'java'
]

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
show_authors = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'openstackdocs'

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%Y-%m-%d %H:%M'

# If false, no index is generated.
html_use_index = True

# If false, no module index is generated.
html_use_modindex = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'python-monascaclientdoc'

# -- Options for LaTeX output ---------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  (master_doc, 'python-monascaclient.tex', u'python-monascaclient Documentation',
   u'Openstack Foundation \\textless{}monasca@lists.launchpad.net\\textgreater{}', 'manual'),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'python-monascaclient', u'python-monascaclient Documentation',
     [author], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  (master_doc, 'python-monascaclient', u'python-monascaclient Documentation',
   author, 'python-monascaclient', 'Rest-API to collect logs from your cloud.',
   'Miscellaneous'),
]

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://doc.python.org/': None}
