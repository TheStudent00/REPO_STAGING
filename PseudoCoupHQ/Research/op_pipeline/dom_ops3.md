# dom_ops -- the dominant operators

- rule: THE DOM_OP CONSTRUCTION RULE (the owner, 2026-08-26): dominant operators are DISCOVERED from machine evidence by matching, never asserted
- node: a node is the PROVENANCE of a probe -- which grammar rule of ONE language generated it: language, grammar operator, arity bucket.  Arity is part of identity because one token can be two operators.
- candidate set: machine-form evidence only: two nodes are compared when they have units in the same equivalence class of dominant_table3.  No operator token takes part in any key, grouping, pairing or selection here.
- spelling: the operator token appears exactly once per node, as the display label `label` on a member that also carries its language and its id
- edge weights: primary: the number of equivalence classes in which the two nodes both have member units.  secondary: the number of distinct operand-type keys those classes carry, so a coincidence on bool alone scores 1.
- mutual filter: each node keeps its strongest counterpart per foreign language (classes, then type keys, then the smaller class count); the edge survives only when both endpoints chose each other
- intention: `intention` is null on every row by instruction; the hint field is proposed only.  the owner settles.

nodes 143, edges 248 before the mutual filter, 210 after, dom_ops 28

without the arity fix, the same construction gives nodes 124, edges 228 before the filter, 171 after, components 25.

the same-language assertion ran over 28 components; 17 collisions found.

the brief said a component cannot hold two nodes of one language BY CONSTRUCTION.  It can, and the assertion found it.  A node keeps one counterpart per foreign language, but a component is a CHAIN, and a chain can walk back into a language it already visited.  Nothing is merged and nothing is dropped here; the collision is recorded on the row and the owner settles the rule.

## D0001 -- 9 members over c, c, c, c, cpp, cpp, cpp, go, swift

| language | label | arity |
| --- | --- | --- |
| c | `+` | unary_prefix |
| c | `++` | unary_postfix |
| c | `--` | unary_postfix |
| c | `__extension__` | unary_prefix |
| cpp | `+` | unary_prefix |
| cpp | `++` | unary_postfix |
| cpp | `--` | unary_postfix |
| go | `+` | unary_prefix |
| swift | `+` | unary_prefix |

- classes spanned (7): K0001, K0002, K0003, K0004, K0005, K0067, K0249
- classes any member touches: 10
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: canon-byte
- surviving edges: 20
  - N0009--N0041: 6 shared classes, 6 shared operand-type keys
  - N0009--N0079: 2 shared classes, 2 shared operand-type keys
  - N0009--N0126: 5 shared classes, 5 shared operand-type keys
  - N0010--N0042: 5 shared classes, 5 shared operand-type keys
  - N0010--N0046: 5 shared classes, 5 shared operand-type keys
  - N0010--N0079: 2 shared classes, 2 shared operand-type keys
  - N0010--N0126: 5 shared classes, 5 shared operand-type keys
  - N0014--N0042: 5 shared classes, 5 shared operand-type keys
  - N0014--N0046: 5 shared classes, 5 shared operand-type keys
  - N0014--N0079: 2 shared classes, 2 shared operand-type keys
  - N0014--N0126: 5 shared classes, 5 shared operand-type keys
  - N0028--N0042: 5 shared classes, 5 shared operand-type keys
  - N0028--N0046: 5 shared classes, 5 shared operand-type keys
  - N0028--N0079: 2 shared classes, 2 shared operand-type keys
  - N0028--N0126: 5 shared classes, 5 shared operand-type keys
  - N0042--N0079: 2 shared classes, 2 shared operand-type keys
  - N0042--N0126: 5 shared classes, 5 shared operand-type keys
  - N0046--N0079: 2 shared classes, 2 shared operand-type keys
  - N0046--N0126: 5 shared classes, 5 shared operand-type keys
  - N0079--N0126: 2 shared classes, 2 shared operand-type keys
- bridges: 1
  - K0249 dominates K0067 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c,cpp, dominated c
- fences: 0
- languages absent:
  - rust: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0009--N0010 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0009--N0014 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0009--N0028 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0009--N0041 | 6 | byte | byte |
| N0009--N0042 | 5 | byte | byte |
| N0009--N0046 | 5 | byte | byte |
| N0009--N0079 | 2 | byte | byte |
| N0009--N0126 | 5 | byte | byte |
| N0010--N0014 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0010--N0028 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0010--N0041 | 5 | byte | byte |
| N0010--N0042 | 5 | byte | byte |
| N0010--N0046 | 5 | byte | byte |
| N0010--N0079 | 2 | byte | byte |
| N0010--N0126 | 5 | byte | byte |
| N0014--N0028 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0014--N0041 | 5 | byte | byte |
| N0014--N0042 | 5 | byte | byte |
| N0014--N0046 | 5 | byte | byte |
| N0014--N0079 | 2 | byte | byte |
| N0014--N0126 | 5 | byte | byte |
| N0028--N0041 | 5 | byte | byte |
| N0028--N0042 | 5 | byte | byte |
| N0028--N0046 | 5 | byte | byte |
| N0028--N0079 | 2 | byte | byte |
| N0028--N0126 | 5 | byte | byte |
| N0041--N0042 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0041--N0046 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0041--N0079 | 2 | byte | byte |
| N0041--N0126 | 5 | byte | byte |
| N0042--N0046 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0042--N0079 | 2 | byte | byte |
| N0042--N0126 | 5 | byte | byte |
| N0046--N0079 | 2 | byte | byte |
| N0046--N0126 | 5 | byte | byte |
| N0079--N0126 | 2 | byte | byte |

## D0002 -- 6 members over c, cpp, cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| c | `&` | binary |
| cpp | `&` | binary |
| cpp | `bitand` | binary |
| go | `&` | binary |
| rust | `&` | binary |
| swift | `&` | binary |

- classes spanned (16): K0006, K0010, K0011, K0012, K0093, K0094, K0095, K0096, K0097, K0098, K0099, K0100, K0101, K0102, K0103, K0104
- classes any member touches: 17
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 14
  - N0004--N0036: 16 shared classes, 16 shared operand-type keys
  - N0004--N0059: 16 shared classes, 16 shared operand-type keys
  - N0004--N0073: 3 shared classes, 3 shared operand-type keys
  - N0004--N0098: 3 shared classes, 3 shared operand-type keys
  - N0004--N0122: 3 shared classes, 3 shared operand-type keys
  - N0036--N0073: 3 shared classes, 3 shared operand-type keys
  - N0036--N0098: 3 shared classes, 3 shared operand-type keys
  - N0036--N0122: 3 shared classes, 3 shared operand-type keys
  - N0059--N0073: 3 shared classes, 3 shared operand-type keys
  - N0059--N0098: 3 shared classes, 3 shared operand-type keys
  - N0059--N0122: 3 shared classes, 3 shared operand-type keys
  - N0073--N0098: 3 shared classes, 3 shared operand-type keys
  - N0073--N0122: 3 shared classes, 3 shared operand-type keys
  - N0098--N0122: 3 shared classes, 3 shared operand-type keys
