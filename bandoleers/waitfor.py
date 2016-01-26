"""

wait-for -- wait for a URL to become available

Usage:
    wait-for <URL> [-t|--timeout=seconds] [-v|--verbose]
    wait-for (-h | --help | --version)

"""
import asyncore
import logging
import socket
import sys
import time
import warnings
try:
    from urllib import parse
except ImportError:
    import urlparse as parse

warnings.simplefilter('ignore', UserWarning)

from cassandra import cluster
import docopt
import psycopg2
import requests.exceptions


logging.basicConfig(
    level=logging.INFO,
    format='%(relativeCreated)-10d %(levelname)-8s %(message)s')
LOGGER = logging.getLogger(__name__)


def connect_to(url, timeout):
    scheme, netloc, path, query, fragment = parse.urlsplit(url)
    if scheme in ('http', 'https'):
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return True

    elif scheme == 'cassandra':
        host, _, port = netloc.partition(':')
        _, _, ip_addrs = socket.gethostbyname_ex(host)
        options = dict(parse.parse_qsl(query))
        options['contact_points'] = ip_addrs
        options['port'] = int(port) or 9042
        options['control_connection_timeout'] = timeout
        for key in ('protocol_version', 'executor_threads',
                    'max_schema_agreement_wait', 'idle_heartbeat_interval',
                    'schema_refresh_window', 'topology_event_refresh_window'):
            if key in options:
                options[key] = int(options[key])

        conn = cluster.Cluster(**options)
        conn.connect()
        asyncore.close_all()
        asyncore.loop()

        return True

    elif scheme == 'postgresql':
        kwargs = {
            'user': 'postgres',
            'password': None,
            'host': 'localhost',
            'port': 5432,
            'database': 'postgres',
        }
        user_n_pass, sep, host_n_port = netloc.partition('@')
        if sep:
            user, sep, password = user_n_pass.partition(':')
            kwargs['user'] = user
            if sep:
                kwargs['password'] = password
        else:
            host_n_port = user_n_pass

        host, sep, port = host_n_port.partition(':')
        kwargs['host'] = host
        if sep:
            kwargs['port'] = int(port)

        if path:
            kwargs['database'] = path[1:]

        LOGGER.debug('connecting to postgres with %r', kwargs)
        conn = psycopg2.connect(**kwargs)
        conn.close()
        return True

    else:
        raise RuntimeError("I don't know what to do with {0}".format(scheme))


def run():
    logger = logging.getLogger(__name__)
    opts = docopt.docopt(__doc__)
    timeout = opts.get('--timeout', None)
    sleep_time = 0.25

    if opts.get('--verbose', False) or opts.get('-v', False):
        logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger('cassandra').setLevel(logging.CRITICAL)

    t0 = time.time()
    wait_forever = timeout is None
    timeout = 0.25 if wait_forever else float(timeout)
    logger.debug('waiting on %s for %s', opts['<URL>'],
                 'forever' if wait_forever else '{}s'.format(timeout))
    while wait_forever or (time.time() - t0) < timeout:
        try:
            if connect_to(opts['<URL>'], timeout=timeout):
                logger.debug('connection to %s succeeded after %f seconds',
                             opts['<URL>'], time.time() - t0)
                sys.exit(0)

        except RuntimeError:
            logger.exception('internal failure')
            sys.exit(70)

        except KeyboardInterrupt:
            logger.info('killed')
            sys.exit(-1)

        except Exception as error:
            logger.debug('%r, sleeping for %f seconds', error, sleep_time)
            time.sleep(sleep_time)

    logger.error('wait timed out after %f seconds', time.time() - t0)
    sys.exit(-1)
