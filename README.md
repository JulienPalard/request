request
=======

A curl like command line in 66 lines of Python, with pagination and highlighting.

One may prefer using HTTPie, the same with a lot of features.

usage
-----

    usage: request [-h] [-X GET] [-d DATA] [-H [HEADER [HEADER ...]]] [-i] url

    positional arguments:
      url

    optional arguments:
      -h, --help            show this help message and exit
      -X GET, --request GET
      -d DATA, --data DATA  Data to send in the body of the request. If you're
                            giving JSON, an appropriate header will be set.
      -H [HEADER [HEADER ...]], --header [HEADER [HEADER ...]]
      -i, --include         Include HTTP headers in the response
