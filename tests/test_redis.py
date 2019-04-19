#!/usr/bin/env python3
# python3 -m unittest tests/test_redis.py

import unittest

from pygments_redis import RedisLexer


class PythonTest(unittest.TestCase):
    def setUp(self):
        self.lexer = RedisLexer()

    def test_token_structure(self):
        lex = self.lexer
        self.assertIsInstance(lex.tokens, dict)
        self.assertIsInstance(lex.tokens["root"], list)
        for tup in lex.tokens["root"]:
            self.assertIsInstance(tup, tuple)
            self.assertEqual(len(tup), 2)


if __name__ == "__main__":
    unittest.main()