- bridges: 1
  - K0006 dominates K0019 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c,cpp, dominated cpp,go,rust,swift
- fences: 0
- languages absent:
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0004--N0036 | 16 | byte | byte |
| N0004--N0059 | 16 | byte | byte |
| N0004--N0073 | 3 | sem | sem |
| N0004--N0098 | 3 | byte | byte |
| N0004--N0122 | 3 | byte | byte |
| N0036--N0059 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0036--N0073 | 3 | sem | sem |
| N0036--N0098 | 3 | byte | byte |
| N0036--N0122 | 3 | byte | byte |
| N0059--N0073 | 3 | sem | sem |
| N0059--N0098 | 3 | byte | byte |
| N0059--N0122 | 3 | byte | byte |
| N0073--N0098 | 3 | sem | sem |
| N0073--N0122 | 3 | sem | sem |
| N0098--N0122 | 3 | byte | byte |

## D0003 -- 6 members over c, cpp, go, java, rust, swift

| language | label | arity |
| --- | --- | --- |
| c | `+` | binary |
| cpp | `+` | binary |
| go | `+` | binary |
| java | `+` | binary |
| rust | `+` | binary |
| swift | `+` | binary |

- classes spanned (36): K0031, K0032, K0043, K0044, K0045, K0136, K0137, K0138, K0139, K0140, K0141, K0142, K0143, K0144, K0145, K0146, K0147, K0148, K0149, K0150, K0151, K0152, K0153, K0154, K0155, K0156, K0157, K0158, K0159, K0160, K0161, K0162, K0163, K0164, K0165, K0166
- classes any member touches: 39
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 14
  - N0008--N0040: 36 shared classes, 36 shared operand-type keys
  - N0008--N0078: 5 shared classes, 5 shared operand-type keys
  - N0008--N0094: 1 shared classes, 1 shared operand-type keys
  - N0008--N0101: 5 shared classes, 5 shared operand-type keys
  - N0008--N0125: 2 shared classes, 2 shared operand-type keys
  - N0040--N0078: 5 shared classes, 5 shared operand-type keys
  - N0040--N0094: 1 shared classes, 1 shared operand-type keys
  - N0040--N0101: 5 shared classes, 5 shared operand-type keys
  - N0040--N0125: 2 shared classes, 2 shared operand-type keys
  - N0078--N0094: 1 shared classes, 1 shared operand-type keys
  - N0078--N0101: 5 shared classes, 5 shared operand-type keys
  - N0078--N0125: 2 shared classes, 2 shared operand-type keys
  - N0094--N0101: 1 shared classes, 1 shared operand-type keys
  - N0101--N0125: 2 shared classes, 2 shared operand-type keys
- bridges: 0
- fences: 15
  - in0 + in1 carries out of 64 bits (unsigned) -> None x5
  - in0 + in1 overflows 32 bits (signed) -> None x5
  - in0 + in1 overflows 64 bits (signed) -> None x5
- languages absent:
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0008--N0040 | 36 | byte | byte |
| N0008--N0078 | 5 | byte | sem |
| N0008--N0094 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0008--N0101 | 5 | byte | byte |
| N0008--N0125 | 2 | byte | byte |
| N0040--N0078 | 5 | byte | sem |
| N0040--N0094 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0040--N0101 | 5 | byte | byte |
| N0040--N0125 | 2 | byte | byte |
| N0078--N0094 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0078--N0101 | 5 | byte | sem |
| N0078--N0125 | 2 | byte | byte |
| N0094--N0101 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0094--N0125 | 0 | -- | -- |
| N0101--N0125 | 2 | byte | byte |

## D0004 -- 6 members over c, cpp, cpp, cpp, go, swift

| language | label | arity |
| --- | --- | --- |
| c | `--` | unary_prefix |
| cpp | `!` | unary_prefix |
| cpp | `--` | unary_prefix |
| cpp | `not` | unary_prefix |
| go | `!` | unary_prefix |
| swift | `!` | unary_prefix |

- classes spanned (11): K0035, K0037, K0038, K0258, K0268, K0291, K0292, K0293, K0670, K0672, K0673
- classes any member touches: 11
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 8
  - N0015--N0047: 5 shared classes, 5 shared operand-type keys
  - N0015--N0070: 1 shared classes, 1 shared operand-type keys
  - N0015--N0119: 1 shared classes, 1 shared operand-type keys
  - N0033--N0070: 1 shared classes, 1 shared operand-type keys
  - N0033--N0119: 1 shared classes, 1 shared operand-type keys
  - N0062--N0070: 1 shared classes, 1 shared operand-type keys
  - N0062--N0119: 1 shared classes, 1 shared operand-type keys
  - N0070--N0119: 1 shared classes, 1 shared operand-type keys
- bridges: 9
  - K0491 dominates K0035 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated c,cpp,rust,swift
  - K0377 dominates K0258 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0378 dominates K0268 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0379 dominates K0670 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0379 dominates K0670 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0398 dominates K0672 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0398 dominates K0672 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0451 dominates K0673 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0451 dominates K0673 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
- fences: 3
  - in0 >= 64 (unsigned) -> None x3
- languages absent:
  - rust: no mutual counterpart: the language has units in these classes, but no node of it was chosen back
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0015--N0033 | 1 | byte | byte |
| N0015--N0047 | 5 | byte | byte |
| N0015--N0062 | 1 | byte | byte |
| N0015--N0070 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0015--N0119 | 1 | byte | byte |
| N0033--N0047 | 0 | -- | -- |
| N0033--N0062 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0033--N0070 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0033--N0119 | 1 | byte | byte |
| N0047--N0062 | 0 | -- | -- |
| N0047--N0070 | 0 | -- | -- |
| N0047--N0119 | 0 | -- | -- |
| N0062--N0070 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0062--N0119 | 1 | byte | byte |
| N0070--N0119 | 1 | not-recorded-per-pair | not-recorded-per-pair |

## D0005 -- 6 members over c, cpp, cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| c | `^` | binary |
| cpp | `^` | binary |
| cpp | `xor` | binary |
| go | `^` | binary |
| rust | `^` | binary |
| swift | `^` | binary |

