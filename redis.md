**Redis Strings — Reference & Examples**
## Other References

### Deleting keys

- `DEL key` — remove a key (any type). Returns number of keys removed (0 if key did not exist).

```bash
DEL mykey
# returns 1 if deleted, 0 if not present
```

If you want to remove only specific fields from a hash, use `HDEL key field [field ...]`.

```bash
HDEL myhash field1 field2
# returns number of fields removed
```


### Expiration / TTL

- `EXPIRE key seconds` — set time-to-live in seconds
- `TTL key` — returns remaining TTL in seconds (or -1 if no TTL, -2 if key missing)
- `SET key value EX seconds` — set value with expiry in one command

```bash
SET message:1 "hello" EX 10   # expires after 10 seconds
EXPIRE cache:42 3600           # set TTL to one hour
TTL cache:42                   # check remaining seconds
```


### Why Redis is fast

- Data is stored in RAM, so reads/writes are low-latency.
- Uses efficient I/O multiplexing (epoll/kqueue) for many connections.
- Single-threaded command execution avoids locks and context switching overhead.
- Highly optimized C implementation and simple data structures.


### Common use-cases

- Cache
- Message broker (pub/sub)
- Rate limiter
- Session store
- Distributed locks
- Leaderboards and rankings
- Real-time counters and analytics


## Hashes

Hashes map string fields to string values and are ideal for storing objects.

Use cases: user profiles, configuration, product records.

Core commands:

- `HSET key field value` — set field
- `HGET key field` — get field value
- `HMSET key field1 val1 field2 val2` — set multiple fields (deprecated in some clients; prefer `HSET key field1 val1 field2 val2`)
- `HGETALL key` — get all fields and values
- `HDEL key field [field ...]` — delete one or more fields
- `HINCRBY key field increment` — atomically increment integer field
- `HINCRBYFLOAT key field increment` — increment float field
- `HEXISTS key field` — check field exists
- `HKEYS key` — list fields
- `HVALS key` — list values

Examples:

```bash
HSET user:1 name "rahul" age 30
HGET user:1 name
HINCRBY user:1 visits 1
HGETALL user:1
```


## Lists

Ordered collections of strings; useful for queues, stacks, activity feeds.

Core commands:

- `LPUSH key value` — push to head
- `RPUSH key value` — push to tail
- `LPOP key` — pop from head
- `RPOP key` — pop from tail
- `LRANGE key start stop` — get range
- `LLEN key` — length
- `LTRIM key start stop` — trim list to range
- `LINDEX key index` — get element by index

Examples:

```bash
LPUSH tasks "task1"
RPUSH tasks "task2"
LRANGE tasks 0 -1
LPOP tasks
```


## Sets

Unordered collection of unique strings.

Use cases: unique visitors, tags, relationships, voting systems.

Core commands:

- `SADD key member` — add member
- `SREM key member` — remove member
- `SMEMBERS key` — list members
- `SISMEMBER key member` — test membership
- `SCARD key` — cardinality
- `SUNION key1 key2` — union
- `SINTER key1 key2` — intersection
- `SDIFF key1 key2` — difference

Examples:

```bash
SADD visitors user:1 user:2
SISMEMBER visitors user:3
SMEMBERS visitors
```


## Sorted sets (ZSET)

Sorted sets store unique members with a numeric score; members are ordered by score.

Commands you asked about:

- `ZADD key score member [score member ...]` — add or update members
- `ZRANGE key start stop [WITHSCORES]` — ascending range (by score)
- `ZREVRANGE key start stop [WITHSCORES]` — descending range
- `ZRANK key member` — 0-based rank in ascending order
- `ZREVRANK key member` — rank in descending order
- `ZSCORE key member` — return member's score
- `ZREM key member [member ...]` — remove member(s)
- `ZINCRBY key increment member` — increment member's score atomically

Examples:

```bash
ZADD leaderboard 100 alice 150 bob
ZRANGE leaderboard 0 9 WITHSCORES      # lowest scores first
ZREVRANGE leaderboard 0 9 WITHSCORES   # highest scores first
ZRANK leaderboard alice
ZSCORE leaderboard bob
ZINCRBY leaderboard 10 alice            # add 10 to alice's score
```

Complexity notes: most single-element operations are O(log N); range reads are O(log N + M) where M is number of returned elements.

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






 sbse pahle : lets start with the strings: 

 in this i know : 
 set key value 
 get key 
 incr counter
 decr counter
 append key value // adds value in the string i suppose...
 strlen key //to find the length of the string i guess..
 setex key seconds value # set with expiration 
 setnx key value  // set if does not exists 
 mset key1 val1 key2 val2 # multiple set 
 mget key1




 # Hashes : 
 maps between strings fields and string values: aik tarah se to sara hi data isi form me hai : pr yha pr
 
 Use cases:
 user profiles
 object storage
 configuration settings 
 product details

HSET key field value
HGET KEY field
HMSET key field1 value1 field2 value2 
HGETALL key
HDEL key field # what happens if the i do not mention the field ?: will get error , what you should actually do is : 
DEL key # to delete the hash ...

HINCRBY key field increment 
HEXISTS key field 
HKEYS key # is data ke konse konse key hai 
HVALS key # is data ke koinse konse value hai 


# Lists:
ordered collection of strings , can act as stacks or queues

task queues
activity feeds 
recent items 
message queues

LPUSH key value #add to the head
RPUSH key value #add  to the tail
LPOP key #remove from the head 
RPOP key # remove form the tail 
LRANGE key start stop 
LLEN key
LTRIM key start stop
LINDEX key index



# SET : 
unordered collection of unique strings. 

use cases:
unique visitors
tags
relationships 
voting systems

SADD key member #add this member to this set
SREM key member. #remove this member from the set with the key key
SMEMBERS key   #mention all members of the key
SISMEMBER key member #is this the member of this ??
SCARD key #cardinality of this set
SUNION key1 key2 #Union of sets
SINTER key1 key2 #Intersection
SDIFF key1 key2 #Diffrence


# Ordered sets : 

ZADD key score member # exmpl: ZADD leaderboard 100 alice 150 bob

ZRANGE key start stop [WITHSCORES] # ZRANGE leaderboard 0 9 withscores gives top 10 lowest scroes  - returns in ascending score.

ZREVRANGE key start stop [WITHSCORES] # Same as zrange but descending (highest scores first)

ZRANK key member - ZRANK leaderboard alice : return 0-based rank of member in ascending order , or (nil) if missing. Example: zrank leaderboard alice

ZREVRANK key member - return rank in descending order, or (nil) if missing , Example: ZREVRANK leaderboard alice

ZSCORE: zscore key member - return the numeric score of member(string) or (nil) if not present. Example: zscore leaderboard bob

ZREM key member [ member, ....]-remove one or more members; returns number of members, example: ZREM leaderboard alice

ZINCRBY key increment member- increment member's score by increment ( creates member with score = increment if missing) leaderboard 10 alice 






