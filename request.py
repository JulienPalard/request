#!/usr/bin/env python

import requests
from argparse import ArgumentParser
from subprocess import Popen, PIPE
import json
from pygments import highlight
from pygments.lexers import get_lexer_by_name, \
    find_lexer_class, guess_lexer, TextLexer
from pygments.formatters import get_all_formatters, get_formatter_by_name, \
    get_formatter_for_filename, find_formatter_class, \
    TerminalFormatter  # pylint:disable-msg=E0611


def getTerminalSize():
    import os
    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            import struct
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                                                 '1234'))
        except:
            return
        return cr
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


parser = ArgumentParser('requests')
parser.add_argument('url')
parser.add_argument('-X', '--request',
                    default='GET')
parser.add_argument('-d', '--data')
parser.add_argument('-H', '--header', nargs='*')
parser.add_argument('-i', '--include',
                    help='Include HTTP headers in the response',
                    action='store_true',
                    default=False)

args = parser.parse_args()

if not args.url.lower().startswith('http'):
    args.url = 'http://' + args.url

headers = {}
if args.data is not None:
    try:
        headers['Content-Type'] = 'application/json'
        data = json.loads(args.data)
    except:
        data = args.data
    data = args.data
else:
    data = None

if args.header is not None:
    for header in args.header:
        key, value = header.split(': ', 2)
        headers[key] = value

response = requests.request(args.request, args.url,
                            data=args.data,
                            headers=headers)
try:
    lexer = get_lexer_by_name('json')
    formatter = get_formatter_by_name('terminal')
    to_print = highlight(json.dumps(json.loads(response.text),
                                    sort_keys=True,
                                    indent=4),
                         lexer, formatter)
except:
    try:
        lexer = guess_lexer(response.text)
        formatter = get_formatter_by_name('terminal')
        to_print = highlight(response.text, lexer, formatter)
    except:
        to_print = response.text

if args.include:
    to_print = json.dumps(dict(response.headers), indent=4) + "\n\n" + to_print

(width, height) = getTerminalSize()
if len(to_print.split('\n')) >= height:
    less = Popen(["less", '-R'], stdin=PIPE)
    less.communicate(to_print.encode('UTF8'))
else:
    print to_print