- classes spanned (16): K0016, K0017, K0018, K0040, K0081, K0082, K0083, K0084, K0085, K0086, K0087, K0088, K0089, K0090, K0091, K0092
- classes any member touches: 17
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 14
  - N0024--N0057: 16 shared classes, 16 shared operand-type keys
  - N0024--N0066: 16 shared classes, 16 shared operand-type keys
  - N0024--N0090: 3 shared classes, 3 shared operand-type keys
  - N0024--N0116: 3 shared classes, 3 shared operand-type keys
  - N0024--N0140: 3 shared classes, 3 shared operand-type keys
  - N0057--N0090: 3 shared classes, 3 shared operand-type keys
  - N0057--N0116: 3 shared classes, 3 shared operand-type keys
  - N0057--N0140: 3 shared classes, 3 shared operand-type keys
  - N0066--N0090: 3 shared classes, 3 shared operand-type keys
  - N0066--N0116: 3 shared classes, 3 shared operand-type keys
  - N0066--N0140: 3 shared classes, 3 shared operand-type keys
  - N0090--N0116: 3 shared classes, 3 shared operand-type keys
  - N0090--N0140: 3 shared classes, 3 shared operand-type keys
  - N0116--N0140: 3 shared classes, 3 shared operand-type keys
- bridges: 1
  - K0040 dominates K0036 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c,cpp, dominated cpp,rust,swift
- fences: 0
- languages absent:
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0024--N0057 | 16 | byte | byte |
| N0024--N0066 | 16 | byte | byte |
| N0024--N0090 | 3 | sem | sem |
| N0024--N0116 | 3 | byte | byte |
| N0024--N0140 | 3 | byte | byte |
| N0057--N0066 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0057--N0090 | 3 | sem | sem |
| N0057--N0116 | 3 | byte | byte |
| N0057--N0140 | 3 | byte | byte |
| N0066--N0090 | 3 | sem | sem |
| N0066--N0116 | 3 | byte | byte |
| N0066--N0140 | 3 | byte | byte |
| N0090--N0116 | 3 | sem | sem |
| N0090--N0140 | 3 | sem | sem |
| N0116--N0140 | 3 | byte | byte |

## D0006 -- 6 members over c, cpp, cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| c | `\|` | binary |
| cpp | `bitor` | binary |
| cpp | `\|` | binary |
| go | `\|` | binary |
| rust | `\|` | binary |
| swift | `\|` | binary |

- classes spanned (16): K0013, K0014, K0015, K0039, K0069, K0070, K0071, K0072, K0073, K0074, K0075, K0076, K0077, K0078, K0079, K0080
- classes any member touches: 17
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 14
  - N0030--N0060: 16 shared classes, 16 shared operand-type keys
  - N0030--N0067: 16 shared classes, 16 shared operand-type keys
  - N0030--N0092: 3 shared classes, 3 shared operand-type keys
  - N0030--N0117: 3 shared classes, 3 shared operand-type keys
  - N0030--N0141: 3 shared classes, 3 shared operand-type keys
  - N0060--N0092: 3 shared classes, 3 shared operand-type keys
  - N0060--N0117: 3 shared classes, 3 shared operand-type keys
  - N0060--N0141: 3 shared classes, 3 shared operand-type keys
  - N0067--N0092: 3 shared classes, 3 shared operand-type keys
  - N0067--N0117: 3 shared classes, 3 shared operand-type keys
  - N0067--N0141: 3 shared classes, 3 shared operand-type keys
  - N0092--N0117: 3 shared classes, 3 shared operand-type keys
  - N0092--N0141: 3 shared classes, 3 shared operand-type keys
  - N0117--N0141: 3 shared classes, 3 shared operand-type keys
- bridges: 1
  - K0039 dominates K0020 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c,cpp, dominated cpp,go,rust,swift
- fences: 0
- languages absent:
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0030--N0060 | 16 | byte | byte |
| N0030--N0067 | 16 | byte | byte |
| N0030--N0092 | 3 | sem | sem |
| N0030--N0117 | 3 | byte | byte |
| N0030--N0141 | 3 | byte | byte |
| N0060--N0067 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0060--N0092 | 3 | sem | sem |
| N0060--N0117 | 3 | byte | byte |
| N0060--N0141 | 3 | byte | byte |
| N0067--N0092 | 3 | sem | sem |
| N0067--N0117 | 3 | byte | byte |
| N0067--N0141 | 3 | byte | byte |
| N0092--N0117 | 3 | sem | sem |
| N0092--N0141 | 3 | sem | sem |
| N0117--N0141 | 3 | byte | byte |

## D0007 -- 6 members over c, cpp, cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| c | `~` | unary_prefix |
| cpp | `compl` | unary_prefix |
| cpp | `~` | unary_prefix |
| go | `^` | unary_prefix |
| rust | `!` | unary_prefix |
| swift | `~` | unary_prefix |

- classes spanned (4): K0007, K0008, K0009, K0068
- classes any member touches: 5
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 14
  - N0032--N0061: 4 shared classes, 4 shared operand-type keys
  - N0032--N0069: 4 shared classes, 4 shared operand-type keys
  - N0032--N0091: 3 shared classes, 3 shared operand-type keys
  - N0032--N0095: 3 shared classes, 3 shared operand-type keys
  - N0032--N0143: 3 shared classes, 3 shared operand-type keys
  - N0061--N0091: 3 shared classes, 3 shared operand-type keys
  - N0061--N0095: 3 shared classes, 3 shared operand-type keys
  - N0061--N0143: 3 shared classes, 3 shared operand-type keys
  - N0069--N0091: 3 shared classes, 3 shared operand-type keys
  - N0069--N0095: 3 shared classes, 3 shared operand-type keys
  - N0069--N0143: 3 shared classes, 3 shared operand-type keys
  - N0091--N0095: 3 shared classes, 3 shared operand-type keys
  - N0091--N0143: 3 shared classes, 3 shared operand-type keys
  - N0095--N0143: 3 shared classes, 3 shared operand-type keys
- bridges: 0
- fences: 1
  - in0 >= 64 (unsigned) -> None x1
- languages absent:
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0032--N0061 | 4 | byte | byte |
| N0032--N0069 | 4 | byte | byte |
| N0032--N0091 | 3 | sem | sem |
| N0032--N0095 | 3 | byte | byte |
| N0032--N0143 | 3 | byte | byte |
| N0061--N0069 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0061--N0091 | 3 | sem | sem |
| N0061--N0095 | 3 | byte | byte |
| N0061--N0143 | 3 | byte | byte |
| N0069--N0091 | 3 | sem | sem |
| N0069--N0095 | 3 | byte | byte |
| N0069--N0143 | 3 | byte | byte |
| N0091--N0095 | 3 | sem | sem |
| N0091--N0143 | 3 | sem | sem |
| N0095--N0143 | 3 | byte | byte |

