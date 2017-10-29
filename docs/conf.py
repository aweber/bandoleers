# -*- coding: utf-8 -*-
import sphinx_rtd_theme
import bandoleers

project = 'bandoleers'
copyright = 'AWeber Communications, Inc.'
version = bandoleers.__version__
release = '.'.join(str(v) for v in bandoleers.version_info[0:2])

needs_sphinx = '1.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

templates_path = []
source_suffix = '.rst'
source_encoding = 'utf-8-sig'
master_doc = 'index'
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = []

intersphinx_mapping = {
    'python': ('http://docs.python.org/3/', None),
    'rejected': ('http://rejected.readthedocs.org/en/latest/', None),
    'consulate': ('http://consulate.readthedocs.org/en/latest/', None),
    'datastax': ('http://datastax.github.io/python-driver', None),
    'requests': ('http://requests.readthedocs.io/en/master/', None),
}
