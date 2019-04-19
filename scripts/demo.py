#!/usr/bin/env python3

"""A simple demo of the Redis lexer's colorized result."""

import pygments
import pygments.formatters.terminal

from pygments_redis import RedisLexer

lexer = RedisLexer()


def pprint(code: str) -> None:
    print(
        pygments.highlight(
            code, lexer, pygments.formatters.terminal.TerminalFormatter()
        )
    )


code = '''\
127.0.0.1:6379> SET foo bar
OK
127.0.0.1:6379> GET foo
"bar"'''


if __name__ == "__main__":
    import sys

    sys.exit(pprint(code))
