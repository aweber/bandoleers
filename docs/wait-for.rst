wait-for
========
.. program:: wait-for

The :program:`wait-for` utility polls a URL periodically until it gets a
successful response.

.. code::

   wait-for ([-q|--quiet] | [-v|--verbose]) [-s|--sleep SECONDS]
            [-t|--timeout SECONDS] URL
   wait-for (-h | --help | --version)

.. option:: URL

   Specifies the URL to poll.  The following schemes are supported:

   +---------------------+----------------------------------------------+
   | ``http``, ``https`` | Fail for non-200 family status codes         |
   +---------------------+----------------------------------------------+
   | ``cassandra``       | Fail unless connecting the `datastax`_       |
   |                     | Cassandra client to the URL succeeds.        |
   +---------------------+----------------------------------------------+
   | ``postgresql``      | Fail unless connecting `psycopg2`_ to the    |
   |                     | URL succeeds.                                |
   +---------------------+----------------------------------------------+
   | ``tcp``             | Fail unless connecting a TCP socket succeeds.|
   +---------------------+----------------------------------------------+

.. option:: -s <seconds>, --sleep <seconds>

   Sleep for the specified number of seconds between hitting the URL.

.. option:: -t <seconds>, --timeout <seconds>

   Timeout and exit unsuccessfully if a successful response is not received
   within *timeout* seconds.

.. option:: -v, --verbose

   Write diagnostics to standard output.  Without this flag, the utility
   is quite silent.

.. option:: -q, --quiet

   Only show output when an error occurs.

.. option:: -h, --help

   Display a usage synopsis and exit with a failure status.

.. option:: --version

   Display the package version and exit with a failure status.


.. _datastax: https://github.com/datastax/python-driver
.. _psycopg2: http://initd.org/psycopg/docs/
