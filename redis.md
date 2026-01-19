**Redis Strings — Reference & Examples**

## Index
/- [Index](#index)
- [Overview](#overview)
- [Basic SET/GET](#basic-setget)
- [SET options (NX, XX, EX, PX, KEEPTTL, GET)](#set-options-nx-xx-ex-px-keepttl-get)
- [Multiple keys: MSET / MGET](#multiple-keys-mset--mget)
- [Atomic get-and-set: GETSET](#atomic-get-and-set-getset)
- [Numeric operations (INCR / DECR / INCRBY / INCRBYFLOAT)](#numeric-operations-incr--decr--incrby--incrbyfloat)
- [String mutation: APPEND / SETRANGE / GETRANGE / STRLEN](#string-mutation-append--setrange--getrange--strlen)
- [Bit operations: BITCOUNT / BITOP / BITPOS / BITFIELD](#bit-operations-bitcount--bitop--bitpos--bitfield)
- [Performance and complexity notes](#performance-and-complexity-notes)
- [Best practices and alternatives](#best-practices-and-alternatives)
- [Quick redis-cli examples](#quick-redis-cli-examples)


## Overview

Redis Strings are the simplest value type in Redis. They can contain any binary sequence, e.g., a JPEG image or a serialized object. The maximum length of a string value is 512 MB.


## Basic SET/GET

- SET: store a string value

```bash
SET key value
```

- GET: retrieve a string value

```bash
GET key
```


## SET options (NX, XX, EX, PX, KEEPTTL, GET)

The `SET` command supports several useful options.

- `NX` — set only if key does not exist (create-once)
- `XX` — set only if key already exists
- `EX seconds` — set expire time in seconds
- `PX milliseconds` — set expire time in milliseconds
- `KEEPTTL` — retain existing TTL
- `GET` — return old value and set new value atomically (Redis 6.2+)

Examples:

```bash
SET user:1:name "rahul" NX            # create only if not exists
SET session:123 token EX 3600          # set with 1 hour expiry
SET key newvalue GET                    # atomically get old then set new
```


## Multiple keys: MSET / MGET

- `MSET key1 val1 key2 val2 ...` — set multiple keys atomically
- `MGET key1 key2 ...` — get multiple values

```bash
MSET msg:1 "b_bye_baby" msg:2 "i_love_you" msg:3 "take_care"
MGET msg:1 msg:2 msg:3
```


## Atomic get-and-set: GETSET

- `GETSET key value` — set new value and return the old value (atomic)

```bash
GETSET counter "0"   # returns previous value
```


## Numeric operations (INCR / DECR / INCRBY / INCRBYFLOAT)

Strings can hold integer or floating-point numbers and support atomic arithmetic operations.

- `INCR key` — increment integer value by 1
- `INCRBY key increment` — increment by specified integer
- `INCRBYFLOAT key increment` — increment by floating point
- `DECR key` — decrement by 1
- `DECRBY key decrement` — decrement by specified integer

Examples:

```bash
SET visits 0
INCR visits          # 1
INCRBY visits 2      # 3
INCRBYFLOAT price 0.15
DECR visits          # 2
```

Note: these commands are atomic and will create the key if it does not exist (initial value 0).


## String mutation: APPEND / SETRANGE / GETRANGE / STRLEN

- `APPEND key value` — append a value to existing string (returns new length)
- `SETRANGE key offset value` — overwrite part of the string starting at offset
- `GETRANGE key start end` — get substring (inclusive indices)
- `STRLEN key` — get length of string in bytes

Examples:

```bash
SET greeting "Hello"
APPEND greeting ", world"         # greeting now "Hello, world"
GETRANGE greeting 0 4              # returns "Hello"
SETRANGE greeting 7 "Redis"       # modify starting at offset 7
STRLEN greeting                    # returns length
```


## Bit operations: BITCOUNT / BITOP / BITPOS / BITFIELD

Strings are binary-safe and Redis provides bit-level operations useful for bitmaps and compact counters.

- `BITCOUNT key [start end]` — count set bits in a string or range
- `BITOP op destkey key [key ...]` — perform bitwise operations (AND/OR/XOR/NOT)
- `BITPOS key bit [start] [end]` — first bit with value 0 or 1
- `BITFIELD key [GET/SET/INCRBY ...]` — complex bitfield manipulations (useful for packed integers)

Examples:

```bash
SETBIT mybitmap 10 1                # set bit at offset 10
BITCOUNT mybitmap                   # count set bits
BITOP OR dest src1 src2             # dest = src1 OR src2
BITFIELD stats INCRBY u16 0 1       # increment unsigned 16-bit at pos 0
```


## Performance and complexity notes

- Most basic operations (`GET`, `SET`, `INCR`, `DECR`, `MGET`, `MSET`, `GETSET`) are O(1).
- Operations that touch the whole string or a large range are O(N) where N is the length of the string or the range (examples: `GETRANGE`, `SETRANGE` when they copy/modify many bytes, `BITCOUNT`, `BITOP`).
- `APPEND` is typically efficient but may be O(1) amortized; extremely large appends may incur reallocation costs.
- Strings can be up to 512 MB; if you routinely manipulate large blobs consider using hashes/streams/RedisJSON or an external object store.


## Best practices and alternatives

- Use `NX` with `SET` for safe creation (avoid race conditions).
- Prefer `MSET`/`MGET` to reduce round-trips when dealing with many keys.
- For structured data prefer `HASH` or `RedisJSON` when you need to update individual fields frequently.
- Use `BITFIELD` and bitmaps for compact counters, flags, and hyperloglog-like patterns when appropriate.


## Quick redis-cli examples

Copyable snippets to try in `redis-cli`:

```bash
# Basic
SET user:1:name rahul
GET user:1:name

# Conditional set
SET user:2:name "alice" NX

# With expiry
SET session:42 token EX 3600

# Multiple
MSET a 1 b 2 c 3
MGET a b c

# Numeric
SET counter 100
INCR counter
INCRBY counter 50
INCRBYFLOAT balance 3.1415

# Substring / mutation
SET msg "hello"
APPEND msg ", world"
GETRANGE msg 0 4
SETRANGE msg 7 "Redis"

# Bits
SETBIT flags 100 1
BITCOUNT flags
BITOP AND out f1 f2
```



# Other in general References Guides: 

To delete a value : del key_name
del name 

the output 0 means , it does not exist or it remains unsuccesful , or the output 1 means it is deleted or the process is sucessful.(it returns a integer number meaning deleted sucessfull or not ....)


To setup ttl to have the value for a limited time: just to make sure we are not having stale data in our redis cache we can set a ttl to the key value pair using : 

expire key_name 360000 or something similar like this ... 
 
 expire message:1 10 ## it it might also be both the seting up the value and deletion together : 

 set message:1 "hello world" ex 10  ## it will set the value for 10 seconds only ...


 why is redis insane fast : 
 > data stored in RAM, 
 > uses I/O multiplexing (epoll), 
 > single threaded -> no locks, 
 > optimized C implementation.

 redis is not only cache : 
 cache 
 message broker(pub/sub)
 rate limiter
 session store
 distributed locks 
 leaderboards 
 real-time counters

