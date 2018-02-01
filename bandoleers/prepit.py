"""
Platform service configuration utility.

The prepit utility looks for a set of configuratione files in a local
directory called platform, and attempts to apply those configuration
settings to platform services that are discovered via environment
variables. See the README file in the git repo for this utility
for more details.

"""
import logging
import os.path
import re
import sys
try:
    from urllib.parse import urlsplit, urlunsplit
except ImportError:
    from urlparse import urlsplit, urlunsplit

from redis import StrictRedis
import consulate
import json
import queries
import requests

from bandoleers import args


LOGGER = logging.getLogger(__name__)


def prep_redis(file_):
    try:
        LOGGER.info('Processing %s', file_)
        parts = urlsplit(os.environ.get('REDIS_URI', 'redis://localhost'))
        redis = StrictRedis(host=parts.hostname,
                            port=parts.port or 6379,
                            db=parts.path[1:] or 0)

        with open(file_) as fh:
            config = json.load(fh)
            for command, entries in config.items():
                for name, values in entries.items():
                    redis.execute_command(command, name, *values)
    except Exception:
        LOGGER.exception('Failed to execute redis commands.')
        sys.exit(-1)


def prep_consul(file):
    try:
        LOGGER.info('Processing %s', file)
        consul = consulate.Consul(os.environ.get('CONSUL_HOST', 'localhost'),
                                  int(os.environ.get('CONSUL_PORT', '8500')))
        with open(file) as fh:
            config = json.load(fh)
            LOGGER.debug('%r', config)
            for k, v in config.items():
                consul.kv[k] = v
    except Exception:
        LOGGER.exception('Failed to load consul data.')
        sys.exit(-1)


def prep_postgres(file):
    try:
        LOGGER.info('Processing %s', file)
        db = os.path.splitext(os.path.basename(file))[0]
        uri = os.environ.get('PGSQL_{0}'.format(db.upper()))
        if uri is not None:
            chop = len(db) + 1
            base = uri[:-chop]
        else:
            base = os.environ.get('PGSQL',
                                  'postgresql://postgres@localhost:5432')
            uri = os.path.join(base, db)
            with queries.Session(os.path.join(base, 'postgres')) as session:
                LOGGER.debug('Creating database')
                session.query('DROP DATABASE IF EXISTS {0};'.format(db))
                session.query('CREATE DATABASE {0};'.format(db))

        with queries.Session(uri) as session:
            with open(file) as fh:
                session.query(fh.read())
    except Exception:
        LOGGER.exception('Failed to execute pgsql queries.')
        sys.exit(-1)


def prep_rabbit(file):
    try:
        LOGGER.info('Processing %s', file)
        host = os.environ.get('RABBITMQ', 'localhost')
        with open(file) as fh:
            config = json.load(fh)
            for action in config:
                uri = 'http://{0}/{1}'.format(host, action['path'])
                LOGGER.debug('%s', action)
                r = requests.request(
                    url=uri, method=action['method'],
                    auth=('guest', 'guest'), json=action['body'])
                r.raise_for_status()
    except Exception:
        LOGGER.exception('Failed to configure rabbit.')
        sys.exit(-1)


def prep_http(file):
    LOGGER.info('Processing %s', file)
    var_pattern = re.compile(r'\$(?P<name>[_a-z0-9]+)',
                             re.IGNORECASE)
    with open(file) as fh:
        input_requests = json.load(fh)
        for request in input_requests:
            try:
                url = request['url']
                matches = var_pattern.findall(url)
                for var_name in matches:
                    if var_name in os.environ:
                        url = url.replace('${}'.format(var_name),
                                          os.environ[var_name])
                parts = urlsplit(url)
                user, password = parts.username, parts.password
                hostname, port = parts.hostname, parts.port
                if port:
                    netloc = '{}:{}'.format(hostname, port)
                else:
                    netloc = hostname

                request['url'] = urlunsplit((
                    parts.scheme, netloc, parts.path, parts.query,
                    parts.fragment))
                request.setdefault('method', 'GET')
                request.setdefault('auth', (user, password))
                LOGGER.debug('making HTTP request %r', request)
                r = requests.request(**request)
                r.raise_for_status()
            except Exception:
                LOGGER.exception('HTTP request %r failed.', request)
                sys.exit(-1)


def run():
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)1.1s - %(name)s: %(message)s')
    parser = args.ArgumentParser()
    parser.add_argument('-d', '--dir', metavar='DIRECTORY',
                        default='platform', dest='directory',
                        help='read files from DIRECTORY')
    opts = parser.parse_args()

    resources = {
        'consul': prep_consul,
        'http': prep_http,
        'postgres': prep_postgres,
        'rabbitmq': prep_rabbit,
        'redis': prep_redis,
    }

    top_level = os.listdir(opts.directory)
    for resource in resources:
        if resource in top_level:
            path = '/'.join([opts.directory, resource])
            files = os.listdir(path)
            for data_file in files:
                if data_file.startswith('.') or data_file.endswith('~'):
                    continue
                resources[resource]('/'.join([path, data_file]))
    LOGGER.info('Finished processing successfully.')
    sys.exit(0)


if __name__ == '__main__':
    run()
