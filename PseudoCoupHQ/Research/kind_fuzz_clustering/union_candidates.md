# union candidates at the value grain

Built 2026-08-20 by `make_union_candidates.py`, from
`dominance_valuegrain.json`. Nothing was run to produce it.

This is the Hub-facing half of log 043. The order rebuilt at the
value grain has **209 maximal leaves of 239**, so there is no one
operation that carries the node. What follows is the next
question: which maximal operations can be laid on top of one
another without either giving up a measured answer.

Two leaves are COMPATIBLE when they never carry different tokens
on an element they both speak on. Two kinds of compatible edge,
and the difference matters to anyone reading this as evidence:

| edge | meaning | what it is worth |
|---|---|---|
| agreeing | they share elements and agree on every one | measured sameness |
| vacuous | they share no element at all | assembly, not evidence |

A union of any size is possible exactly when every PAIR in it is
compatible, so the assemblies below are the maximal cliques of
that graph, enumerated exactly.

Coverage is elements out of the 1156 in the merged grid.

## the headline, per family

| family | leaves | maximal | agreeing pairs | vacuous pairs | blocked pairs | widest assembly | its coverage |
|---|---|---|---|---|---|---|---|
| arithmetic | 60 | 59 | 0 | 0 | 1711 | 0 | 0 of 1156 |
| comparison | 83 | 72 | 1 | 12 | 2543 | 2 | 531 of 1156 |
| logical | 36 | 24 | 10 | 1 | 265 | 2 | 1156 of 1156 |
| bitwise | 33 | 27 | 2 | 0 | 349 | 2 | 64 of 1156 |
| shift | 21 | 21 | 1 | 0 | 209 | 2 | 16 of 1156 |
| other | 6 | 6 | 0 | 0 | 15 | 0 | 0 of 1156 |

**14 agreeing pairs against 5092 blocked, within a family.** The 
agreeing pairs are the whole short list of places where two maximal
operations could be one operation, and they are the answer this
log hands the Hub.

## arithmetic

60 leaves, 59 of them maximal. Compatible pairs: 0 agreeing,
0 vacuous. Blocked pairs: 1711.

**No agreeing pair at all.** Every pair of maximal leaves in
this family either contradicts the other somewhere or shares no
element with it.

**No assembly of two or more exists here.** Every pair of maximal
leaves in this family blocks, so nothing can be laid on top of
anything else.

The blocked unions, with one blocking element quoted each.

| left | right | blocking element | left answers | right answers |
|---|---|---|---|---|
| `php.%` | `python.%` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `fractional:0.0, raise:TypeError, whole:0` |
| `php.%` | `python.*` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `fractional:2.25, fractional:9/4, raise:TypeErr` |
| `php.%` | `python.**` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `fractional:1.8371173070874, raise:TypeError` |
| `php.%` | `python.+` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `fractional:3, raise:TypeError, whole:3` |
| `php.%` | `python.-` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `fractional:0.0, raise:TypeError, whole:0` |
| `php.%` | `python./` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `fractional:1, raise:TypeError, whole:1` |
| `php.%` | `python.//` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `fractional:1, raise:TypeError, whole:1` |
| `php.%` | `python.@` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `raise:TypeError` |
| `php.%` | `ruby.%` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `fractional:0.0, raise:NoMethodError, whole:0` |
| `php.%` | `ruby.*` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `fractional:2.25, fractional:9/4, raise:NoMetho` |
| `php.%` | `ruby.**` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `fractional:1.8371173070874, raise:NoMethodErro` |
| `php.%` | `ruby.+` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `fractional:3, raise:NoMethodError, whole:3` |
| `php.%` | `ruby.-` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `fractional:0.0, raise:NoMethodError, whole:0` |
| `php.%` | `ruby./` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `fractional:1, raise:NoMethodError, whole:1` |
| `php.*` | `python.%` | `fractional\|base_1_5\|fractional\|base_1_5` | `fractional:2.25` | `fractional:0.0, raise:TypeError, whole:0` |
| `php.*` | `python.*` | `fractional\|base_1_5\|fractional\|base_1_5` | `fractional:2.25` | `fractional:2.25, fractional:9/4, raise:TypeErr` |
| `php.*` | `python.**` | `fractional\|base_1_5\|fractional\|base_1_5` | `fractional:2.25` | `fractional:1.8371173070874, raise:TypeError` |
| `php.*` | `python.+` | `fractional\|base_1_5\|fractional\|base_1_5` | `fractional:2.25` | `fractional:3, raise:TypeError, whole:3` |
| `php.*` | `python.-` | `fractional\|base_1_5\|fractional\|base_1_5` | `fractional:2.25` | `fractional:0.0, raise:TypeError, whole:0` |
| `php.*` | `python./` | `fractional\|base_1_5\|fractional\|base_1_5` | `fractional:2.25` | `fractional:1, raise:TypeError, whole:1` |