## D0008 -- 5 members over c, cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| c | `*` | binary |
| cpp | `*` | binary |
| go | `*` | binary |
| rust | `*` | binary |
| swift | `*` | binary |

- classes spanned (36): K0006, K0027, K0028, K0049, K0050, K0051, K0199, K0200, K0201, K0202, K0203, K0204, K0205, K0206, K0207, K0208, K0209, K0210, K0211, K0212, K0213, K0214, K0215, K0216, K0217, K0218, K0219, K0220, K0221, K0222, K0223, K0224, K0225, K0226, K0227, K0228
- classes any member touches: 39
- strongest evidence over the member pairs: byte
- weakest over the member pairs: anchored sem identity (the two lifted forms are identical)
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 10
  - N0007--N0039: 36 shared classes, 36 shared operand-type keys
  - N0007--N0077: 5 shared classes, 5 shared operand-type keys
  - N0007--N0100: 5 shared classes, 5 shared operand-type keys
  - N0007--N0124: 2 shared classes, 2 shared operand-type keys
  - N0039--N0077: 5 shared classes, 5 shared operand-type keys
  - N0039--N0100: 5 shared classes, 5 shared operand-type keys
  - N0039--N0124: 2 shared classes, 2 shared operand-type keys
  - N0077--N0100: 5 shared classes, 5 shared operand-type keys
  - N0077--N0124: 2 shared classes, 2 shared operand-type keys
  - N0100--N0124: 2 shared classes, 2 shared operand-type keys
- bridges: 1
  - K0006 dominates K0019 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c,cpp, dominated cpp,go,rust,swift
- fences: 11
  - in0 * in1 overflows 64 bits (signed) -> None x1
  - in1 * in0 overflows 32 bits (signed) -> None x5
  - in1 * in0 overflows 64 bits (signed) -> None x5
- languages absent:
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0007--N0039 | 36 | byte | byte |
| N0007--N0077 | 5 | byte | sem |
| N0007--N0100 | 5 | byte | byte |
| N0007--N0124 | 2 | byte | byte |
| N0039--N0077 | 5 | byte | sem |
| N0039--N0100 | 5 | byte | byte |
| N0039--N0124 | 2 | byte | byte |
| N0077--N0100 | 5 | byte | sem |
| N0077--N0124 | 2 | byte | byte |
| N0100--N0124 | 2 | byte | byte |

## D0009 -- 5 members over c, cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| c | `-` | binary |
| cpp | `-` | binary |
| go | `-` | binary |
| rust | `-` | binary |
| swift | `-` | binary |

- classes spanned (36): K0033, K0034, K0046, K0047, K0048, K0167, K0168, K0169, K0170, K0171, K0172, K0173, K0174, K0175, K0176, K0177, K0178, K0179, K0180, K0181, K0182, K0183, K0184, K0185, K0186, K0187, K0188, K0189, K0190, K0191, K0192, K0193, K0195, K0196, K0197, K0198
- classes any member touches: 39
- strongest evidence over the member pairs: byte
- weakest over the member pairs: anchored sem identity (the two lifted forms are identical)
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 10
  - N0012--N0044: 36 shared classes, 36 shared operand-type keys
  - N0012--N0080: 5 shared classes, 5 shared operand-type keys
  - N0012--N0102: 5 shared classes, 5 shared operand-type keys
  - N0012--N0127: 2 shared classes, 2 shared operand-type keys
  - N0044--N0080: 5 shared classes, 5 shared operand-type keys
  - N0044--N0102: 5 shared classes, 5 shared operand-type keys
  - N0044--N0127: 2 shared classes, 2 shared operand-type keys
  - N0080--N0102: 5 shared classes, 5 shared operand-type keys
  - N0080--N0127: 2 shared classes, 2 shared operand-type keys
  - N0102--N0127: 2 shared classes, 2 shared operand-type keys
- bridges: 0
- fences: 11
  - in0 - in1 overflows 32 bits (signed) -> None x5
  - in0 - in1 overflows 64 bits (signed) -> None x5
  - in0 < in1 (unsigned) -> None x1
- languages absent:
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0012--N0044 | 36 | byte | byte |
| N0012--N0080 | 5 | byte | sem |
| N0012--N0102 | 5 | byte | byte |
| N0012--N0127 | 2 | byte | byte |
| N0044--N0080 | 5 | byte | sem |
| N0044--N0102 | 5 | byte | byte |
| N0044--N0127 | 2 | byte | byte |
| N0080--N0102 | 5 | byte | sem |
| N0080--N0127 | 2 | byte | byte |
| N0102--N0127 | 2 | byte | byte |

## D0010 -- 5 members over c, cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| c | `-` | unary_prefix |
| cpp | `-` | unary_prefix |
| go | `-` | unary_prefix |
| rust | `-` | unary_prefix |
| swift | `-` | unary_prefix |

- classes spanned (6): K0041, K0042, K0052, K0053, K0105, K0194
- classes any member touches: 10
- strongest evidence over the member pairs: byte
- weakest over the member pairs: anchored sem identity (the two lifted forms are identical)
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 9
  - N0013--N0045: 6 shared classes, 6 shared operand-type keys
  - N0013--N0081: 3 shared classes, 3 shared operand-type keys
  - N0013--N0103: 4 shared classes, 4 shared operand-type keys
  - N0013--N0128: 2 shared classes, 2 shared operand-type keys
  - N0045--N0081: 3 shared classes, 3 shared operand-type keys
  - N0045--N0103: 4 shared classes, 4 shared operand-type keys
  - N0045--N0128: 2 shared classes, 2 shared operand-type keys
  - N0081--N0103: 2 shared classes, 2 shared operand-type keys
  - N0103--N0128: 2 shared classes, 2 shared operand-type keys
- bridges: 0
- fences: 10
  - 0 - in0 overflows 32 bits (signed) -> None x5
  - 0 - in0 overflows 64 bits (signed) -> None x5
- languages absent:
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0013--N0045 | 6 | byte | byte |
| N0013--N0081 | 3 | sem | sem |
| N0013--N0103 | 4 | byte | byte |
| N0013--N0128 | 2 | byte | byte |
| N0045--N0081 | 3 | sem | sem |
| N0045--N0103 | 4 | byte | byte |
| N0045--N0128 | 2 | byte | byte |
| N0081--N0103 | 2 | sem | sem |
| N0081--N0128 | 0 | -- | -- |
| N0103--N0128 | 2 | byte | byte |

