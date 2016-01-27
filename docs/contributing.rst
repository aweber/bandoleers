How to Contribute
=================
Do you want to contribute fixes or improvements?

   **AWesome!** *Thank you very much, and let's get started.*

Set up a development environment
--------------------------------
The first thing that you need is a development environment so that you can
run the test suite, update the documentation, and everything else that is
involved in contributing.  The easiest way to do that is to create a virtual
environment for your endevours::

   $ python3.4 -mvenv env

Don't worry about writing code against previous versions of Python unless
you you don't have a choice.  If you don't have a choice, then install
`virtualenv`_ to create the environment instead.  The next step is to
install the development tools that this project uses.  These are listed in
*requires/development.txt*::

   $ env/bin/pip install -qr requires/development.txt

At this point, you will have everything that you need to develop at your
disposal.  *setup.py* is the swiss-army knife in your development tool
chest.  It provides the following commands:

**./setup.py build_sphinx**
   Generate the documentation using `sphinx`_.

**./setup.py flake8**
   Run `flake8`_ over the code and report style violations.

If any of the preceding commands give you problems, then you will have to
fix them **before** your pull request will be accepted.

Submitting a Pull Request
-------------------------
Once you have made your modifications and added any necessary documentation,
it is time to contribute back for posterity.  You've probably already cloned
this repository and created a new branch.  If you haven't, then checkout what
you have as a branch and roll back *master* to where you found it.  Then push
your repository up to github and issue a pull request.  Describe your changes
in the request and someone will review it, and eventually merge it and release
a new version.

.. _flake8: http://flake8.readthedocs.org/
.. _sphinx: http://sphinx-doc.org/
.. _virtualenv: http://virtualenv.pypa.io/
