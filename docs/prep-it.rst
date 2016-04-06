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

cassandra
---------
Text files containing queries that are executed using a
:class:`cassandra.cluster.Cluster` instance.  Queries are separated by
semi-colons and executed in the order that they appear in the file.  The
Cassandra server is configured by setting the :envvar:`CASSANDRA_URI`
environment variable.

consul
------
JSON files containing top-level object definitions (e.g., dictionaries)
that are loaded into a Consul key-value store using a :class:`consulate.Consul`
instance.  The Consul endpoint is configured by setting the
:envvar:`CONSUL_HOST` and :envvar:`CONSUL_PORT` environment variables.

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