## D0011 -- 5 members over c, cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| c | `/` | binary |
| cpp | `/` | binary |
| go | `/` | binary |
| rust | `/` | binary |
| swift | `/` | binary |

- classes spanned (37): K0029, K0030, K0229, K0230, K0231, K0232, K0233, K0234, K0235, K0236, K0237, K0238, K0239, K0240, K0241, K0242, K0243, K0244, K0245, K0246, K0247, K0248, K0250, K0251, K0252, K0253, K0254, K0255, K0256, K0257, K0259, K0260, K0261, K0262, K0263, K0264, K0367
- classes any member touches: 44
- strongest evidence over the member pairs: byte
- weakest over the member pairs: core-text identity: verdicts4's own column found the two normal-path cores textually equal
- weakest the class table itself recorded on the spanned classes: core-text
- surviving edges: 10
  - N0016--N0048: 36 shared classes, 36 shared operand-type keys
  - N0016--N0082: 2 shared classes, 2 shared operand-type keys
  - N0016--N0108: 2 shared classes, 2 shared operand-type keys
  - N0016--N0131: 2 shared classes, 2 shared operand-type keys
  - N0048--N0082: 2 shared classes, 2 shared operand-type keys
  - N0048--N0108: 2 shared classes, 2 shared operand-type keys
  - N0048--N0131: 2 shared classes, 2 shared operand-type keys
  - N0082--N0108: 3 shared classes, 3 shared operand-type keys
  - N0082--N0131: 2 shared classes, 2 shared operand-type keys
  - N0108--N0131: 2 shared classes, 2 shared operand-type keys
- bridges: 1
  - K0264 dominates K1103 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c,cpp, dominated swift
- fences: 13
  - ((-2147483648 + in0) | ~in1) == 0 -> None x1
  - (~in1 | (-9223372036854775808 ^ in0)) == 0 -> None x1
  - in1 == -1 -> None x2
  - in1 == 0 -> None x9
- languages absent:
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0016--N0048 | 36 | byte | byte |
| N0016--N0082 | 2 | byte | byte |
| N0016--N0108 | 2 | byte | byte |
| N0016--N0131 | 2 | byte | byte |
| N0048--N0082 | 2 | byte | byte |
| N0048--N0108 | 2 | byte | byte |
| N0048--N0131 | 2 | byte | byte |
| N0082--N0108 | 3 | byte | core-text |
| N0082--N0131 | 2 | byte | byte |
| N0108--N0131 | 2 | byte | byte |

## D0012 -- 5 members over c, c, c, c, cpp

| language | label | arity |
| --- | --- | --- |
| c | `_Alignof` | unary_prefix |
| c | `__alignof` | unary_prefix |
| c | `__alignof__` | unary_prefix |
| c | `sizeof` | unary_prefix |
| cpp | `sizeof` | unary_prefix |

- classes spanned (6): K0021, K0022, K0023, K0024, K0025, K0026
- classes any member touches: 6
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: canon-byte
- surviving edges: 4
  - N0025--N0065: 6 shared classes, 6 shared operand-type keys
  - N0026--N0065: 6 shared classes, 6 shared operand-type keys
  - N0027--N0065: 6 shared classes, 6 shared operand-type keys
  - N0029--N0065: 6 shared classes, 6 shared operand-type keys
- bridges: 0
- fences: 0
- languages absent:
  - go: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - rust: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - swift: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0025--N0026 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0025--N0027 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0025--N0029 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0025--N0065 | 6 | byte | byte |
| N0026--N0027 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0026--N0029 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0026--N0065 | 6 | byte | byte |
| N0027--N0029 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0027--N0065 | 6 | byte | byte |
| N0029--N0065 | 6 | byte | byte |

## D0013 -- 5 members over cpp, cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| cpp | `!=` | binary |
| cpp | `not_eq` | binary |
| go | `!=` | binary |
| rust | `!=` | binary |
| swift | `!=` | binary |

- classes spanned (36): K0036, K0062, K0063, K0064, K0065, K0066, K0352, K0353, K0354, K0355, K0356, K0669, K0732, K0733, K0734, K0735, K0736, K0737, K0738, K0739, K0740, K0741, K0742, K0743, K0744, K0745, K0746, K0747, K0748, K0749, K0750, K0751, K0752, K0753, K0754, K0755
- classes any member touches: 42
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 9
  - N0034--N0071: 4 shared classes, 4 shared operand-type keys
  - N0034--N0096: 6 shared classes, 6 shared operand-type keys
  - N0034--N0120: 8 shared classes, 8 shared operand-type keys
  - N0063--N0071: 4 shared classes, 4 shared operand-type keys
  - N0063--N0096: 6 shared classes, 6 shared operand-type keys
  - N0063--N0120: 8 shared classes, 8 shared operand-type keys
  - N0071--N0096: 4 shared classes, 4 shared operand-type keys
  - N0071--N0120: 4 shared classes, 4 shared operand-type keys
  - N0096--N0120: 6 shared classes, 6 shared operand-type keys
- bridges: 53
  - K0040 dominates K0036 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c,cpp, dominated cpp,rust,swift
  - K0489 dominates K0062 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0497 dominates K0063 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0504 dominates K0064 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0511 dominates K0065 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0518 dominates K0066 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0490 dominates K0352 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0496 dominates K0353 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0501 dominates K0354 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0520 dominates K0355 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0521 dominates K0356 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0492 dominates K0732 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - (and 41 more)
- fences: 26
  - in0 >= 64 (unsigned) -> None x18
  - in1 >= 64 (unsigned) -> None x8
- languages absent:
  - c: attached by bridge only: a directional bridge reaches these classes, membership does not
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0034--N0063 | 36 | not-recorded-per-pair | not-recorded-per-pair |
| N0034--N0071 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0034--N0096 | 6 | byte | byte |
| N0034--N0120 | 8 | byte | not-recorded-per-pair |
| N0063--N0071 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0063--N0096 | 6 | byte | byte |
| N0063--N0120 | 8 | byte | not-recorded-per-pair |
| N0071--N0096 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0071--N0120 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0096--N0120 | 6 | byte | byte |

## D0014 -- 5 members over cpp, cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| cpp | `&&` | binary |
| cpp | `and` | binary |
| go | `&&` | binary |
| rust | `&&` | binary |
| swift | `&&` | binary |