## comparison

83 leaves, 72 of them maximal. Compatible pairs: 1 agreeing,
12 vacuous. Blocked pairs: 2543.

The agreeing pairs, cross-language first.

| left | right | shared elements | union elements | |
|---|---|---|---|---|
| `cpp.!=` | `cpp.not_eq` | 282 | 282 | same language |

The widest assembly of two or more: 2 maximal leaves covering
531 of 1156 elements, on 0 agreeing and 1 vacuous edges.

```
  dart.<  typescript.in
```

The blocked unions, with one blocking element quoted each.

| left | right | blocking element | left answers | right answers |
|---|---|---|---|---|
| `php.!=` | `python.!=` | `fractional\|base_1_5\|fractional\|inf` | `truth:true` | `raise:OverflowError, truth:true` |
| `php.!=` | `python.<` | `fractional\|base_1_5\|fractional\|inf` | `truth:true` | `raise:OverflowError, truth:true` |
| `php.!=` | `python.<=` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:false` | `truth:true` |
| `php.!=` | `python.==` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:false` | `truth:true` |
| `php.!=` | `python.>` | `fractional\|base_1_5\|fractional\|base_pi` | `truth:true` | `truth:false` |
| `php.!=` | `python.>=` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:false` | `truth:true` |
| `php.!=` | `python.in` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:false` | `raise:TypeError` |
| `php.!=` | `python.is` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:false` | `truth:false, truth:true` |
| `php.!=` | `python.is not` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:false` | `truth:false, truth:true` |
| `php.!=` | `ruby.!=` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:false` | `raise:NoMethodError, truth:false` |
| `php.!=` | `ruby.<` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:false` | `raise:NoMethodError, truth:false` |
| `php.!=` | `ruby.<=` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:false` | `raise:NoMethodError, truth:true` |
| `php.!=` | `ruby.<=>` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:false` | `raise:NoMethodError, whole:0` |
| `php.!=` | `ruby.==` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:false` | `raise:NoMethodError, truth:true` |
| `php.!=` | `ruby.===` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:false` | `raise:NoMethodError, truth:true` |
| `php.!=` | `ruby.>` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:false` | `raise:NoMethodError, truth:false` |
| `php.!=` | `ruby.>=` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:false` | `raise:NoMethodError, truth:true` |
| `php.!==` | `python.!=` | `fractional\|base_1_5\|fractional\|inf` | `truth:true` | `raise:OverflowError, truth:true` |
| `php.!==` | `python.<` | `fractional\|base_1_5\|fractional\|inf` | `truth:true` | `raise:OverflowError, truth:true` |
| `php.!==` | `python.<=` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:false` | `truth:true` |

## logical

36 leaves, 24 of them maximal. Compatible pairs: 10 agreeing,
1 vacuous. Blocked pairs: 265.

The agreeing pairs, cross-language first.

| left | right | shared elements | union elements | |
|---|---|---|---|---|
| `cpp.&&` | `dart.&&` | 4 | 567 | cross-language |
| `cpp.and` | `dart.&&` | 4 | 567 | cross-language |
| `cpp.or` | `dart.||` | 4 | 567 | cross-language |
| `cpp.||` | `dart.||` | 4 | 567 | cross-language |
| `php.&&` | `php.and` | 1156 | 1156 | same language |
| `php.or` | `php.||` | 1156 | 1156 | same language |
| `ruby.&&` | `ruby.and` | 1156 | 1156 | same language |
| `ruby.or` | `ruby.||` | 1156 | 1156 | same language |
| `cpp.&&` | `cpp.and` | 562 | 562 | same language |
| `cpp.or` | `cpp.||` | 562 | 562 | same language |

The widest assembly of two or more: 2 maximal leaves covering
1156 of 1156 elements, on 1 agreeing and 0 vacuous edges.

```
  php.&&  php.and
