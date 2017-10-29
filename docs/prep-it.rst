prep-it
=======
.. program:: prep-it

The :program:`prep-it` utility scans the *platform* sub-directory and
loads data files into various backends.  The following sections describe
each directory name that is supported and its expected content.

.. code::

   prep-it ([-q|--quiet] | [-v|--verbose]) [-d|--dir DIRECTORY]
   prep-it (-h | --help | --version)

.. option:: DIRECTORY

   Specifies the directory to process.  If unspecified, the "platform"
   directory is processed.

.. option:: -v, --verbose

   Write diagnostics to standard output.  Without this flag, informational
   messages will be displayed.

.. option:: -q, --quiet

   Only show output when an error occurs.

.. option:: -h, --help

   Display a usage synopsis and exit with a failure status.

.. option:: --version

   Display the package version and exit with a failure status.

consul
------
JSON files containing top-level object definitions (e.g., dictionaries)
that are loaded into a Consul key-value store using a :class:`consulate.Consul`
instance.  The Consul endpoint is configured by setting the
:envvar:`CONSUL_HOST` and :envvar:`CONSUL_PORT` environment variables.

http
----
JSON files containing an array of objects, one per request.  Each object
is simply a list of parameters passed into :func:`requests.request`.  The
following properties are usually what you want:

:url:
   The targetted resource.  This may be modified as described below.

:method:
   The HTTP method to request.

:params:
   Optional dictionary of query parameters.

:headers:
   Optional dictionary of headers to send.

:json:
   Optional body that will be JSON encoded before being sent.

The ``url`` value may contain environment variables in the host and/or
port number values.  For example ``http://$CONSUL_HOST:$CONSUL_PORT/...``
is rewritten to ``http://127.0.0.1:37832`` if the :envvar:`CONSUL_HOST`
environment variable is set to ``127.0.0.1`` and the :envvar:`CONSUL_PORT`
environment variable is set to ``37832``.

The user name and password parameters are removed from the URL and placed
into the ``auth`` keyword parameter if they are present in the URL.

rabbitmq
--------
JSON files that contain RabbitMQ HTTP API commands to execute.  Each
command is represented by an object with the following properties:

:path:
    The resource to send the request to.

:method:
    The HTTP method to invoke (e.g., ``POST``, ``DELETE``)

:body:
    The body to send with the request.

The RabbitMQ server is identified by setting the :envvar:`RABBITMQ`
environment variable to the host and port of the HTTP API endpoint.

redis
-----
JSON files each containing a top-level object definition where each
property names a redis command.  The property value is another object
definition where the name is the redis key and the value is a list of
values to pass to the command.

For example, the following JSON file would result in calling the
``SADD`` redis command to add ``"abuse"``, ``"admin"``, ``"postmaster"``,
and ``"root"`` to the ``admin_type_address`` redis set.

.. code-block:: javascript

   {
      "SADD": {
         "admin_type_address": [
            "abuse",
            "admin",
            "postmaster",
            "root"
         ]
      }
   }

The redis server is configured by setting the :envvar:`REDIS_URI`
environment variable to a `redis url`_.

.. _redis url: https://www.iana.org/assignments/uri-schemes/prov/redis

postgres
--------
SQL files that are executed using `queries`_.  The database server is
configured by setting the :envvar:`PGSQL` environment variable.  The
database name is based on the file name minus the assumed ``.sql``
suffix.  The database will be dropped if it exists and then created
anew before running the SQL commands from the file.

The database connection for a specific database can also be specified
by setting the :envvar:`PGSQL_$DBNAME` environment variable where
``$DBNAME`` is the name of the database in upper-case.  If a database
specific environment variable exists, **then the database will not be
created automatically.**

.. _queries: https://github.com/gmr/queries
