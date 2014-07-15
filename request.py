#!/usr/bin/env python

import requests
from argparse import ArgumentParser
from subprocess import Popen, PIPE
import json
from pygments import highlight
from pygments.lexers import guess_lexer, JSONLexer
from pygments.formatters import TerminalFormatter


def get_terminal_size():
    import os
    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct
            return struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                                   '1234'))
        except:
            return
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])


def parse_args():
    parser = ArgumentParser('requests')
    parser.add_argument('url')
    parser.add_argument('-X', '--request', dest="method",
                        metavar='GET', default='GET')
    parser.add_argument('-d', '--data',
                        help="Data to send in the body of the request. "
                        "If you're giving JSON, an appropriate header "
                        "will be set.")
    parser.add_argument('-H', '--header', nargs='*')
    parser.add_argument('-i', '--include',
                        help='Include HTTP headers in the response',
                        action='store_true', default=False)
    return parser.parse_args()


def prepare_query(args):
    if not args.url.lower().startswith('http'):
        args.url = 'http://' + args.url
    headers = {}
    try:
        json.loads(args.data)
        headers['Content-Type'] = 'application/json'
    except Exception:
        pass
    headers.update(header.split(': ', 1) for header in args.header)
    return args.method, args.url, headers, args.data


def do_query(method, url, headers, data):
    return requests.request(method, url, data=data, headers=headers)


def pretty_print(text):
    try:
        return highlight(json.dumps(json.loads(text), indent=4),
                         JSONLexer(), TerminalFormatter())
    except Exception:
        pass
    try:
        return highlight(text, guess_lexer(text), TerminalFormatter())
    except Exception:
        pass
    return text


def print_response(args, response):
    to_print = ""
    if args.include:
        to_print += json.dumps(dict(response.headers), indent=4) + "\n\n"
    to_print += pretty_print(response.text)
    if len(to_print.split('\n')) >= get_terminal_size()[1]:
        Popen(["less", '-R'], stdin=PIPE).communicate(to_print.encode('UTF8'))
    else:
        print to_print

args = parse_args()
print_response(args, do_query(*prepare_query(args)))