```

The blocked unions, with one blocking element quoted each.

| left | right | blocking element | left answers | right answers |
|---|---|---|---|---|
| `php.&&` | `python.and` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5, fractional:3/2` |
| `php.&&` | `python.or` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5, fractional:3/2` |
| `php.&&` | `ruby.&&` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5, fractional:3/2, raise:NoMethod` |
| `php.&&` | `ruby.and` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5, fractional:3/2, raise:NoMethod` |
| `php.&&` | `ruby.or` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5, fractional:3/2, raise:NoMethod` |
| `php.&&` | `ruby.||` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5, fractional:3/2, raise:NoMethod` |
| `php.&&` | `typescript.&&` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5` |
| `php.&&` | `typescript.??` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5` |
| `php.&&` | `typescript.||` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5` |
| `php.and` | `python.and` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5, fractional:3/2` |
| `php.and` | `python.or` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5, fractional:3/2` |
| `php.and` | `ruby.&&` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5, fractional:3/2, raise:NoMethod` |
| `php.and` | `ruby.and` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5, fractional:3/2, raise:NoMethod` |
| `php.and` | `ruby.or` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5, fractional:3/2, raise:NoMethod` |
| `php.and` | `ruby.||` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5, fractional:3/2, raise:NoMethod` |
| `php.and` | `typescript.&&` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5` |
| `php.and` | `typescript.??` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5` |
| `php.and` | `typescript.||` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5` |
| `php.or` | `python.and` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5, fractional:3/2` |
| `php.or` | `python.or` | `fractional\|base_1_5\|fractional\|base_1_5` | `truth:true` | `fractional:1.5, fractional:3/2` |

## bitwise

33 leaves, 27 of them maximal. Compatible pairs: 2 agreeing,
0 vacuous. Blocked pairs: 349.

The agreeing pairs, cross-language first.

| left | right | shared elements | union elements | |
|---|---|---|---|---|
| `cpp.&` | `cpp.bitand` | 64 | 64 | same language |
| `cpp.bitor` | `cpp.|` | 64 | 64 | same language |

The widest assembly of two or more: 2 maximal leaves covering
64 of 1156 elements, on 1 agreeing and 0 vacuous edges.

```
  cpp.&  cpp.bitand
```

The blocked unions, with one blocking element quoted each.

| left | right | blocking element | left answers | right answers |
|---|---|---|---|---|
| `php.&` | `python.&` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `raise:TypeError` |
| `php.&` | `python.^` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `raise:TypeError` |
| `php.&` | `python.|` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `raise:TypeError` |
| `php.&` | `ruby.&` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `raise:NoMethodError` |
| `php.&` | `ruby.^` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `raise:NoMethodError` |
| `php.&` | `ruby.|` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `raise:NoMethodError` |
| `php.^` | `python.&` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `raise:TypeError` |
| `php.^` | `python.^` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `raise:TypeError` |
| `php.^` | `python.|` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `raise:TypeError` |
| `php.^` | `ruby.&` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `raise:NoMethodError` |
| `php.^` | `ruby.^` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `raise:NoMethodError` |
| `php.^` | `ruby.|` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `raise:NoMethodError` |
| `php.|` | `python.&` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `raise:TypeError` |
| `php.|` | `python.^` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `raise:TypeError` |
| `php.|` | `python.|` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `raise:TypeError` |
| `php.|` | `ruby.&` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `raise:NoMethodError` |
| `php.|` | `ruby.^` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `raise:NoMethodError` |
| `php.|` | `ruby.|` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `raise:NoMethodError` |
| `python.&` | `ruby.&` | `fractional\|base_1_5\|fractional\|base_1_5` | `raise:TypeError` | `raise:NoMethodError` |
| `python.&` | `ruby.^` | `fractional\|base_1_5\|fractional\|base_1_5` | `raise:TypeError` | `raise:NoMethodError` |

## shift

21 leaves, 21 of them maximal. Compatible pairs: 1 agreeing,
0 vacuous. Blocked pairs: 209.

The agreeing pairs, cross-language first.

| left | right | shared elements | union elements | |
|---|---|---|---|---|
| `java.>>` | `java.>>>` | 16 | 16 | same language |

The widest assembly of two or more: 2 maximal leaves covering
16 of 1156 elements, on 1 agreeing and 0 vacuous edges.

```
  java.>>  java.>>>
```

The blocked unions, with one blocking element quoted each.

