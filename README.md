request
=======

A curl like command line, with automatic pagination when needed, and automatic highlighting.

usage
-----

    usage: requests [-h] [-X REQUEST] [-d DATA] [-H [HEADER [HEADER ...]]] [-i]
                    url

    positional arguments:
      url

    optional arguments:
      -h, --help            show this help message and exit
      -X REQUEST, --request REQUEST
      -d DATA, --data DATA
      -H [HEADER [HEADER ...]], --header [HEADER [HEADER ...]]
      -i, --include         Include HTTP headers in the response
