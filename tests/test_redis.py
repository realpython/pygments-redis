#!/usr/bin/env python3
# python3 -m unittest -v tests/test_redis.py

import textwrap
import unittest

from pygments import token as Token

from pygments_redis import RedisLexer


class RedisTest(unittest.TestCase):
    def setUp(self):
        self.lexer = RedisLexer()

    def test_token_structure(self):
        lex = self.lexer
        self.assertIsInstance(lex.tokens, dict)
        self.assertIsInstance(lex.tokens["root"], list)
        for tup in lex.tokens["root"]:
            self.assertIsInstance(tup, tuple)
            self.assertEqual(len(tup), 2)

    def test_get_tokens(self):
        for name, (shellstr, tokentups) in PARAMS.items():
            with self.subTest(msg=name):
                # `msg` will be in [brackets] displayed next to
                # the method name for any failed runs
                self.assertEqual(
                    list(self.lexer.get_tokens(textwrap.dedent(shellstr))),
                    tokentups,
                )


PARAMS = {
    "test_get_tokens_case_insensitive": (
        """\
127.0.0.1:6379> PING
PONG
127.0.0.1:6379> ping
PONG
127.0.0.1:6379> ECHO hi
"hi"
127.0.0.1:6379> echo HELLO
"HELLO"
""",
        [
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "PING"),
            (Token.Text, "\n"),
            (Token.Text, "PONG"),
            (Token.Text, "\n"),
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "ping"),
            (Token.Text, "\n"),
            (Token.Text, "PONG"),
            (Token.Text, "\n"),
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "ECHO"),
            (Token.Text, " "),
            (Token.Text, "hi"),
            (Token.Text, "\n"),
            (Token.Text, '"hi"'),
            (Token.Text, "\n"),
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "echo"),
            (Token.Text, " "),
            (Token.Text, "HELLO"),
            (Token.Text, "\n"),
            (Token.Text, '"HELLO"'),
            (Token.Text, "\n"),
        ],
    ),
    "test_get_tokens_carat": (
        """\
127.0.0.1:6379> set k>e>y 127.0.0.1:6379>
OK
127.0.0.1:6379> get k>e>y
"127.0.0.1:6379>"
""",
        [
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "set"),
            (Token.Text, " "),
            (Token.Text, "k>e>y 127.0.0.1:6379>"),
            (Token.Text, "\n"),
            (Token.Text, "OK"),
            (Token.Text, "\n"),
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "get"),
            (Token.Text, " "),
            (Token.Text, "k>e>y"),
            (Token.Text, "\n"),
            (Token.Text, '"127.0.0.1:6379>"'),
            (Token.Text, "\n"),
        ],
    ),
    "test_get_tokens_dupe_cmd": (
        """\
127.0.0.1:6379> echo echo
"echo"
127.0.0.1:6379> echo ECHO
"ECHO"
""",
        [
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "echo"),
            (Token.Text, " "),
            (Token.Text, "echo"),
            (Token.Text, "\n"),
            (Token.Text, '"echo"'),
            (Token.Text, "\n"),
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "echo"),
            (Token.Text, " "),
            (Token.Text, "ECHO"),
            (Token.Text, "\n"),
            (Token.Text, '"ECHO"'),
            (Token.Text, "\n"),
        ],
    ),
    "test_get_tokens_error": (
        """\
127.0.0.1:6379> set foo bar
OK
127.0.0.1:6379> hget foo bar
(error) WRONGTYPE Operation against a key holding the wrong kind of value
127.0.0.1:6379> not a cmd
(error) ERR unknown command `not`, with args beginning with: `a`, `cmd`,
127.0.0.1:6379> CLUSTER INFO
ERR This instance has cluster support disabled
127.0.0.1:6379> DEBUG OBJECT dne
(error) ERR no such key
""",
        [
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "set"),
            (Token.Text, " "),
            (Token.Text, "foo bar"),
            (Token.Text, "\n"),
            (Token.Text, "OK"),
            (Token.Text, "\n"),
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "hget"),
            (Token.Text, " "),
            (Token.Text, "foo bar"),
            (Token.Text, "\n"),
            (Token.Keyword.Type, "(error)"),
            (Token.Text, " "),
            (
                Token.Text,
                "WRONGTYPE Operation against a key holding the wrong kind of value",  # noqa
            ),
            (Token.Text, "\n"),
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Text, "not a cmd"),
            (Token.Text, "\n"),
            (Token.Keyword.Type, "(error)"),
            (Token.Text, " "),
            (
                Token.Text,
                "ERR unknown command `not`, with args beginning with: `a`, `cmd`,",  # noqa
            ),
            (Token.Text, "\n"),
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "CLUSTER INFO"),
            (Token.Text, "\n"),
            (Token.Text, "ERR This instance has cluster support disabled"),
            (Token.Text, "\n"),
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "DEBUG OBJECT"),
            (Token.Text, " "),
            (Token.Text, "dne"),
            (Token.Text, "\n"),
            (Token.Keyword.Type, "(error)"),
            (Token.Text, " "),
            (Token.Text, "ERR no such key"),
            (Token.Text, "\n"),
        ],
    ),
    "test_get_tokens_noarg_cmds": (
        """\
127.0.0.1:6379> LASTSAVE
(integer) 1555707818
127.0.0.1:6379> TIME
1) "1555708182"
2) "689929"
127.0.0.1:6379> RANDOMKEY
"k>e>y"
127.0.0.1:6379> BGSAVE
Background saving started
""",
        [
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "LASTSAVE"),
            (Token.Text, "\n"),
            (Token.Keyword.Type, "(integer)"),
            (Token.Text, " "),
            (Token.Text, "1555707818"),
            (Token.Text, "\n"),
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "TIME"),
            (Token.Text, "\n"),
            (Token.Text, '1) "1555708182"'),
            (Token.Text, "\n"),
            (Token.Text, '2) "689929"'),
            (Token.Text, "\n"),
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "RANDOMKEY"),
            (Token.Text, "\n"),
            (Token.Text, '"k>e>y"'),
            (Token.Text, "\n"),
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "BGSAVE"),
            (Token.Text, "\n"),
            (Token.Text, "Background saving started"),
            (Token.Text, "\n"),
        ],
    ),
    "test_get_tokens_chrs": (
        """\
127.0.0.1:6379> psetex chili 1000000 Jalapeño
OK
127.0.0.1:6379> GET chili
"Jalape\xc3\xb1o"
127.0.0.1:6379> GET foo
"bar"
127.0.0.1:6379> DUMP foo
"\x00\x03bar\t\x006L\x18\xac\xba\xe0\x9e\xa6"
""",
        [
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "psetex"),
            (Token.Text, " "),
            (Token.Text, "chili 1000000 Jalapeño"),
            (Token.Text, "\n"),
            (Token.Text, "OK"),
            (Token.Text, "\n"),
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "GET"),
            (Token.Text, " "),
            (Token.Text, "chili"),
            (Token.Text, "\n"),
            (Token.Text, '"JalapeÃ±o"'),
            (Token.Text, "\n"),
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "GET"),
            (Token.Text, " "),
            (Token.Text, "foo"),
            (Token.Text, "\n"),
            (Token.Text, '"bar"'),
            (Token.Text, "\n"),
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "DUMP"),
            (Token.Text, " "),
            (Token.Text, "foo"),
            (Token.Text, "\n"),
            (Token.Text, '"\x00\x03bar\t\x006L\x18¬ºà\x9e¦"'),
            (Token.Text, "\n"),
        ],
    ),
    "test_get_tokens_float": (
        """\
127.0.0.1:6379> incrbyfloat lim 9.098
"59.098"
""",
        [
            (Token.Generic.Prompt, "127.0.0.1:6379>"),
            (Token.Text, " "),
            (Token.Keyword, "incrbyfloat"),
            (Token.Text, " "),
            (Token.Text, "lim 9.098"),
            (Token.Text, "\n"),
            (Token.Text, '"59.098"'),
            (Token.Text, "\n"),
        ],
    ),
}

if __name__ == "__main__":
    unittest.main()
