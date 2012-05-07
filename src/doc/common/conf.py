import sys, os, sphinx

SAGE_ROOT = os.environ['SAGE_ROOT']
SAGE_DOC = os.path.join(SAGE_ROOT, 'devel/sage/doc')

def get_doc_abspath(path):
    """
    return the absolute path from a SAGE_DOC relative path
    """
    return os.path.abspath(os.path.join(SAGE_DOC, path))

# If your extensions are in another directory, add it here. If the directory
# is relative to the documentation root, use get_doc_abspath to make it
# absolute, like shown here.
sys.path.append(get_doc_abspath('common'))

# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['inventory_builder', 'multidocs',
              'sage_autodoc',  'sphinx.ext.graphviz',
              'sphinx.ext.inheritance_diagram', 'sphinx.ext.todo',
              'sphinx.ext.extlinks']
# We do *not* fully initialize intersphinx since we call it by hand
# in find_sage_dangling_links.
#, 'sphinx.ext.intersphinx']


# Add any paths that contain templates here, relative to this directory.
templates_path = [os.path.join(SAGE_DOC, 'common/templates'), 'templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u""
copyright = u'2005--2011, The Sage Development Team'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
from sage.version import version
release = version

#version = '3.1.2'
# The full version, including alpha/beta/rc tags.
#release = '3.1.2'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ['.build']

# The reST default role (used for this markup: `text`) to use for all documents.
default_role = 'math'

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.  NOTE:
# This overrides a HTML theme's corresponding setting (see below).
pygments_style = 'sphinx'

# GraphViz includes dot, neato, twopi, circo, fdp.
graphviz_dot = 'dot'
inheritance_graph_attrs = { 'rankdir' : 'BT' }
inheritance_node_attrs = { 'height' : 0.5, 'fontsize' : 12, 'shape' : 'oval' }
inheritance_edge_attrs = {}

# Extension configuration
# -----------------------

# include the todos
todo_include_todos = True


# Cross-links to other project's online documentation.
# intersphinx_mapping = {'http://docs.python.org/': None}
#intersphinx_mapping = {'python': ('http://docs.python.org/',
#                                  'python-inv.txt')}
intersphinx_mapping = {
    'http://docs.python.org/': get_doc_abspath('common/python.inv')}

def set_intersphinx_mappings(app):
    """
    Add reference's objects.inv to intersphinx if not compiling reference
    """
    app.config.intersphinx_mapping = intersphinx_mapping
    refpath = 'output/html/en/reference/'
    if not app.srcdir.endswith('reference'):
        app.config.intersphinx_mapping[get_doc_abspath(refpath)] = get_doc_abspath(refpath+'objects.inv')
pythonversion = sys.version.split(' ')[0]
# Python and Sage trac ticket shortcuts. For example, :trac:`7549` .

# Sage trac ticket shortcuts. For example, :trac:`7549` .
extlinks = {
    'python': ('http://docs.python.org/release/'+pythonversion+'/%s', ''),
    'trac': ('http://trac.sagemath.org/%s', 'trac ticket #'),
    'wikipedia': ('http://en.wikipedia.org/wiki/%s', 'Wikipedia article ')}

# Options for HTML output
# -----------------------

# HTML theme (e.g., 'default', 'sphinxdoc').  We use a custom Sage
# theme to set a Pygments style, stylesheet, and insert MathJax macros. See
# the directory doc/common/themes/sage/ for files comprising the custom Sage
# theme.
html_theme = 'sage'

# Theme options are theme-specific and customize the look and feel of
# a theme further.  For a list of options available for each theme,
# see the documentation.
html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = [os.path.join(SAGE_DOC, 'common/themes')]

# HTML style sheet NOTE: This overrides a HTML theme's corresponding
# setting.
#html_style = 'default.css'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (within the static path) to place at the top of
# the sidebar.
#html_logo = 'sagelogo-word.ico'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = 'favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = [os.path.join(SAGE_DOC, 'common/static'), 'static']

# We use MathJax to build the documentation unless the environment
# variable SAGE_DOC_MATHJAX is set to "no" or "False".  (Note that if
# the user does not set this variable, then the script sage-env sets
# it to "True".)

if (os.environ.get('SAGE_DOC_MATHJAX', 'no') != 'no'
            and os.environ.get('SAGE_DOC_MATHJAX', 'no') != 'False'):

    extensions.append('sphinx.ext.mathjax')
    mathjax_path = 'MathJax.js?config=TeX-AMS_HTML-full,../mathjax_sage.js'

    from sage.misc.latex_macros import sage_mathjax_macros
    html_theme_options['mathjax_macros'] = sage_mathjax_macros()

    from pkg_resources import Requirement, working_set
    sagenb_path = working_set.find(Requirement.parse('sagenb')).location
    mathjax_relative = os.path.join('sagenb','data','mathjax')

    # It would be really nice if sphinx would copy the entire mathjax directory,
    # (so we could have a _static/mathjax directory), rather than the contents of the directory

    mathjax_static = os.path.join(sagenb_path, mathjax_relative)
    html_static_path.append(mathjax_static)
    exclude_patterns=['**/'+os.path.join(mathjax_relative, i) for i in ('docs', 'README*', 'test',
                                                                        'unpacked', 'LICENSE')]
else:
     extensions.append('sphinx.ext.pngmath')


# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_use_modindex = True

# A list of prefixes that are ignored for sorting the Python module index ( if
# this is set to ['foo.'], then foo.bar is shown under B, not F). Works only
# for the HTML builder currently.
modindex_common_prefix = ['sage.']

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
html_split_index = True

# If true, the reST sources are included in the HTML build as _sources/<name>.
#html_copy_source = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
#htmlhelp_basename = ''


# Options for LaTeX output
# ------------------------
# See http://sphinx.pocoo.org/config.html#confval-latex_elements
latex_elements = {}

# Extended UTF-8 scheme
latex_elements['inputenc'] = '\\usepackage[utf8x]{inputenc}'

# Prevent Sphinx from by default inserting the following LaTeX
# declaration into the preamble of a .tex file:
#
# \DeclareUnicodeCharacter{00A0}{\nobreakspace}
#
# This happens in the file src/sphinx/writers/latex.py in the sphinx
# spkg.  This declaration is known to result in a failure to build the
# PDF version of a document in the Sage standard documentation. See
# ticket #8183 for further information on this issue.
latex_elements['utf8extra'] = ''

# The paper size ('letterpaper' or 'a4paper').
#latex_elements['papersize'] = 'letterpaper'

# The font size ('10pt', '11pt' or '12pt').
#latex_elements['pointsize'] = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
latex_documents = []

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = 'sagelogo-word.png'

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
latex_elements['preamble'] = '\usepackage{amsmath}\n\usepackage{amssymb}\n'

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True

#####################################################
# add LaTeX macros for Sage

from sage.misc.latex_macros import sage_latex_macros

try:
    pngmath_latex_preamble  # check whether this is already defined
except NameError:
    pngmath_latex_preamble = ""

for macro in sage_latex_macros():
    # used when building latex and pdf versions
    latex_elements['preamble'] += macro + '\n'
    # used when building html version
    pngmath_latex_preamble += macro + '\n'

#####################################################

def process_docstring_aliases(app, what, name, obj, options, docstringlines):
    """
    Change the docstrings for aliases to point to the original object.
    """
    basename = name.rpartition('.')[2]
    if hasattr(obj, '__name__') and obj.__name__ != basename:
        docstringlines[:] = ['See :obj:`%s`.' % name]

def process_directives(app, what, name, obj, options, docstringlines):
    """
    Remove 'nodetex' and other directives from the first line of any
    docstring where they appear.
    """
    if len(docstringlines) == 0:
        return
    first_line = docstringlines[0]
    directives = [ d.lower() for d in first_line.split(',') ]
    if 'nodetex' in directives:
        docstringlines.pop(0)

def process_docstring_cython(app, what, name, obj, options, docstringlines):
    """
    Remove Cython's filename and location embedding.
    """
    if len(docstringlines) <= 1:
        return

    first_line = docstringlines[0]
    if first_line.startswith('File:') and '(starting at' in first_line:
        #Remove the first two lines
        docstringlines.pop(0)
        docstringlines.pop(0)

def process_docstring_module_title(app, what, name, obj, options, docstringlines):
    """
    Removes the first line from the beginning of the module's docstring.  This
    corresponds to the title of the module's documentation page.
    """
    if what != "module":
        return

    #Remove any additional blank lines at the beginning
    title_removed = False
    while len(docstringlines) > 1 and not title_removed:
        if docstringlines[0].strip() != "":
            title_removed = True
        docstringlines.pop(0)

    #Remove any additional blank lines at the beginning
    while len(docstringlines) > 1:
        if docstringlines[0].strip() == "":
            docstringlines.pop(0)
        else:
            break

skip_picklability_check_modules = [
    #'sage.misc.nested_class_test', # for test only
    'sage.misc.latex',
    'sage.misc.explain_pickle',
    '__builtin__',
]

def check_nested_class_picklability(app, what, name, obj, skip, options):
    """
    Print a warning if pickling is broken for nested classes.
    """
    import types
    if hasattr(obj, '__dict__') and hasattr(obj, '__module__'):
        # Check picklability of nested classes.  Adapted from
        # sage.misc.nested_class.modify_for_nested_pickle.
        module = sys.modules[obj.__module__]
        for (nm, v) in obj.__dict__.iteritems():
            if (isinstance(v, (type, types.ClassType)) and
                v.__name__ == nm and
                v.__module__ == module.__name__ and
                getattr(module, nm, None) is not v and
                v.__module__ not in skip_picklability_check_modules):
                # OK, probably this is an *unpicklable* nested class.
                app.warn('Pickling of nested class %r is probably broken. '
                         'Please set __metaclass__ of the parent class to '
                         'sage.misc.nested_class.NestedClassMetaclass.' % (
                        v.__module__ + '.' + name + '.' + nm))

def skip_member(app, what, name, obj, skip, options):
    """
    To suppress Sphinx warnings / errors, we

    - Don't include [aliases of] builtins.

    - Don't include the docstring for any nested class which has been
      inserted into its module by
      :class:`sage.misc.NestedClassMetaclass` only for pickling.  The
      class will be properly documented inside its surrounding class.

    - Don't include
      sagenb.notebook.twist.userchild_download_worksheets.zip.

    - Optionally, check whether pickling is broken for nested classes.

    - Optionally, include objects whose name begins with an underscore
      ('_'), i.e., "private" or "hidden" attributes, methods, etc.

    Otherwise, we abide by Sphinx's decision.  Note: The object
    ``obj`` is excluded (included) if this handler returns True
    (False).
    """
    if 'SAGE_CHECK_NESTED' in os.environ:
        check_nested_class_picklability(app, what, name, obj, skip, options)

    if getattr(obj, '__module__', None) == '__builtin__':
        return True

    if (hasattr(obj, '__name__') and obj.__name__.find('.') != -1 and
        obj.__name__.split('.')[-1] != name):
        return True

    if name.find("userchild_download_worksheets.zip") != -1:
        return True

    if 'SAGE_DOC_UNDERSCORE' in os.environ:
        if name.split('.')[-1].startswith('_'):
            return False

    return skip

def process_dollars(app, what, name, obj, options, docstringlines):
    r"""
    Replace dollar signs with backticks.
    See sage.misc.sagedoc.process_dollars for more information
    """
    if len(docstringlines) > 0 and name.find("process_dollars") == -1:
        from sage.misc.sagedoc import process_dollars as sagedoc_dollars
        s = sagedoc_dollars("\n".join(docstringlines))
        lines = s.split("\n")
        for i in range(len(lines)):
            docstringlines[i] = lines[i]

def process_inherited(app, what, name, obj, options, docstringlines):
    """
    If we're including inherited members, omit their docstrings.
    """
    if not options.get('inherited-members'):
        return

    if what in ['class', 'data', 'exception', 'function', 'module']:
        return

    name = name.split('.')[-1]

    if what == 'method' and hasattr(obj, 'im_class'):
        if name in obj.im_class.__dict__.keys():
            return

    if what == 'attribute' and hasattr(obj, '__objclass__'):
        if name in obj.__objclass__.__dict__.keys():
            return

    for i in xrange(len(docstringlines)):
        docstringlines.pop()

dangling_debug = False

def debug_inf(app, message):
    if dangling_debug: app.info(message)

def call_intersphinx(app, env, node, contnode):
    """
    Call intersphinx and work around its misshandling of relative links
    """
    debug_inf(app, "???? Trying intersphinx for %s"%node['reftarget'])
    builder = app.builder
    res =  sphinx.ext.intersphinx.missing_reference(
        app, env, node, contnode)
    if res: #workaround intersphinx misshandling of relative links
        # useful for debugging
        # import pdb
        # pdb.set_trace()
        if res['refuri'].startswith(SAGE_DOC):
            here = os.path.dirname(os.path.join(builder.outdir,
                                                node['refdoc']))
            res['refuri'] = os.path.relpath(res['refuri'], here)
            debug_inf(app, "++++ Found at %s"%res['refuri'])
    else:
        debug_inf(app, "---- Intersphinx: %s not Found"%node['reftarget'])
    return res

def find_sage_dangling_links(app, env, node, contnode):
    """
    Try to find dangling link in local module imports or all.py.
    """
    debug_inf(app, "==================== find_sage_dangling_links ")

    reftype = node['reftype']
    reftarget  = node['reftarget']
    try:
        doc = node['refdoc']
    except KeyError:
        debug_inf(app, "-- no refdoc in node %s"%node)
        return None

    debug_inf(app, "Searching %s from %s"%(reftarget, doc))

    # Workaround: in Python's doc 'object', 'list', ... are documented as a
    # function rather than a class
    if reftarget in base_class_as_func and reftype == 'class':
        node['reftype'] = 'func'

    res = call_intersphinx(app, env, node, contnode)
    if res:
        debug_inf(app, "++ DONE %s"%(res['refuri']))
        return res

    if node.get('refdomain') != 'py': # not a python file
       return None

    try:
        module = node['py:module']
        cls    = node['py:class']
    except KeyError:
        debug_inf(app, "-- no module or class for :%s:%s"%(reftype, reftarget))
        return None

    basename = reftarget.split(".")[0]
    try:
        target_module = getattr(sys.modules['sage.all'], basename).__module__
    except AttributeError:
        debug_inf(app, "-- %s not found in sage.all"%(basename))
        return None
    if target_module is None:
        target_module = ""
        debug_inf(app, "?? found in None !!!")

    debug_inf(app, "++ found %s using sage.all in %s"%(basename, target_module))

    newtarget = target_module+'.'+reftarget
    node['reftarget'] = newtarget

    # adapted  from sphinx/domains/python.py
    builder = app.builder
    searchmode = node.hasattr('refspecific') and 1 or 0
    matches =  builder.env.domains['py'].find_obj(
        builder.env, module, cls, newtarget, reftype, searchmode)
    if not matches:
        debug_inf(app, "?? no matching doc for %s"%newtarget)
        return call_intersphinx(app, env, node, contnode)
    elif len(matches) > 1:
        env.warn(target_module,
                 'more than one target found for cross-reference '
                 '%r: %s' % (newtarget,
                             ', '.join(match[0] for match in matches)),
                 node.line)
    name, obj = matches[0]
    debug_inf(app, "++ match = %s %s"%(name, obj))

    from docutils import nodes
    newnode = nodes.reference('', '', internal=True)
    if name == target_module:
        newnode['refid'] = name
    else:
        newnode['refuri'] = builder.get_relative_uri(node['refdoc'], obj[0])
        newnode['refuri'] += '#' + name
        debug_inf(app, "++ DONE at URI %s"%(newnode['refuri']))
    newnode['reftitle'] = name
    newnode.append(contnode)
    return newnode

# lists of basic Python class which are documented as functions
base_class_as_func = [
    'bool', 'complex', 'dict', 'file', 'float',
    'frozenset', 'int', 'list', 'long', 'object',
    'set', 'slice', 'str', 'tuple', 'type', 'unicode', 'xrange']

# Nit picky option configuration: Put here broken links we want to ignore. For
# link to the Python documentation several links where broken because there
# where class listed as functions. Expand the list 'base_class_as_func'
# above instead of marking the link as broken.
nitpick_ignore = (
    ('py:class', 'twisted.web2.resource.Resource'),
    ('py:class', 'twisted.web2.resource.PostableResource'))

def nitpick_patch_config(app):
    """
    Patch the default config for nitpicky

    Calling path_config ensure that nitpicky is not considered as a Sphinx
    environment variable but rather as a Sage environment variable. As a
    consequence, changing it doesn't force the recompilation of the entire
    documentation.
    """
    app.config.values['nitpicky'] = (False, 'sage')
    app.config.values['nitpick_ignore'] = ([], 'sage')

from sage.misc.sageinspect import sage_getargspec
autodoc_builtin_argspec = sage_getargspec

def setup(app):
    app.connect('autodoc-process-docstring', process_docstring_cython)
    app.connect('autodoc-process-docstring', process_directives)
    app.connect('autodoc-process-docstring', process_docstring_module_title)
    app.connect('autodoc-process-docstring', process_dollars)
    app.connect('autodoc-process-docstring', process_inherited)
    app.connect('autodoc-skip-member', skip_member)

    # When building the standard docs, app.srcdir is set to SAGE_DOC +
    # 'LANGUAGE/DOCNAME', but when doing introspection, app.srcdir is
    # set to a temporary directory.  We don't want to use intersphinx,
    # etc., when doing introspection.
    if app.srcdir.startswith(SAGE_DOC):
        app.add_config_value('intersphinx_mapping', {}, True)
        app.add_config_value('intersphinx_cache_limit', 5, False)
        # We do *not* fully initialize intersphinx since we call it by hand
        # in find_sage_dangling_links.
        #   app.connect('missing-reference', missing_reference)
        app.connect('missing-reference', find_sage_dangling_links)
        import sphinx.ext.intersphinx
        app.connect('builder-inited', set_intersphinx_mappings)
        app.connect('builder-inited', sphinx.ext.intersphinx.load_mappings)
        app.connect('builder-inited', nitpick_patch_config)
        # Minimize GAP/libGAP RAM usage when we build the docs
        from sage.interfaces.gap import set_gap_memory_pool_size
        set_gap_memory_pool_size(0)  # will be rounded up to 1M

