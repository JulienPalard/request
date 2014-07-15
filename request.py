#!/usr/bin/env python

import requests
from argparse import ArgumentParser
from subprocess import Popen, PIPE
import json
from pygments import highlight
from pygments.lexers import guess_lexer, JSONLexer
from pygments.formatters import TerminalFormatter
from contextlib import suppress


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
    with suppress(Exception):
        json.loads(args.data)
        headers['Content-Type'] = 'application/json'
    headers.update(header.split(': ', 1) for header in args.header)
    return args.method, args.url, headers, args.data


def do_query(method, url, headers, data):
    return requests.request(method, url, data=data, headers=headers)


def pretty_print(text):
    with suppress(Exception):
        return highlight(json.dumps(json.loads(text), indent=4),
                         JSONLexer(), TerminalFormatter())
    with suppress(Exception):
        return highlight(text, guess_lexer(text), TerminalFormatter())
    return text


def print_response(args, response):
    to_print = ""
    if args.include:
        to_print += pretty_print(json.dumps(dict(response.headers))) + "\n\n"
    to_print += pretty_print(response.text)
    Popen(["less", '-XFR'], stdin=PIPE).communicate(to_print.encode('UTF8'))

args = parse_args()
print_response(args, do_query(*prepare_query(args)))
