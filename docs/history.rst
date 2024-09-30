.. :changelog:

Release History
===============

`Next Release`_
---------------

`4.0.1`_ (2024-09-30)
---------------------
- Loosen psycopg3 pin to allow for all major versions of psycopg3

`4.0.0`_ (2024-09-27)
---------------------
- Replace ``pyscopg2`` with ``psycopg3``

`3.3.2`_ (2023-11-29)
---------------------
- Loosen redis pin to allow redis 5

`3.3.1`_ (2022-08-23)
---------------------
- Loosen redis pin to allow redis 4
- Switch to GitHub Actions for CI

`3.3.0`_ (2021-09-02)
---------------------
- Replace consulate usage with requests
- Add classifiers for 3.8 & 3.9.

`3.2.0`_ (2019-04-05)
---------------------
- Use ``psycopg2`` instead of ``queries``

`3.1.0`_ (2019-03-27)
---------------------
- Expand supported redis package versions

`3.0.0`_ (2018-02-01)
---------------------
- Upgrade to queries 2.0.x.
- Drop support for Python 2.6.

`2.1.0`_ (2017-10-28)
---------------------
- Add raw HTTP support to ``prep-it``
- Ignore data files that look like temporary files.  This specifcally
  ignores files that start with a period and files that end with a tilde.

`2.0.0`_ (2017-05-22)
---------------------
- Remove Cassandra support

`1.1.1`_ (2016-08-17)
---------------------
- Support Python 2.6

`1.1.0`_ (2016-04-13)
---------------------
- Make the platform directory name an option for ``prep-it``
- Add ``--sleep`` parameter to ``wait-for``
- Normalize parameter processing between commands
- Do not create a postgres database if the database-specific
  environment variable exists.
- Add support for ``tcp://`` in ``wait-for``

`1.0.0`_ (2016-01-27)
---------------------
- Infect the world!

`0.3.5`_ (2016-01-26)
---------------------
- Query parameters are now passed from cassandra:// URLs into the cluster
  instance.

`0.3.4`_ (2016-01-14)
---------------------
- Add postgres support in ``wait-for``

`0.3.3`_ (2015-10-08)
---------------------
- The default Redis DB must be an integer

`0.3.0`_ (2015-09-15)
---------------------
- Read and execute the entire SQL file when bootstrapping Postgresql

`0.2.1`_ (2015-09-14)
---------------------
- Remove ``codecs`` from ``setup.py`` for Python 3 compatibility.

`0.2.0`_ (2015-08-05)
---------------------
- Added the ``wait-for`` utility

`0.1.0`_ (2015-06-23)
---------------------
- Initial release of the PrepIt package
- Import @briank's work on prepit.

.. _Next Release: https://github.com/aweber/bandoleers/compare/3.3.2...HEAD
.. _3.3.1: https://github.com/aweber/bandoleers/compare/3.3.1...3.3.2
.. _3.3.1: https://github.com/aweber/bandoleers/compare/3.3.0...3.3.1
.. _3.3.0: https://github.com/aweber/bandoleers/compare/3.2.0...3.3.0
.. _3.2.0: https://github.com/aweber/bandoleers/compare/3.1.0...3.2.0
.. _3.1.0: https://github.com/aweber/bandoleers/compare/3.0.0...3.1.0
.. _3.0.0: https://github.com/aweber/bandoleers/compare/2.1.0...3.0.0
.. _2.1.0: https://github.com/aweber/bandoleers/compare/2.0.0...2.1.0
.. _2.0.0: https://github.com/aweber/bandoleers/compare/1.1....2.0.0
.. _1.1.1: https://github.com/aweber/bandoleers/compare/1.1.0...1.1.1
.. _1.1.0: https://github.com/aweber/bandoleers/compare/1.0.0...1.1.0
.. _1.0.0: https://github.com/aweber/bandoleers/compare/0.3.5...1.0.0
.. _0.3.5: https://github.com/aweber/bandoleers/compare/0.3.4...0.3.5
.. _0.3.4: https://github.com/aweber/bandoleers/compare/0.3.3...0.3.4
.. _0.3.3: https://github.com/aweber/bandoleers/compare/0.3.0...0.3.3
.. _0.3.0: https://github.com/aweber/bandoleers/compare/0.2.1...0.3.0
.. _0.2.1: https://github.com/aweber/bandoleers/compare/0.2.0...0.2.1
.. _0.2.0: https://github.com/aweber/bandoleers/compare/0.1.0...0.2.0
.. _0.1.0: https://github.com/aweber/bandoleers/compare/0.0.0...0.1.0
