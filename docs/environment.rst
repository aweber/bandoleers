Environment Variables
=====================

.. envvar:: CASSANDRA_URI

   Identifies a Cassandra cluster to connect to.  The general form is::

      cassandra://HOST:PORT?property=value&property=value

   The ``HOST`` portion is the DNS name or IP address of the Cassandra
   server.  It is used as the ``contact_points`` parameter in the
   :class:`cassandra.cluster.Cluster` initializer.  If it resolves to 
   multiple addresses, then the entire list is passed to the initializer.
   If the ``PORT`` is omitted, then it defaults to 9042.  The optional
   "query string" contains properties that are passed to the initializer
   as keyword parameters.

.. envvar:: CONSUL_HOST

   Identifies the IP address or DNS name of the Consul server.

.. envvar:: CONSUL_PORT

   Identifies the TCP port number that the Consul server is listening on.

.. envvar:: RABBITMQ

   The network location portion for the RabbitMQ HTTP API.  This is
   inserted directly into a HTTP URL.

.. envvar:: REDIS_URI

   Identifies the redis server, port, and database to connect to.  This
   value follows the IANA-registered `redis url`_ format.

.. envvar:: PGSQL

   Identifies the PostgreSQL server to connect to using the standard
   `postgresql:// scheme`_

.. envvar:: PGSQL_...

   Identifies the PostgreSQL connection to use for the specific database
   named by the suffix using the standard `postgresql:// scheme`_


.. _postgresql:// scheme: http://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-CONNSTRING
.. _redis url: https://www.iana.org/assignments/uri-schemes/prov/redis
