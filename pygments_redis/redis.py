"""Lexer for `Redis <https://redis.io/>`_ CLI/REPL output.

Author: Brad Solomon <brad.solomon.1124@gmail.com>
"""

__all__ = ["RedisLexer"]

import re

from pygments import lexer, token


class RedisLexer(lexer.RegexLexer):
    """Lexer for `Redis <https://redis.io/>`_ CLI/REPL output."""

    name = "Redis"
    aliases = ["redis"]
    flags = re.MULTILINE | re.UNICODE | re.IGNORECASE

    # This lexer only has one state, 'root'.
    # Each element in the list is a (regex, action) tuple.
    # (There is a third element, new_state, that we don't need.)
    # http://pygments.org/docs/lexerdevelopment/#regexlexer
    #
    # We keep the tokenization fairly high-level rather than getting
    # overly granular.  Brief description of tokens follows.
    #
    # A token can be:
    #
    # (1) A prompt, which can potentially take a whole bunch of
    # different forms depending on the -h and -p flags, such as:
    #
    # - 127.0.0.1:6379>, localhost:6379>, 127.0.0.1:6379[10]>, [::1]:6379>
    # - redis://user:secret@localhost:6379/0?foo=bar&qux=baz>
    # - redis://myapp-001.abcdef.0001.use1.cache.amazonaws.com:6379/0>
    # - not connected>, lua debugger>
    #
    # Luckily, a literal > is not a URI char from RFC 3986, so we don't
    # need to get too fancy, but just watch out for one edge case like
    # this:
    #     127.0.0.1:6379> set k1 "abcd>efg"
    #     127.0.0.1:6379> get k1
    #     "abcd>efg"
    # (For that, we get around by using the fact that quotation mark
    # is also not in the URI set.)
    # For more on Redis' URI see:
    # - https://github.com/antirez/redis/blob/unstable/src/redis-cli.c
    # - https://www.iana.org/assignments/uri-schemes/prov/redis
    #
    # (2) A command.  Case-insensitive, may be one or more words.
    # Complete set of Redis commands from https://redis.io/commands.
    # Grabbed via:
    #     from urllib.request import urlopen
    #     from bs4 import BeautifulSoup
    #     with urlopen('https://redis.io/commands') as response:
    #         html = response.read()
    #         soup = BeautifulSoup(html, 'html.parser')
    #         tags = soup.find_all("span", {"class": "command"})
    #         for t in tags:
    #             print('"{}",'.format(t.text.strip().partition("\n")[0]))
    #
    # (3) A 'reply type' (not sure if there's a more technical term).
    # See cliFormatReplyTTY from:
    # https://github.com/antirez/redis/blob/unstable/deps/hiredis/read.h
    # for the logic and exhaustive set.
    #
    # (4) 'Other.'  That is, we treat both arguments to commands and
    # any part of the reply *except* the parenthesized reply type
    # as text.  We could get fancy with this and include special subsets
    # for stuff like String.Double, but probably overkill given
    # Redis' minimalist style itself.  This also includes whitespace

    tokens = {
        "root": [
            (r"^[^>\n\"]*>", token.Generic.Prompt),
            (
                lexer.words(
                    (
                        r"APPEND",
                        r"AUTH",
                        r"BGREWRITEAOF",
                        r"BGSAVE",
                        r"BITCOUNT",
                        r"BITFIELD",
                        r"BITOP",
                        r"BITPOS",
                        r"BLPOP",
                        r"BRPOP",
                        r"BRPOPLPUSH",
                        r"BZPOPMIN",
                        r"BZPOPMAX",
                        r"CLIENT ID",
                        r"CLIENT KILL",
                        r"CLIENT LIST",
                        r"CLIENT GETNAME",
                        r"CLIENT PAUSE",
                        r"CLIENT REPLY",
                        r"CLIENT SETNAME",
                        r"CLIENT UNBLOCK",
                        r"CLUSTER ADDSLOTS",
                        r"CLUSTER COUNT-FAILURE-REPORTS",
                        r"CLUSTER COUNTKEYSINSLOT",
                        r"CLUSTER DELSLOTS",
                        r"CLUSTER FAILOVER",
                        r"CLUSTER FORGET",
                        r"CLUSTER GETKEYSINSLOT",
                        r"CLUSTER INFO",
                        r"CLUSTER KEYSLOT",
                        r"CLUSTER MEET",
                        r"CLUSTER NODES",
                        r"CLUSTER REPLICATE",
                        r"CLUSTER RESET",
                        r"CLUSTER SAVECONFIG",
                        r"CLUSTER SET-CONFIG-EPOCH",
                        r"CLUSTER SETSLOT",
                        r"CLUSTER SLAVES",
                        r"CLUSTER REPLICAS",
                        r"CLUSTER SLOTS",
                        r"COMMAND",
                        r"COMMAND COUNT",
                        r"COMMAND GETKEYS",
                        r"COMMAND INFO",
                        r"CONFIG GET",
                        r"CONFIG REWRITE",
                        r"CONFIG SET",
                        r"CONFIG RESETSTAT",
                        r"DBSIZE",
                        r"DEBUG OBJECT",
                        r"DEBUG SEGFAULT",
                        r"DECR",
                        r"DECRBY",
                        r"DEL",
                        r"DISCARD",
                        r"DUMP",
                        r"ECHO",
                        r"EVAL",
                        r"EVALSHA",
                        r"EXEC",
                        r"EXISTS",
                        r"EXPIRE",
                        r"EXPIREAT",
                        r"FLUSHALL",
                        r"FLUSHDB",
                        r"GEOADD",
                        r"GEOHASH",
                        r"GEOPOS",
                        r"GEODIST",
                        r"GEORADIUS",
                        r"GEORADIUSBYMEMBER",
                        r"GET",
                        r"GETBIT",
                        r"GETRANGE",
                        r"GETSET",
                        r"HDEL",
                        r"HEXISTS",
                        r"HGET",
                        r"HGETALL",
                        r"HINCRBY",
                        r"HINCRBYFLOAT",
                        r"HKEYS",
                        r"HLEN",
                        r"HMGET",
                        r"HMSET",
                        r"HSET",
                        r"HSETNX",
                        r"HSTRLEN",
                        r"HVALS",
                        r"INCR",
                        r"INCRBY",
                        r"INCRBYFLOAT",
                        r"INFO",
                        r"KEYS",
                        r"LASTSAVE",
                        r"LINDEX",
                        r"LINSERT",
                        r"LLEN",
                        r"LPOP",
                        r"LPUSH",
                        r"LPUSHX",
                        r"LRANGE",
                        r"LREM",
                        r"LSET",
                        r"LTRIM",
                        r"MEMORY DOCTOR",
                        r"MEMORY HELP",
                        r"MEMORY MALLOC-STATS",
                        r"MEMORY PURGE",
                        r"MEMORY STATS",
                        r"MEMORY USAGE",
                        r"MGET",
                        r"MIGRATE",
                        r"MONITOR",
                        r"MOVE",
                        r"MSET",
                        r"MSETNX",
                        r"MULTI",
                        r"OBJECT",
                        r"PERSIST",
                        r"PEXPIRE",
                        r"PEXPIREAT",
                        r"PFADD",
                        r"PFCOUNT",
                        r"PFMERGE",
                        r"PING",
                        r"PSETEX",
                        r"PSUBSCRIBE",
                        r"PUBSUB",
                        r"PTTL",
                        r"PUBLISH",
                        r"PUNSUBSCRIBE",
                        r"QUIT",
                        r"RANDOMKEY",
                        r"READONLY",
                        r"READWRITE",
                        r"RENAME",
                        r"RENAMENX",
                        r"RESTORE",
                        r"ROLE",
                        r"RPOP",
                        r"RPOPLPUSH",
                        r"RPUSH",
                        r"RPUSHX",
                        r"SADD",
                        r"SAVE",
                        r"SCARD",
                        r"SCRIPT DEBUG",
                        r"SCRIPT EXISTS",
                        r"SCRIPT FLUSH",
                        r"SCRIPT KILL",
                        r"SCRIPT LOAD",
                        r"SDIFF",
                        r"SDIFFSTORE",
                        r"SELECT",
                        r"SET",
                        r"SETBIT",
                        r"SETEX",
                        r"SETNX",
                        r"SETRANGE",
                        r"SHUTDOWN",
                        r"SINTER",
                        r"SINTERSTORE",
                        r"SISMEMBER",
                        r"SLAVEOF",
                        r"REPLICAOF",
                        r"SLOWLOG",
                        r"SMEMBERS",
                        r"SMOVE",
                        r"SORT",
                        r"SPOP",
                        r"SRANDMEMBER",
                        r"SREM",
                        r"STRLEN",
                        r"SUBSCRIBE",
                        r"SUNION",
                        r"SUNIONSTORE",
                        r"SWAPDB",
                        r"SYNC",
                        r"TIME",
                        r"TOUCH",
                        r"TTL",
                        r"TYPE",
                        r"UNSUBSCRIBE",
                        r"UNLINK",
                        r"UNWATCH",
                        r"WAIT",
                        r"WATCH",
                        r"ZADD",
                        r"ZCARD",
                        r"ZCOUNT",
                        r"ZINCRBY",
                        r"ZINTERSTORE",
                        r"ZLEXCOUNT",
                        r"ZPOPMAX",
                        r"ZPOPMIN",
                        r"ZRANGE",
                        r"ZRANGEBYLEX",
                        r"ZREVRANGEBYLEX",
                        r"ZRANGEBYSCORE",
                        r"ZRANK",
                        r"ZREM",
                        r"ZREMRANGEBYLEX",
                        r"ZREMRANGEBYRANK",
                        r"ZREMRANGEBYSCORE",
                        r"ZREVRANGE",
                        r"ZREVRANGEBYSCORE",
                        r"ZREVRANK",
                        r"ZSCORE",
                        r"ZUNIONSTORE",
                        r"SCAN",
                        r"SSCAN",
                        r"HSCAN",
                        r"ZSCAN",
                        r"XINFO",
                        r"XADD",
                        r"XTRIM",
                        r"XDEL",
                        r"XRANGE",
                        r"XREVRANGE",
                        r"XLEN",
                        r"XREAD",
                        r"XGROUP",
                        r"XREADGROUP",
                        r"XACK",
                        r"XCLAIM",
                        r"XPENDING",
                    ),
                    prefix=r"(?<=> )",
                ),
                token.Keyword,
            ),
            (r"^\([^)]+\)", token.Keyword.Type),
            (r"\s+", token.Text),
            (r".+?$", token.Text),
        ]
    }
