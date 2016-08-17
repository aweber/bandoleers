import argparse
import logging
import sys

import bandoleers


class ArgumentParser(argparse.ArgumentParser):
    """
    Implements some common command-line behaviors.

    This is a slightly extended version of the standard
    :class:`argparse.ArgumentParser` class that does three
    things for you:

    * exits with a non-zero status when help is shown
    * implements --quiet and --verbose mutually exclusive
      options that call :meth:`logging.Logger.setLevel` on
      the root logger
    * adds a --version flag

    """

    def __init__(self, *args, **kwargs):
        super(ArgumentParser, self).__init__(*args, **kwargs)
        output_control = self.add_mutually_exclusive_group()
        output_control.add_argument('-q', '--quiet',
                                    action='store_true', default=False,
                                    help='disable non-failure output')
        output_control.add_argument('-v', '--verbose',
                                    action='store_true', default=False,
                                    help='show diagnostic output')
        self.add_argument(
            '--version', action='version',
            version='%(prog)s {0}'.format(bandoleers.__version__))

    def parse_args(self, *args, **kwargs):
        result = super(ArgumentParser, self).parse_args(*args, **kwargs)
        if result.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        if result.quiet:
            logging.getLogger().setLevel(logging.ERROR)
        return result

    def print_usage(self, file=None):
        stream = file or sys.stdout
        stream.write(self.format_usage())
        sys.exit(64)

    def print_help(self, file=None):
        stream = file or sys.stdout
        stream.write(self.format_help())
        sys.exit(64)
