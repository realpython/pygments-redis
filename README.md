# pygments-redis

[![Build](https://img.shields.io/circleci/project/github/realpython/pygments-redis.svg)](https://circleci.com/gh/realpython/pygments-redis/tree/master)
[![License](https://img.shields.io/github/license/realpython/pygments-redis.svg)](https://github.com/realpython/pygments-redis/blob/master/LICENSE)
[![Version](https://img.shields.io/pypi/v/pygments-redis.svg)](https://pypi.org/project/pygments-redis/)

----

 A minimalistic Pygments lexer for the [Redis](https://redis.io/) CLI.

 This lexer differentiates four components of input/output from the `redis-cli` shell:

 - The prompt
 - A command
 - A reply type
 - "Everything else"
