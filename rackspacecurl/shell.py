"""
Command-line wrapper to curl for Rackspace Cloud API
"""

import argparse
import sys
import logging

import rackspacecurl
from rackspacecurl import client
from rackspacecurl import utils
from rackspacecurl.v1_0 import shell as shell_v1_0

logger = logging.getLogger(__name__)

class RackspaceCurlArgumentParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(RackspaceCurlArgumentParser, self).__init__(*args, **kwargs)

    def error(self, message):
        """error(message: string)

        Prints a usage message incorporating the message to stderr and exits
        """
        self.print_usage(sys.stderr)
        choose_from = ' (choose from'
        progparts = self.prog.partition(' ')
        self.exit(2, "error: %(errmsg)s\nTry '%(mainp)s help %(subp)s'"
                " for more information.\n" %
                {'errmsg': message.split(choose_from)[0],
                    'mainp': progparts[0],
                    'subp': progparts[2]})

class RackspaceCurlShell(object):

    def get_base_parser(self):
        parser = RackspaceCurlArgumentParser(
                prog='raxcurl',
                description=__doc__.strip(),
                epilog='See "raxcurl help COMMAND" '\
                        'for help on specific command.',
                add_help=False,
                formatter_class=RackspaceCurlHelpFormatter,
                )

        # Global Args
        parser.add_argument('-h', '--help',
                action='store_true',
                help=argparse.SUPPRESS,
                )

        parser.add_argument('--debug',
                default=False,
                action='store_true',
                help="Print debugging output")

        parser.add_argument('--xml',
                default=False,
                action='store_true',
                help="Output xml instead of json (application/xml)")
        return parser

    def get_subcommand_parser(self):
        parser = self.get_base_parser()

        self.subcommands = {}
        subparsers = parser.add_subparsers(metavar='<subcommand>')

        actions_module = shell_v1_0

        self._find_actions(subparsers, actions_module)
        self._find_actions(subparsers, self)

        return parser

    def _find_actions(self, subparsers, actions_module):
        for attr in (a for a in dir(actions_module) if a.startswith('do_')):
            # handle hypen-separated instead of underscores
            command = attr[3:].replace('_', '-')
            callback = getattr(actions_module, attr)
            desc = callback.__doc__ or ''
            action_help = desc.strip().split('\n')[0]
            arguments = getattr(callback, 'arguments', [])

            subparser = subparsers.add_parser(command,
                    help=action_help,
                    description=desc,
                    add_help=False,
                    formatter_class=RackspaceCurlHelpFormatter
                    )
            subparser.add_argument('-h', '--help',
                    action='help',
                    help=argparse.SUPPRESS,
                    )
            self.subcommands[command] = subparser
            for (args, kwargs) in arguments:
                subparser.add_argument(*args, **kwargs)
            subparser.set_defaults(func=callback)

    def setup_debugging(self, debug):
        if not debug:
            return

        streamhandler = logging.StreamHandler()
        streamformat = "%(levelname)s (%(module)s:%(lineno)d) %(message)s"
        streamhandler.setFormatter(logging.Formatter(streamformat))
        logger.setLevel(logging.DEBUG)

    def main(self, argv):
        parser = self.get_base_parser()
        (options, args) = parser.parse_known_args(argv)
        self.setup_debugging(options.debug)

        subcommand_parser = self.get_subcommand_parser()
        self.parser = subcommand_parser

        if options.help and len(args) == 0:
            subcommand_parser.print_help()
            return 0

        args = subcommand_parser.parse_args(argv)

        # Short-circuit and deal with help right away.
        if args.func == self.do_help:
            self.do_help(args)
            return 0

        self.cs = client.Client("1.0")

        args.func(self.cs, args)

        return

    @utils.arg('command', metavar='<subcommand>', nargs='?',
            help='Display help for <subcommand>')
    def do_help(self, args):
        """
        Display help about this program or one of its subcommands.
        """
        if args.command:
            if args.command in self.subcommands:
                self.subcommands[args.command].print_help()
            else:
                raise exc.CommandError("'%s' is not a valid subcommand" %
                        args.command)
        else:
            self.parser.print_help()

class RackspaceCurlHelpFormatter(argparse.HelpFormatter):
    def start_section(self, heading):
        # Title-case the headings
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(RackspaceCurlHelpFormatter, self).start_section(heading)

def main():
    try:
        RackspaceCurlShell().main(sys.argv[1:])

    except Exception, e:
        logger.debug(e, exc_info=1)
        print >> sys.stderr, "ERROR: %s" % unicode(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
