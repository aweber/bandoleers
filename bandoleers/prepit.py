""" Prepit platform service configuration utility.

The prepit utility looks for a set of configuratione files in a local
directory called platform, and attempts to apply those configuration
settings to platform services that are discovered via environment
variables. See the README file in the git repo for this utility
for more details.

"""
import logging
import os
import socket
import sys
try:
    from urllib.parse import parse_qsl, urlsplit
except ImportError:
    from urlparse import parse_qsl, urlsplit

from cassandra.cluster import Cluster
from redis import StrictRedis
import consulate
import json
import queries
import requests


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


def prep_cassandra(file):
    try:
        LOGGER.info('Processing %s', file)
        uri = os.environ.get('CASSANDRA_URI', 'cassandra://localhost')
        parts = urlsplit(uri)
        _, _, ips = socket.gethostbyname_ex(parts.hostname)
        config = dict(parse_qsl(parts.query))
        config['contact_points'] = ips
        config['port'] = parts.port or 9042
        for key in ('protocol_version', 'executor_threads',
                    'max_schema_agreement_wait', 'idle_heartbeat_interval',
                    'schema_refresh_window', 'topology_event_refresh_window'):
            if key in config:
                config[key] = int(config[key])
        cluster = Cluster(**config)
        session = cluster.connect()
        with open(file) as fh:
            for schema_line in fh.read().split(';'):
                if schema_line.strip():
                    LOGGER.debug('%s', schema_line)
                    session.execute(schema_line + ';')
        session.shutdown()
    except Exception:
        LOGGER.exception('Failed to execute cassandra queries.')
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
        db = file.split('/')[-1][:-4]
        uri = os.environ.get('PGSQL_{}'.format(db.upper()))
        if uri is not None:
            chop = len(db) + 1
            base = uri[:-chop]
        else:
            base = os.environ.get('PGSQL',
                                  'postgresql://postgres@localhost:5432')
            uri = base + '/' + db
        with queries.Session(base + '/postgres') as session:
            LOGGER.debug('Creating database')
            session.query('DROP DATABASE IF EXISTS {};'.format(db))
            session.query('CREATE DATABASE {};'.format(db))
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
                uri = 'http://{}/{}'.format(host, action['path'])
                LOGGER.debug('%s', action)
                r = requests.request(
                    url=uri, method=action['method'],
                    auth=('guest', 'guest'), json=action['body'])
                r.raise_for_status()
    except Exception:
        LOGGER.exception('Failed to configure rabbit.')
        sys.exit(-1)


def run():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)1.1s - %(name)s: %(message)s')

    resources = {
        'cassandra': prep_cassandra,
        'consul': prep_consul,
        'postgres': prep_postgres,
        'rabbitmq': prep_rabbit,
        'redis': prep_redis,
    }

    dir = os.listdir('./platform')
    for resource in resources:
        if resource in dir:
            path = '/'.join(['./platform', resource])
            files = os.listdir(path)
            for file in files:
                resources[resource]('/'.join([path, file]))
    LOGGER.info('Finished processing successfully.')
    sys.exit(0)


if __name__ == '__main__':
    run()