| left | right | blocking element | left answers | right answers |
|---|---|---|---|---|
| `php.<<` | `python.<<` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:2` | `raise:TypeError` |
| `php.<<` | `python.>>` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:2` | `raise:TypeError` |
| `php.<<` | `ruby.<<` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:2` | `raise:NoMethodError` |
| `php.<<` | `ruby.>>` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:2` | `raise:NoMethodError` |
| `php.>>` | `python.<<` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `raise:TypeError` |
| `php.>>` | `python.>>` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `raise:TypeError` |
| `php.>>` | `ruby.<<` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `raise:NoMethodError` |
| `php.>>` | `ruby.>>` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `raise:NoMethodError` |
| `python.<<` | `ruby.<<` | `fractional\|base_1_5\|fractional\|base_1_5` | `raise:TypeError` | `raise:NoMethodError` |
| `python.<<` | `ruby.>>` | `fractional\|base_1_5\|fractional\|base_1_5` | `raise:TypeError` | `raise:NoMethodError` |
| `python.>>` | `ruby.<<` | `fractional\|base_1_5\|fractional\|base_1_5` | `raise:TypeError` | `raise:NoMethodError` |
| `python.>>` | `ruby.>>` | `fractional\|base_1_5\|fractional\|base_1_5` | `raise:TypeError` | `raise:NoMethodError` |
| `php.<<` | `typescript.<<` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:2` | `fractional:2.0` |
| `php.<<` | `typescript.>>` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:2` | `fractional:0.0` |
| `php.>>` | `typescript.<<` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `fractional:2.0` |
| `php.>>` | `typescript.>>` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:0` | `fractional:0.0` |
| `python.<<` | `typescript.<<` | `fractional\|base_1_5\|fractional\|base_1_5` | `raise:TypeError` | `fractional:2.0` |
| `python.<<` | `typescript.>>` | `fractional\|base_1_5\|fractional\|base_1_5` | `raise:TypeError` | `fractional:0.0` |
| `python.>>` | `typescript.<<` | `fractional\|base_1_5\|fractional\|base_1_5` | `raise:TypeError` | `fractional:2.0` |
| `python.>>` | `typescript.>>` | `fractional\|base_1_5\|fractional\|base_1_5` | `raise:TypeError` | `fractional:0.0` |

## other

6 leaves, 6 of them maximal. Compatible pairs: 0 agreeing,
0 vacuous. Blocked pairs: 15.

**No agreeing pair at all.** Every pair of maximal leaves in
this family either contradicts the other somewhere or shares no
element with it.

**No assembly of two or more exists here.** Every pair of maximal
leaves in this family blocks, so nothing can be laid on top of
anything else.

The blocked unions, with one blocking element quoted each.

| left | right | blocking element | left answers | right answers |
|---|---|---|---|---|
| `php..` | `python.not in` | `fractional\|base_1_5\|fractional\|base_1_5` | `text:312e35312e35` | `raise:TypeError` |
| `php..` | `ruby.=~` | `fractional\|base_1_5\|fractional\|base_1_5` | `text:312e35312e35` | `raise:NoMethodError` |
| `python.not in` | `ruby.=~` | `fractional\|base_1_5\|fractional\|base_1_5` | `raise:TypeError` | `raise:NoMethodError` |
| `dart.~/` | `php..` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `text:312e35312e35` |
| `dart.~/` | `python.not in` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `raise:TypeError` |
| `dart.~/` | `ruby.=~` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `raise:NoMethodError` |
| `php..` | `rust...` | `fractional\|base_1_5\|fractional\|base_1_5` | `text:312e35312e35` | `range:[fractional:1.5,fractional:1.5,excl]` |
| `python.not in` | `rust...` | `fractional\|base_1_5\|fractional\|base_1_5` | `raise:TypeError` | `range:[fractional:1.5,fractional:1.5,excl]` |
| `ruby.=~` | `rust...` | `fractional\|base_1_5\|fractional\|base_1_5` | `raise:NoMethodError` | `range:[fractional:1.5,fractional:1.5,excl]` |
| `kotlin...` | `php..` | `fractional\|base_1_5\|fractional\|base_1_5` | `opaque:1.5..1.5` | `text:312e35312e35` |
| `kotlin...` | `python.not in` | `fractional\|base_1_5\|fractional\|base_1_5` | `opaque:1.5..1.5` | `raise:TypeError` |
| `kotlin...` | `ruby.=~` | `fractional\|base_1_5\|fractional\|base_1_5` | `opaque:1.5..1.5` | `raise:NoMethodError` |
| `kotlin...` | `rust...` | `fractional\|base_1_5\|fractional\|base_1_5` | `opaque:1.5..1.5` | `range:[fractional:1.5,fractional:1.5,excl]` |
| `dart.~/` | `rust...` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `range:[fractional:1.5,fractional:1.5,excl]` |
| `dart.~/` | `kotlin...` | `fractional\|base_1_5\|fractional\|base_1_5` | `whole:1` | `opaque:1.5..1.5` |

