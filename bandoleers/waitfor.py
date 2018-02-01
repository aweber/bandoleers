"""
Wait for a URL to become available.

"""
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

import psycopg2
import requests.exceptions

from bandoleers import args


LOGGER = logging.getLogger(__name__)


def connect_to(url, timeout):
    scheme, netloc, path, query, fragment = parse.urlsplit(url)
    if scheme in ('http', 'https'):
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

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

    elif scheme == 'tcp':
        host, sep, port = netloc.partition(':')
        if not sep:
            raise RuntimeError('tcp:// requires a port')
        try:
            port = int(port)
        except:
            raise RuntimeError('failed to extract port from ' + netloc)

        ip_addr = socket.gethostbyname(host)
        LOGGER.debug('opening TCP connection to %r:%r', ip_addr, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM,
                             socket.IPPROTO_TCP)
        sock.settimeout(timeout)
        sock.connect((ip_addr, port))
        sock.close()

    else:
        raise RuntimeError("I don't know what to do with {0}".format(scheme))


def run():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format='%(relativeCreated)-10.3f %(levelname)-8s %(message)s')

    parser = args.ArgumentParser()
    parser.add_argument('-s', '--sleep', type=float, metavar='SECONDS',
                        default=0.25, help='time to sleep after a failure')
    parser.add_argument('-t', '--timeout', type=float, metavar='SECONDS',
                        default=None,
                        help=('total number of seconds to run for. '
                              'Default is to run forever'))
    parser.add_argument('URL')
    opts = parser.parse_args()

    t0 = time.time()
    wait_forever = opts.timeout is None
    timeout = max(opts.sleep, opts.timeout or opts.sleep)
    logger.debug('waiting on %s for %s', opts.URL,
                 'forever' if wait_forever else opts.timeout)

    while True:
        try:
            connect_to(opts.URL, timeout=timeout)
            logger.debug('connection to %s succeeded after %f seconds',
                         opts.URL, time.time() - t0)
            sys.exit(0)

        except RuntimeError:
            logger.exception('internal failure')
            sys.exit(70)

        except KeyboardInterrupt:
            logger.info('killed')
            sys.exit(-1)

        except Exception as error:
            if not wait_forever and (time.time() - t0) >= opts.timeout:
                break

            logger.debug('%r, sleeping for %f seconds', error, opts.sleep)
            time.sleep(opts.sleep)

    logger.error('wait timed out after %f seconds', time.time() - t0)
    sys.exit(-1)


if __name__ == '__main__':
    run()
