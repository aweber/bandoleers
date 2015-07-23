"""

wait-for -- wait for a URL to become available

Usage:
    wait-for <URL> [--timeout=seconds]
    wait-for (-h | --help | --version)

"""
import logging
import time
import sys
try:
    from urllib import parse
except:
    import urlparse as parse

import docopt
import requests.exceptions


logging.basicConfig(
    level=logging.DEBUG,
    format='%(relativeCreated)-10d %(levelname)-8s %(message)s')


def connect_to(url, timeout):
    scheme, netloc, path, query, fragment = parse.urlsplit(url)
    if scheme in ('http', 'https'):
        requests.get(url, timeout=timeout)
    else:
        raise RuntimeError("I don't know what to do with {0}".format(scheme))


def run():
    logger = logging.getLogger(__name__)
    opts = docopt.docopt(__doc__)
    timeout = opts.get('--timeout', None)

    t0 = time.time()
    wait_forever = timeout is None
    timeout = 0.25 if wait_forever else float(timeout)
    logger.debug('waiting for %s', 'forever' if wait_forever else timeout)
    while wait_forever or (time.time() - t0) < timeout:
        try:
            try:
                connect_to(opts['<URL>'], timeout=timeout)
                logger.debug('connection to %s succeeded after %f seconds',
                             opts['<URL>'], time.time() - t0)
                sys.exit(0)

            except requests.exceptions.Timeout:
                break

            except requests.exceptions.ConnectionError:
                logger.debug('connection error occurred, sleeping')
                time.sleep(0.25)

        except RuntimeError:
            logger.exception('internal failure')
            sys.exit(70)

        except KeyboardInterrupt:
            logger.info('killed')
            sys.exit(-1)

    logger.error('wait timed out after %f seconds', time.time() - t0)
    sys.exit(-1)