- classes spanned (36): K0019, K0330, K0331, K0332, K0333, K0334, K0335, K0336, K0337, K0338, K0339, K0340, K0341, K0342, K0343, K0344, K0345, K0346, K0347, K0348, K0349, K0350, K0351, K0688, K0689, K0690, K0691, K0692, K0693, K0694, K0695, K0696, K0697, K0698, K0699, K0700
- classes any member touches: 36
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 9
  - N0038--N0075: 1 shared classes, 1 shared operand-type keys
  - N0038--N0099: 1 shared classes, 1 shared operand-type keys
  - N0038--N0123: 1 shared classes, 1 shared operand-type keys
  - N0058--N0075: 1 shared classes, 1 shared operand-type keys
  - N0058--N0099: 1 shared classes, 1 shared operand-type keys
  - N0058--N0123: 1 shared classes, 1 shared operand-type keys
  - N0075--N0099: 1 shared classes, 1 shared operand-type keys
  - N0075--N0123: 1 shared classes, 1 shared operand-type keys
  - N0099--N0123: 1 shared classes, 1 shared operand-type keys
- bridges: 49
  - K0006 dominates K0019 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c,cpp, dominated cpp,go,rust,swift
  - K0416 dominates K0330 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0417 dominates K0331 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0419 dominates K0332 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0420 dominates K0333 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0421 dominates K0334 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0422 dominates K0335 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0423 dominates K0336 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0425 dominates K0337 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0426 dominates K0338 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0427 dominates K0339 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0434 dominates K0340 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - (and 37 more)
- fences: 0
- languages absent:
  - c: attached by bridge only: a directional bridge reaches these classes, membership does not
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0038--N0058 | 36 | not-recorded-per-pair | not-recorded-per-pair |
| N0038--N0075 | 1 | sem | sem |
| N0038--N0099 | 1 | byte | byte |
| N0038--N0123 | 1 | byte | byte |
| N0058--N0075 | 1 | sem | sem |
| N0058--N0099 | 1 | byte | byte |
| N0058--N0123 | 1 | byte | byte |
| N0075--N0099 | 1 | sem | sem |
| N0075--N0123 | 1 | sem | sem |
| N0099--N0123 | 1 | byte | byte |

## D0015 -- 5 members over cpp, cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| cpp | `or` | binary |
| cpp | `\|\|` | binary |
| go | `\|\|` | binary |
| rust | `\|\|` | binary |
| swift | `\|\|` | binary |

- classes spanned (36): K0020, K0308, K0309, K0310, K0311, K0312, K0313, K0314, K0315, K0316, K0317, K0318, K0319, K0320, K0321, K0322, K0323, K0324, K0325, K0326, K0327, K0328, K0329, K0674, K0675, K0676, K0677, K0678, K0679, K0680, K0681, K0683, K0684, K0685, K0686, K0687
- classes any member touches: 36
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 9
  - N0064--N0093: 1 shared classes, 1 shared operand-type keys
  - N0064--N0118: 1 shared classes, 1 shared operand-type keys
  - N0064--N0142: 1 shared classes, 1 shared operand-type keys
  - N0068--N0093: 1 shared classes, 1 shared operand-type keys
  - N0068--N0118: 1 shared classes, 1 shared operand-type keys
  - N0068--N0142: 1 shared classes, 1 shared operand-type keys
  - N0093--N0118: 1 shared classes, 1 shared operand-type keys
  - N0093--N0142: 1 shared classes, 1 shared operand-type keys
  - N0118--N0142: 1 shared classes, 1 shared operand-type keys
- bridges: 49
  - K0039 dominates K0020 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c,cpp, dominated cpp,go,rust,swift
  - K0380 dominates K0308 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0381 dominates K0309 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0383 dominates K0310 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0384 dominates K0311 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0385 dominates K0312 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0386 dominates K0313 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0387 dominates K0314 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0389 dominates K0315 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0390 dominates K0316 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0391 dominates K0317 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0399 dominates K0318 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - (and 37 more)
- fences: 0
- languages absent:
  - c: attached by bridge only: a directional bridge reaches these classes, membership does not
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0064--N0068 | 36 | not-recorded-per-pair | not-recorded-per-pair |
| N0064--N0093 | 1 | sem | sem |
| N0064--N0118 | 1 | byte | byte |
| N0064--N0142 | 1 | byte | byte |
| N0068--N0093 | 1 | sem | sem |
| N0068--N0118 | 1 | byte | byte |
| N0068--N0142 | 1 | byte | byte |
| N0093--N0118 | 1 | sem | sem |
| N0093--N0142 | 1 | sem | sem |
| N0118--N0142 | 1 | byte | byte |

## D0016 -- 4 members over cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| cpp | `<` | binary |
| go | `<` | binary |
| rust | `<` | binary |
| swift | `<` | binary |

- classes spanned (8): K0054, K0055, K0124, K0125, K0126, K0357, K0847, K0852
- classes any member touches: 40
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 6
  - N0049--N0083: 5 shared classes, 5 shared operand-type keys
  - N0049--N0109: 6 shared classes, 6 shared operand-type keys
  - N0049--N0132: 7 shared classes, 7 shared operand-type keys
  - N0083--N0109: 5 shared classes, 5 shared operand-type keys
  - N0083--N0132: 5 shared classes, 5 shared operand-type keys
  - N0109--N0132: 5 shared classes, 5 shared operand-type keys
- bridges: 8
  - K0654 dominates K0054 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,go,rust,swift
  - K0661 dominates K0055 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,go,rust,swift
  - K0633 dominates K0124 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0640 dominates K0125 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0647 dominates K0126 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0668 dominates K0357 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust
  - K0634 dominates K0847 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0639 dominates K0852 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
- fences: 15
  - in0 >= 64 (unsigned) -> None x9
  - in1 >= 64 (unsigned) -> None x6
- languages absent:
  - c: attached by bridge only: a directional bridge reaches these classes, membership does not
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0049--N0083 | 5 | byte | not-recorded-per-pair |
| N0049--N0109 | 6 | byte | byte |
| N0049--N0132 | 7 | byte | not-recorded-per-pair |
| N0083--N0109 | 5 | byte | not-recorded-per-pair |
| N0083--N0132 | 5 | byte | not-recorded-per-pair |
| N0109--N0132 | 5 | byte | byte |

## D0017 -- 4 members over cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| cpp | `<=` | binary |
| go | `<=` | binary |
| rust | `<=` | binary |
| swift | `<=` | binary |

