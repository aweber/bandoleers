Bandoleers
==========

This package contains useful command line tools that make deployment and
local data bootstrapping less painful.

:prep-it:
    This simple utility iterates over data files in a sub-tree and loads
    them into various backends such as Cassandra, RabbitMQ, and PostgreSQL.

:wait-for:
    This simple utility pings a URL periodically until it responds
    successfully.  It supports HTTP, Cassandra, and Postgres URLs out of
    the box.


Quickstart Development Guide
----------------------------

.. code:: bash

    $ python3.4 -mvenv env
    $ . ./env/bin/activate
    (env) $ pip install -qr requires/development.txt
