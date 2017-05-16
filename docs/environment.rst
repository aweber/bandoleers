Environment Variables
=====================

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