- classes spanned (11): K0058, K0059, K0358, K0359, K0360, K0361, K0372, K0373, K0374, K0817, K0822
- classes any member touches: 43
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 6
  - N0051--N0085: 2 shared classes, 2 shared operand-type keys
  - N0051--N0111: 6 shared classes, 6 shared operand-type keys
  - N0051--N0134: 4 shared classes, 4 shared operand-type keys
  - N0085--N0111: 2 shared classes, 2 shared operand-type keys
  - N0085--N0134: 5 shared classes, 5 shared operand-type keys
  - N0111--N0134: 2 shared classes, 2 shared operand-type keys
- bridges: 8
  - K0618 dominates K0058 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,go,rust,swift
  - K0625 dominates K0059 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,go,rust,swift
  - K0597 dominates K0358 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust
  - K0604 dominates K0359 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust
  - K0611 dominates K0360 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust
  - K0632 dominates K0361 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust
  - K0598 dominates K0817 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0603 dominates K0822 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
- fences: 10
  - in0 >= 64 (unsigned) -> None x6
  - in1 >= 64 (unsigned) -> None x4
- languages absent:
  - c: attached by bridge only: a directional bridge reaches these classes, membership does not
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0051--N0085 | 2 | byte | byte |
| N0051--N0111 | 6 | byte | byte |
| N0051--N0134 | 4 | byte | not-recorded-per-pair |
| N0085--N0111 | 2 | byte | byte |
| N0085--N0134 | 5 | byte | sem |
| N0111--N0134 | 2 | byte | byte |

## D0018 -- 4 members over cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| cpp | `==` | binary |
| go | `==` | binary |
| rust | `==` | binary |
| swift | `==` | binary |

- classes spanned (8): K0130, K0131, K0132, K0133, K0134, K0135, K0702, K0707
- classes any member touches: 42
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 6
  - N0053--N0086: 4 shared classes, 4 shared operand-type keys
  - N0053--N0112: 6 shared classes, 6 shared operand-type keys
  - N0053--N0135: 8 shared classes, 8 shared operand-type keys
  - N0086--N0112: 4 shared classes, 4 shared operand-type keys
  - N0086--N0135: 4 shared classes, 4 shared operand-type keys
  - N0112--N0135: 6 shared classes, 6 shared operand-type keys
- bridges: 8
  - K0453 dominates K0130 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0460 dominates K0131 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0467 dominates K0132 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0474 dominates K0133 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0481 dominates K0134 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0488 dominates K0135 on the result-register-only projection; adapter `read only %rax; the extra live register is not the answer`; dominant c, dominated cpp,rust,swift
  - K0454 dominates K0702 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0459 dominates K0707 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
- fences: 14
  - in0 >= 64 (unsigned) -> None x10
  - in1 >= 64 (unsigned) -> None x4
- languages absent:
  - c: attached by bridge only: a directional bridge reaches these classes, membership does not
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0053--N0086 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0053--N0112 | 6 | byte | byte |
| N0053--N0135 | 8 | byte | not-recorded-per-pair |
| N0086--N0112 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0086--N0135 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0112--N0135 | 6 | byte | byte |

## D0019 -- 4 members over cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| cpp | `>` | binary |
| go | `>` | binary |
| rust | `>` | binary |
| swift | `>` | binary |

- classes spanned (11): K0056, K0057, K0362, K0363, K0364, K0365, K0369, K0370, K0371, K0757, K0762
- classes any member touches: 43
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 6
  - N0054--N0087: 2 shared classes, 2 shared operand-type keys
  - N0054--N0113: 6 shared classes, 6 shared operand-type keys
  - N0054--N0136: 4 shared classes, 4 shared operand-type keys
  - N0087--N0113: 2 shared classes, 2 shared operand-type keys
  - N0087--N0136: 5 shared classes, 5 shared operand-type keys
  - N0113--N0136: 2 shared classes, 2 shared operand-type keys
- bridges: 8
  - K0546 dominates K0056 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,go,rust,swift
  - K0553 dominates K0057 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,go,rust,swift
  - K0525 dominates K0362 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust
  - K0532 dominates K0363 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust
  - K0539 dominates K0364 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust
  - K0560 dominates K0365 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust
  - K0526 dominates K0757 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0531 dominates K0762 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
- fences: 9
  - in0 >= 64 (unsigned) -> None x3
  - in1 >= 64 (unsigned) -> None x6
- languages absent:
  - c: attached by bridge only: a directional bridge reaches these classes, membership does not
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0054--N0087 | 2 | byte | byte |
| N0054--N0113 | 6 | byte | byte |
| N0054--N0136 | 4 | byte | not-recorded-per-pair |
| N0087--N0113 | 2 | byte | byte |
| N0087--N0136 | 5 | byte | sem |
| N0113--N0136 | 2 | byte | byte |

## D0020 -- 4 members over cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| cpp | `>=` | binary |
| go | `>=` | binary |
| rust | `>=` | binary |
| swift | `>=` | binary |

- classes spanned (8): K0060, K0061, K0127, K0128, K0129, K0366, K0787, K0792
- classes any member touches: 40
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 6
  - N0055--N0088: 5 shared classes, 5 shared operand-type keys
  - N0055--N0114: 6 shared classes, 6 shared operand-type keys
  - N0055--N0137: 7 shared classes, 7 shared operand-type keys
  - N0088--N0114: 5 shared classes, 5 shared operand-type keys
  - N0088--N0137: 5 shared classes, 5 shared operand-type keys
  - N0114--N0137: 5 shared classes, 5 shared operand-type keys
- bridges: 8
  - K0582 dominates K0060 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,go,rust,swift
  - K0589 dominates K0061 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,go,rust,swift
  - K0561 dominates K0127 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0568 dominates K0128 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0575 dominates K0129 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0596 dominates K0366 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust
  - K0562 dominates K0787 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0567 dominates K0792 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
- fences: 16
  - in0 >= 64 (unsigned) -> None x7
  - in1 >= 64 (unsigned) -> None x9
- languages absent:
  - c: attached by bridge only: a directional bridge reaches these classes, membership does not
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0055--N0088 | 5 | byte | not-recorded-per-pair |
| N0055--N0114 | 6 | byte | byte |
| N0055--N0137 | 7 | byte | not-recorded-per-pair |
| N0088--N0114 | 5 | byte | not-recorded-per-pair |
| N0088--N0137 | 5 | byte | not-recorded-per-pair |
| N0114--N0137 | 5 | byte | byte |

## D0021 -- 3 members over c, cpp, rust

| language | label | arity |
| --- | --- | --- |
| c | `<<` | binary |
| cpp | `<<` | binary |
| rust | `<<` | binary |

- classes spanned (16): K0106, K0107, K0108, K0109, K0110, K0111, K0112, K0113, K0114, K0294, K0295, K0296, K0297, K0298, K0299, K0300
- classes any member touches: 16
- strongest evidence over the member pairs: byte
- weakest over the member pairs: byte identity (the two units are the same machine bytes)
- weakest the class table itself recorded on the spanned classes: byte
- surviving edges: 3
  - N0018--N0050: 16 shared classes, 16 shared operand-type keys
  - N0018--N0110: 9 shared classes, 9 shared operand-type keys
  - N0050--N0110: 9 shared classes, 9 shared operand-type keys
- bridges: 0
- fences: 12
  - in1 >= 32 (unsigned) -> None x3
  - in1 >= 64 (unsigned) -> None x9
- languages absent:
  - go: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - swift: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0018--N0050 | 16 | byte | byte |
| N0018--N0110 | 9 | byte | byte |
| N0050--N0110 | 9 | byte | byte |

## D0022 -- 3 members over c, cpp, rust

| language | label | arity |
| --- | --- | --- |
| c | `>>` | binary |
| cpp | `>>` | binary |
| rust | `>>` | binary |

- classes spanned (16): K0115, K0116, K0117, K0118, K0119, K0120, K0121, K0122, K0123, K0301, K0302, K0303, K0304, K0305, K0306, K0307
- classes any member touches: 16
- strongest evidence over the member pairs: byte
- weakest over the member pairs: byte identity (the two units are the same machine bytes)
- weakest the class table itself recorded on the spanned classes: byte
- surviving edges: 3
  - N0023--N0056: 16 shared classes, 16 shared operand-type keys
  - N0023--N0115: 9 shared classes, 9 shared operand-type keys
  - N0056--N0115: 9 shared classes, 9 shared operand-type keys
- bridges: 0
- fences: 6
  - in1 >= 64 (unsigned) -> None x6
- languages absent:
  - go: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - swift: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0023--N0056 | 16 | byte | byte |
| N0023--N0115 | 9 | byte | byte |
| N0056--N0115 | 9 | byte | byte |

## D0023 -- 2 members over c, cpp

| language | label | arity |
| --- | --- | --- |
| c | `%` | binary |
| cpp | `%` | binary |

- classes spanned (16): K0265, K0266, K0267, K0269, K0270, K0271, K0272, K0273, K0274, K0275, K0276, K0277, K0278, K0279, K0280, K0281
- classes any member touches: 16
- strongest evidence over the member pairs: byte
- weakest over the member pairs: byte identity (the two units are the same machine bytes)
- weakest the class table itself recorded on the spanned classes: byte
- surviving edges: 1
  - N0003--N0035: 16 shared classes, 16 shared operand-type keys
- bridges: 0
- fences: 0
- languages absent:
  - go: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - rust: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - swift: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0003--N0035 | 16 | byte | byte |

## D0024 -- 2 members over c, cpp

| language | label | arity |
| --- | --- | --- |
| c | `&` | unary_prefix |
| cpp | `&` | unary_prefix |

- classes spanned (6): K0282, K0283, K0284, K0285, K0286, K0287
- classes any member touches: 6
- strongest evidence over the member pairs: byte
- weakest over the member pairs: byte identity (the two units are the same machine bytes)
- weakest the class table itself recorded on the spanned classes: byte
- surviving edges: 1
  - N0005--N0037: 6 shared classes, 6 shared operand-type keys
- bridges: 0
- fences: 0
- languages absent:
  - go: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - rust: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - swift: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0005--N0037 | 6 | byte | byte |

## D0025 -- 2 members over c, cpp

| language | label | arity |
| --- | --- | --- |
| c | `++` | unary_prefix |
| cpp | `++` | unary_prefix |

- classes spanned (5): K0037, K0038, K0288, K0289, K0290
- classes any member touches: 6
- strongest evidence over the member pairs: byte
- weakest over the member pairs: byte identity (the two units are the same machine bytes)
- weakest the class table itself recorded on the spanned classes: byte
- surviving edges: 1
  - N0011--N0043: 5 shared classes, 5 shared operand-type keys
- bridges: 0
- fences: 0
- languages absent:
  - go: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - rust: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - swift: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0011--N0043 | 5 | byte | byte |

## D0026 -- 2 members over go, rust

| language | label | arity |
| --- | --- | --- |
| go | `%` | binary |
| rust | `%` | binary |

- classes spanned (1): K0368
- classes any member touches: 7
- strongest evidence over the member pairs: core-text
- weakest over the member pairs: core-text identity: verdicts4's own column found the two normal-path cores textually equal
- weakest the class table itself recorded on the spanned classes: core-text
- surviving edges: 1
  - N0072--N0097: 1 shared classes, 1 shared operand-type keys
- bridges: 0
- fences: 8
  - ((-2147483648 + in0) | ~in1) == 0 -> None x1
  - (~in1 | (-9223372036854775808 ^ in0)) == 0 -> None x1
  - in1 == 0 -> None x6
- languages absent:
  - c: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - cpp: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - swift: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0072--N0097 | 1 | core-text | core-text |

## D0027 -- 2 members over go, swift

| language | label | arity |
| --- | --- | --- |
| go | `<<` | binary |
| swift | `<<` | binary |

- classes spanned (1): K0375
- classes any member touches: 17
- strongest evidence over the member pairs: z3
- weakest over the member pairs: z3 over the two lifted forms (a proof about the lifter's model, not about the bytes)
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 1
  - N0084--N0133: 1 shared classes, 1 shared operand-type keys
- bridges: 0
- fences: 18
  - in1 < 0 (signed) -> None x6
  - in1 >= 32 (unsigned) -> None x3
  - in1 >= 64 (unsigned) -> None x9
- languages absent:
  - c: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - cpp: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - rust: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0084--N0133 | 1 | z3 | z3 |

## D0028 -- 2 members over go, swift

| language | label | arity |
| --- | --- | --- |
| go | `>>` | binary |
| swift | `>>` | binary |

- classes spanned (1): K0376
- classes any member touches: 17
- strongest evidence over the member pairs: z3
- weakest over the member pairs: z3 over the two lifted forms (a proof about the lifter's model, not about the bytes)
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 1
  - N0089--N0138: 1 shared classes, 1 shared operand-type keys
- bridges: 0
- fences: 12
  - in1 < 0 (signed) -> None x6
  - in1 >= 64 (unsigned) -> None x6
- languages absent:
  - c: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - cpp: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - rust: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0089--N0138 | 1 | z3 | z3 |

