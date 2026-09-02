# dom_ops -- the dominant operators

- rule: THE DOM_OP CONSTRUCTION RULE (the owner, 2026-08-26): dominant operators are DISCOVERED from machine evidence by matching, never asserted
- node: a node is the PROVENANCE of a probe -- which grammar rule of ONE language generated it: language, grammar operator, arity bucket.  Arity is part of identity because one token can be two operators.
- candidate set: machine-form evidence only: two nodes are compared when they have units in the same equivalence class of dominant_table3.  No operator token takes part in any key, grouping, pairing or selection here.
- spelling: the operator token appears exactly once per node, as the display label `label` on a member that also carries its language and its id
- edge weights: primary: the number of equivalence classes in which the two nodes both have member units.  secondary: the number of distinct operand-type keys those classes carry, so a coincidence on bool alone scores 1.
- mutual filter: each node keeps its strongest counterpart per foreign language (classes, then type keys, then the smaller class count); the edge survives only when both endpoints chose each other
- intention: `intention` is null on every row by instruction; the hint field is proposed only.  the owner settles.

nodes 197, edges 601 before the mutual filter, 412 after, dom_ops 30

without the arity fix, the same construction gives nodes 178, edges 581 before the filter, 317 after, components 31.

the same-language assertion ran over 30 components; 60 collisions found.

the brief said a component cannot hold two nodes of one language BY CONSTRUCTION.  It can, and the assertion found it.  A node keeps one counterpart per foreign language, but a component is a CHAIN, and a chain can walk back into a language it already visited.  Nothing is merged and nothing is dropped here; the collision is recorded on the row and the owner settles the rule.

## D0001 -- 11 members over c, c, cpp, cpp, cpp, cpp, go, go, rust, rust, swift

| language | label | arity |
| --- | --- | --- |
| c | `&` | binary |
| c | `&=` | assignment |
| cpp | `&` | binary |
| cpp | `&=` | assignment |
| cpp | `and_eq` | assignment |
| cpp | `bitand` | binary |
| go | `&` | binary |
| go | `&=` | assignment |
| rust | `&` | binary |
| rust | `&=` | assignment |
| swift | `&` | binary |

- classes spanned (23): A0071, A0228, A0229, A0230, A0231, A0232, A0233, A0234, A0235, A0236, A0237, A0238, A0239, A0240, A0241, A0242, K0006, K0093, K0094, K0097, K0102, K0103, K0104
- classes any member touches: 23
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 36
  - N0005--N0048: 16 shared classes, 16 shared operand-type keys
  - N0005--N0081: 16 shared classes, 16 shared operand-type keys
  - N0005--N0099: 3 shared classes, 3 shared operand-type keys
  - N0005--N0102: 3 shared classes, 3 shared operand-type keys
  - N0005--N0171: 3 shared classes, 3 shared operand-type keys
  - N0008--N0051: 16 shared classes, 16 shared operand-type keys
  - N0008--N0080: 16 shared classes, 16 shared operand-type keys
  - N0008--N0099: 3 shared classes, 3 shared operand-type keys
  - N0008--N0102: 3 shared classes, 3 shared operand-type keys
  - N0008--N0136: 4 shared classes, 4 shared operand-type keys
  - N0008--N0138: 4 shared classes, 4 shared operand-type keys
  - N0008--N0171: 3 shared classes, 3 shared operand-type keys
  - N0048--N0099: 3 shared classes, 3 shared operand-type keys
  - N0048--N0102: 3 shared classes, 3 shared operand-type keys
  - N0048--N0171: 3 shared classes, 3 shared operand-type keys
  - N0051--N0099: 3 shared classes, 3 shared operand-type keys
  - N0051--N0102: 3 shared classes, 3 shared operand-type keys
  - N0051--N0136: 4 shared classes, 4 shared operand-type keys
  - N0051--N0138: 4 shared classes, 4 shared operand-type keys
  - N0051--N0171: 3 shared classes, 3 shared operand-type keys
  - N0080--N0099: 3 shared classes, 3 shared operand-type keys
  - N0080--N0102: 3 shared classes, 3 shared operand-type keys
  - N0080--N0136: 4 shared classes, 4 shared operand-type keys
  - N0080--N0138: 4 shared classes, 4 shared operand-type keys
  - N0080--N0171: 3 shared classes, 3 shared operand-type keys
  - N0081--N0099: 3 shared classes, 3 shared operand-type keys
  - N0081--N0102: 3 shared classes, 3 shared operand-type keys
  - N0081--N0171: 3 shared classes, 3 shared operand-type keys
  - N0099--N0136: 3 shared classes, 3 shared operand-type keys
  - N0099--N0138: 3 shared classes, 3 shared operand-type keys
  - N0099--N0171: 3 shared classes, 3 shared operand-type keys
  - N0102--N0136: 3 shared classes, 3 shared operand-type keys
  - N0102--N0138: 3 shared classes, 3 shared operand-type keys
  - N0102--N0171: 3 shared classes, 3 shared operand-type keys
  - N0136--N0171: 3 shared classes, 3 shared operand-type keys
  - N0138--N0171: 3 shared classes, 3 shared operand-type keys
- bridges: 1
  - K0006 dominates K0019 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c,cpp, dominated cpp,go,rust,swift
- fences: 0
- languages absent:
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0005--N0008 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0005--N0048 | 16 | byte | byte |
| N0005--N0051 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0005--N0080 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0005--N0081 | 16 | byte | byte |
| N0005--N0099 | 3 | sem | sem |
| N0005--N0102 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0005--N0136 | 3 | byte | byte |
| N0005--N0138 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0005--N0171 | 3 | byte | byte |
| N0008--N0048 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0008--N0051 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0008--N0080 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0008--N0081 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0008--N0099 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0008--N0102 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0008--N0136 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0008--N0138 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0008--N0171 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0048--N0051 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0048--N0080 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0048--N0081 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0048--N0099 | 3 | sem | sem |
| N0048--N0102 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0048--N0136 | 3 | byte | byte |
| N0048--N0138 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0048--N0171 | 3 | byte | byte |
| N0051--N0080 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0051--N0081 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0051--N0099 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0051--N0102 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0051--N0136 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0051--N0138 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0051--N0171 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0080--N0081 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0080--N0099 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0080--N0102 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0080--N0136 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0080--N0138 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0080--N0171 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0081--N0099 | 3 | sem | sem |
| N0081--N0102 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0081--N0136 | 3 | byte | byte |
| N0081--N0138 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0081--N0171 | 3 | byte | byte |
| N0099--N0102 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0099--N0136 | 3 | sem | sem |
| N0099--N0138 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0099--N0171 | 3 | sem | sem |
| N0102--N0136 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0102--N0138 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0102--N0171 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0136--N0138 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0136--N0171 | 3 | byte | byte |
| N0138--N0171 | 3 | not-recorded-per-pair | not-recorded-per-pair |

## D0002 -- 11 members over c, c, cpp, cpp, go, go, java, rust, rust, swift, swift

| language | label | arity |
| --- | --- | --- |
| c | `+` | binary |
| c | `+=` | assignment |
| cpp | `+` | binary |
| cpp | `+=` | assignment |
| go | `+` | binary |
| go | `+=` | assignment |
| java | `+` | binary |
| rust | `+` | binary |
| rust | `+=` | assignment |
| swift | `+` | binary |
| swift | `+=` | assignment |

- classes spanned (55): A0124, A0125, A0126, A0127, A0128, A0129, A0130, A0131, A0132, A0133, A0134, A0135, A0136, A0137, A0138, A0139, A0140, A0141, A0142, A0143, A0144, A0145, A0146, A0147, A0148, A0149, A0150, A0151, A0152, A0153, A0154, A0155, A0156, A0157, A0158, A0159, A0720, A0721, A0722, K0136
  (and 15 more)
- classes any member touches: 55
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 46
  - N0011--N0054: 36 shared classes, 36 shared operand-type keys
  - N0011--N0107: 5 shared classes, 5 shared operand-type keys
  - N0011--N0109: 5 shared classes, 5 shared operand-type keys
  - N0011--N0131: 1 shared classes, 1 shared operand-type keys
  - N0011--N0141: 5 shared classes, 5 shared operand-type keys
  - N0011--N0142: 5 shared classes, 5 shared operand-type keys
  - N0011--N0175: 2 shared classes, 2 shared operand-type keys
  - N0011--N0177: 2 shared classes, 2 shared operand-type keys
  - N0015--N0058: 36 shared classes, 36 shared operand-type keys
  - N0015--N0107: 5 shared classes, 5 shared operand-type keys
  - N0015--N0109: 5 shared classes, 5 shared operand-type keys
  - N0015--N0131: 1 shared classes, 1 shared operand-type keys
  - N0015--N0141: 5 shared classes, 5 shared operand-type keys
  - N0015--N0142: 5 shared classes, 5 shared operand-type keys
  - N0015--N0175: 2 shared classes, 2 shared operand-type keys
  - N0015--N0177: 2 shared classes, 2 shared operand-type keys
  - N0054--N0107: 5 shared classes, 5 shared operand-type keys
  - N0054--N0109: 5 shared classes, 5 shared operand-type keys
  - N0054--N0131: 1 shared classes, 1 shared operand-type keys
  - N0054--N0141: 5 shared classes, 5 shared operand-type keys
  - N0054--N0142: 5 shared classes, 5 shared operand-type keys
  - N0054--N0175: 2 shared classes, 2 shared operand-type keys
  - N0054--N0177: 2 shared classes, 2 shared operand-type keys
  - N0058--N0107: 5 shared classes, 5 shared operand-type keys
  - N0058--N0109: 5 shared classes, 5 shared operand-type keys
  - N0058--N0131: 1 shared classes, 1 shared operand-type keys
  - N0058--N0141: 5 shared classes, 5 shared operand-type keys
  - N0058--N0142: 5 shared classes, 5 shared operand-type keys
  - N0058--N0175: 2 shared classes, 2 shared operand-type keys
  - N0058--N0177: 2 shared classes, 2 shared operand-type keys
  - N0107--N0131: 1 shared classes, 1 shared operand-type keys
  - N0107--N0141: 5 shared classes, 5 shared operand-type keys
  - N0107--N0142: 5 shared classes, 5 shared operand-type keys
  - N0107--N0175: 2 shared classes, 2 shared operand-type keys
  - N0107--N0177: 2 shared classes, 2 shared operand-type keys
  - N0109--N0131: 1 shared classes, 1 shared operand-type keys
  - N0109--N0141: 5 shared classes, 5 shared operand-type keys
  - N0109--N0142: 5 shared classes, 5 shared operand-type keys
  - N0109--N0175: 2 shared classes, 2 shared operand-type keys
  - N0109--N0177: 2 shared classes, 2 shared operand-type keys
  - N0131--N0141: 1 shared classes, 1 shared operand-type keys
  - N0131--N0142: 1 shared classes, 1 shared operand-type keys
  - N0141--N0175: 2 shared classes, 2 shared operand-type keys
  - N0141--N0177: 2 shared classes, 2 shared operand-type keys
  - N0142--N0175: 2 shared classes, 2 shared operand-type keys
  - N0142--N0177: 2 shared classes, 2 shared operand-type keys
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
| N0011--N0015 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0011--N0054 | 36 | byte | byte |
| N0011--N0058 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0011--N0107 | 5 | byte | sem |
| N0011--N0109 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0011--N0131 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0011--N0141 | 5 | byte | byte |
| N0011--N0142 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0011--N0175 | 2 | byte | byte |
| N0011--N0177 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0015--N0054 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0015--N0058 | 36 | not-recorded-per-pair | not-recorded-per-pair |
| N0015--N0107 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0015--N0109 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0015--N0131 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0015--N0141 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0015--N0142 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0015--N0175 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0015--N0177 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0054--N0058 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0054--N0107 | 5 | byte | sem |
| N0054--N0109 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0054--N0131 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0054--N0141 | 5 | byte | byte |
| N0054--N0142 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0054--N0175 | 2 | byte | byte |
| N0054--N0177 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0058--N0107 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0058--N0109 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0058--N0131 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0058--N0141 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0058--N0142 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0058--N0175 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0058--N0177 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0107--N0109 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0107--N0131 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0107--N0141 | 5 | byte | sem |
| N0107--N0142 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0107--N0175 | 2 | byte | byte |
| N0107--N0177 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0109--N0131 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0109--N0141 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0109--N0142 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0109--N0175 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0109--N0177 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0131--N0141 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0131--N0142 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0131--N0175 | 0 | -- | -- |
| N0131--N0177 | 0 | -- | -- |
| N0141--N0142 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0141--N0175 | 2 | byte | byte |
| N0141--N0177 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0142--N0175 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0142--N0177 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0175--N0177 | 5 | not-recorded-per-pair | not-recorded-per-pair |

## D0003 -- 11 members over c, c, cpp, cpp, cpp, cpp, go, go, rust, rust, swift

| language | label | arity |
| --- | --- | --- |
| c | `^` | binary |
| c | `^=` | assignment |
| cpp | `^` | binary |
| cpp | `^=` | assignment |
| cpp | `xor` | binary |
| cpp | `xor_eq` | assignment |
| go | `^` | binary |
| go | `^=` | assignment |
| rust | `^` | binary |
| rust | `^=` | assignment |
| swift | `^` | binary |

- classes spanned (23): A0190, A0191, A0192, A0195, A0244, A0245, A0246, A0247, A0248, A0249, A0250, A0251, A0252, A0253, A0254, A0255, K0040, K0081, K0082, K0085, K0090, K0091, K0092
- classes any member touches: 23
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 36
  - N0033--N0077: 16 shared classes, 16 shared operand-type keys
  - N0033--N0089: 16 shared classes, 16 shared operand-type keys
  - N0033--N0125: 3 shared classes, 3 shared operand-type keys
  - N0033--N0127: 3 shared classes, 3 shared operand-type keys
  - N0033--N0194: 3 shared classes, 3 shared operand-type keys
  - N0034--N0078: 16 shared classes, 16 shared operand-type keys
  - N0034--N0090: 16 shared classes, 16 shared operand-type keys
  - N0034--N0125: 3 shared classes, 3 shared operand-type keys
  - N0034--N0127: 3 shared classes, 3 shared operand-type keys
  - N0034--N0162: 4 shared classes, 4 shared operand-type keys
  - N0034--N0163: 4 shared classes, 4 shared operand-type keys
  - N0034--N0194: 3 shared classes, 3 shared operand-type keys
  - N0077--N0125: 3 shared classes, 3 shared operand-type keys
  - N0077--N0127: 3 shared classes, 3 shared operand-type keys
  - N0077--N0194: 3 shared classes, 3 shared operand-type keys
  - N0078--N0125: 3 shared classes, 3 shared operand-type keys
  - N0078--N0127: 3 shared classes, 3 shared operand-type keys
  - N0078--N0162: 4 shared classes, 4 shared operand-type keys
  - N0078--N0163: 4 shared classes, 4 shared operand-type keys
  - N0078--N0194: 3 shared classes, 3 shared operand-type keys
  - N0089--N0125: 3 shared classes, 3 shared operand-type keys
  - N0089--N0127: 3 shared classes, 3 shared operand-type keys
  - N0089--N0194: 3 shared classes, 3 shared operand-type keys
  - N0090--N0125: 3 shared classes, 3 shared operand-type keys
  - N0090--N0127: 3 shared classes, 3 shared operand-type keys
  - N0090--N0162: 4 shared classes, 4 shared operand-type keys
  - N0090--N0163: 4 shared classes, 4 shared operand-type keys
  - N0090--N0194: 3 shared classes, 3 shared operand-type keys
  - N0125--N0162: 3 shared classes, 3 shared operand-type keys
  - N0125--N0163: 3 shared classes, 3 shared operand-type keys
  - N0125--N0194: 3 shared classes, 3 shared operand-type keys
  - N0127--N0162: 3 shared classes, 3 shared operand-type keys
  - N0127--N0163: 3 shared classes, 3 shared operand-type keys
  - N0127--N0194: 3 shared classes, 3 shared operand-type keys
  - N0162--N0194: 3 shared classes, 3 shared operand-type keys
  - N0163--N0194: 3 shared classes, 3 shared operand-type keys
- bridges: 1
  - K0040 dominates K0036 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c,cpp, dominated cpp,rust,swift
- fences: 0
- languages absent:
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0033--N0034 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0033--N0077 | 16 | byte | byte |
| N0033--N0078 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0033--N0089 | 16 | byte | byte |
| N0033--N0090 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0033--N0125 | 3 | sem | sem |
| N0033--N0127 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0033--N0162 | 3 | byte | byte |
| N0033--N0163 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0033--N0194 | 3 | byte | byte |
| N0034--N0077 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0034--N0078 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0034--N0089 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0034--N0090 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0034--N0125 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0034--N0127 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0034--N0162 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0034--N0163 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0034--N0194 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0077--N0078 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0077--N0089 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0077--N0090 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0077--N0125 | 3 | sem | sem |
| N0077--N0127 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0077--N0162 | 3 | byte | byte |
| N0077--N0163 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0077--N0194 | 3 | byte | byte |
| N0078--N0089 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0078--N0090 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0078--N0125 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0078--N0127 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0078--N0162 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0078--N0163 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0078--N0194 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0089--N0090 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0089--N0125 | 3 | sem | sem |
| N0089--N0127 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0089--N0162 | 3 | byte | byte |
| N0089--N0163 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0089--N0194 | 3 | byte | byte |
| N0090--N0125 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0090--N0127 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0090--N0162 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0090--N0163 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0090--N0194 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0125--N0127 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0125--N0162 | 3 | sem | sem |
| N0125--N0163 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0125--N0194 | 3 | sem | sem |
| N0127--N0162 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0127--N0163 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0127--N0194 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0162--N0163 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0162--N0194 | 3 | byte | byte |
| N0163--N0194 | 3 | not-recorded-per-pair | not-recorded-per-pair |

## D0004 -- 11 members over c, c, cpp, cpp, cpp, cpp, go, go, rust, rust, swift

| language | label | arity |
| --- | --- | --- |
| c | `\|` | binary |
| c | `\|=` | assignment |
| cpp | `bitor` | binary |
| cpp | `or_eq` | assignment |
| cpp | `\|` | binary |
| cpp | `\|=` | assignment |
| go | `\|` | binary |
| go | `\|=` | assignment |
| rust | `\|` | binary |
| rust | `\|=` | assignment |
| swift | `\|` | binary |

- classes spanned (23): A0159, A0260, A0261, A0262, A0263, A0264, A0265, A0266, A0267, A0268, A0269, A0270, A0271, A0272, A0273, A0274, K0039, K0069, K0070, K0073, K0078, K0079, K0080
- classes any member touches: 23
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 36
  - N0040--N0082: 16 shared classes, 16 shared operand-type keys
  - N0040--N0091: 16 shared classes, 16 shared operand-type keys
  - N0040--N0128: 3 shared classes, 3 shared operand-type keys
  - N0040--N0129: 3 shared classes, 3 shared operand-type keys
  - N0040--N0195: 3 shared classes, 3 shared operand-type keys
  - N0041--N0087: 16 shared classes, 16 shared operand-type keys
  - N0041--N0092: 16 shared classes, 16 shared operand-type keys
  - N0041--N0128: 3 shared classes, 3 shared operand-type keys
  - N0041--N0129: 3 shared classes, 3 shared operand-type keys
  - N0041--N0164: 4 shared classes, 4 shared operand-type keys
  - N0041--N0165: 4 shared classes, 4 shared operand-type keys
  - N0041--N0195: 3 shared classes, 3 shared operand-type keys
  - N0082--N0128: 3 shared classes, 3 shared operand-type keys
  - N0082--N0129: 3 shared classes, 3 shared operand-type keys
  - N0082--N0195: 3 shared classes, 3 shared operand-type keys
  - N0087--N0128: 3 shared classes, 3 shared operand-type keys
  - N0087--N0129: 3 shared classes, 3 shared operand-type keys
  - N0087--N0164: 4 shared classes, 4 shared operand-type keys
  - N0087--N0165: 4 shared classes, 4 shared operand-type keys
  - N0087--N0195: 3 shared classes, 3 shared operand-type keys
  - N0091--N0128: 3 shared classes, 3 shared operand-type keys
  - N0091--N0129: 3 shared classes, 3 shared operand-type keys
  - N0091--N0195: 3 shared classes, 3 shared operand-type keys
  - N0092--N0128: 3 shared classes, 3 shared operand-type keys
  - N0092--N0129: 3 shared classes, 3 shared operand-type keys
  - N0092--N0164: 4 shared classes, 4 shared operand-type keys
  - N0092--N0165: 4 shared classes, 4 shared operand-type keys
  - N0092--N0195: 3 shared classes, 3 shared operand-type keys
  - N0128--N0164: 3 shared classes, 3 shared operand-type keys
  - N0128--N0165: 3 shared classes, 3 shared operand-type keys
  - N0128--N0195: 3 shared classes, 3 shared operand-type keys
  - N0129--N0164: 3 shared classes, 3 shared operand-type keys
  - N0129--N0165: 3 shared classes, 3 shared operand-type keys
  - N0129--N0195: 3 shared classes, 3 shared operand-type keys
  - N0164--N0195: 3 shared classes, 3 shared operand-type keys
  - N0165--N0195: 3 shared classes, 3 shared operand-type keys
- bridges: 1
  - K0039 dominates K0020 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c,cpp, dominated cpp,go,rust,swift
- fences: 0
- languages absent:
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0040--N0041 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0040--N0082 | 16 | byte | byte |
| N0040--N0087 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0040--N0091 | 16 | byte | byte |
| N0040--N0092 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0040--N0128 | 3 | sem | sem |
| N0040--N0129 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0040--N0164 | 3 | byte | byte |
| N0040--N0165 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0040--N0195 | 3 | byte | byte |
| N0041--N0082 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0041--N0087 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0041--N0091 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0041--N0092 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0041--N0128 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0041--N0129 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0041--N0164 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0041--N0165 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0041--N0195 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0082--N0087 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0082--N0091 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0082--N0092 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0082--N0128 | 3 | sem | sem |
| N0082--N0129 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0082--N0164 | 3 | byte | byte |
| N0082--N0165 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0082--N0195 | 3 | byte | byte |
| N0087--N0091 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0087--N0092 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0087--N0128 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0087--N0129 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0087--N0164 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0087--N0165 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0087--N0195 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0091--N0092 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0091--N0128 | 3 | sem | sem |
| N0091--N0129 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0091--N0164 | 3 | byte | byte |
| N0091--N0165 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0091--N0195 | 3 | byte | byte |
| N0092--N0128 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0092--N0129 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0092--N0164 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0092--N0165 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0092--N0195 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0128--N0129 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0128--N0164 | 3 | sem | sem |
| N0128--N0165 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0128--N0195 | 3 | sem | sem |
| N0129--N0164 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0129--N0165 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0129--N0195 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0164--N0165 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0164--N0195 | 3 | byte | byte |
| N0165--N0195 | 3 | not-recorded-per-pair | not-recorded-per-pair |

## D0005 -- 10 members over c, c, cpp, cpp, go, go, rust, rust, swift, swift

| language | label | arity |
| --- | --- | --- |
| c | `*` | binary |
| c | `*=` | assignment |
| cpp | `*` | binary |
| cpp | `*=` | assignment |
| go | `*` | binary |
| go | `*=` | assignment |
| rust | `*` | binary |
| rust | `*=` | assignment |
| swift | `*` | binary |
| swift | `*=` | assignment |

- classes spanned (55): A0036, A0037, A0038, A0039, A0040, A0041, A0042, A0043, A0044, A0045, A0046, A0047, A0048, A0049, A0050, A0051, A0052, A0053, A0054, A0055, A0056, A0057, A0058, A0059, A0060, A0061, A0062, A0063, A0064, A0065, A0066, A0067, A0068, A0069, A0070, A0071, A0730, A0731, A0732, K0006
  (and 15 more)
- classes any member touches: 55
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 38
  - N0009--N0052: 36 shared classes, 36 shared operand-type keys
  - N0009--N0105: 5 shared classes, 5 shared operand-type keys
  - N0009--N0106: 5 shared classes, 5 shared operand-type keys
  - N0009--N0139: 5 shared classes, 5 shared operand-type keys
  - N0009--N0140: 5 shared classes, 5 shared operand-type keys
  - N0009--N0173: 2 shared classes, 2 shared operand-type keys
  - N0009--N0174: 2 shared classes, 2 shared operand-type keys
  - N0010--N0053: 36 shared classes, 36 shared operand-type keys
  - N0010--N0105: 5 shared classes, 5 shared operand-type keys
  - N0010--N0106: 5 shared classes, 5 shared operand-type keys
  - N0010--N0139: 5 shared classes, 5 shared operand-type keys
  - N0010--N0140: 5 shared classes, 5 shared operand-type keys
  - N0010--N0173: 2 shared classes, 2 shared operand-type keys
  - N0010--N0174: 2 shared classes, 2 shared operand-type keys
  - N0052--N0105: 5 shared classes, 5 shared operand-type keys
  - N0052--N0106: 5 shared classes, 5 shared operand-type keys
  - N0052--N0139: 5 shared classes, 5 shared operand-type keys
  - N0052--N0140: 5 shared classes, 5 shared operand-type keys
  - N0052--N0173: 2 shared classes, 2 shared operand-type keys
  - N0052--N0174: 2 shared classes, 2 shared operand-type keys
  - N0053--N0105: 5 shared classes, 5 shared operand-type keys
  - N0053--N0106: 5 shared classes, 5 shared operand-type keys
  - N0053--N0139: 5 shared classes, 5 shared operand-type keys
  - N0053--N0140: 5 shared classes, 5 shared operand-type keys
  - N0053--N0173: 2 shared classes, 2 shared operand-type keys
  - N0053--N0174: 2 shared classes, 2 shared operand-type keys
  - N0105--N0139: 5 shared classes, 5 shared operand-type keys
  - N0105--N0140: 5 shared classes, 5 shared operand-type keys
  - N0105--N0173: 2 shared classes, 2 shared operand-type keys
  - N0105--N0174: 2 shared classes, 2 shared operand-type keys
  - N0106--N0139: 5 shared classes, 5 shared operand-type keys
  - N0106--N0140: 5 shared classes, 5 shared operand-type keys
  - N0106--N0173: 2 shared classes, 2 shared operand-type keys
  - N0106--N0174: 2 shared classes, 2 shared operand-type keys
  - N0139--N0173: 2 shared classes, 2 shared operand-type keys
  - N0139--N0174: 2 shared classes, 2 shared operand-type keys
  - N0140--N0173: 2 shared classes, 2 shared operand-type keys
  - N0140--N0174: 2 shared classes, 2 shared operand-type keys
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
| N0009--N0010 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0009--N0052 | 36 | byte | byte |
| N0009--N0053 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0009--N0105 | 5 | byte | sem |
| N0009--N0106 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0009--N0139 | 5 | byte | byte |
| N0009--N0140 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0009--N0173 | 2 | byte | byte |
| N0009--N0174 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0010--N0052 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0010--N0053 | 36 | not-recorded-per-pair | not-recorded-per-pair |
| N0010--N0105 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0010--N0106 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0010--N0139 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0010--N0140 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0010--N0173 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0010--N0174 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0052--N0053 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0052--N0105 | 5 | byte | sem |
| N0052--N0106 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0052--N0139 | 5 | byte | byte |
| N0052--N0140 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0052--N0173 | 2 | byte | byte |
| N0052--N0174 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0053--N0105 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0053--N0106 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0053--N0139 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0053--N0140 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0053--N0173 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0053--N0174 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0105--N0106 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0105--N0139 | 5 | byte | sem |
| N0105--N0140 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0105--N0173 | 2 | byte | byte |
| N0105--N0174 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0106--N0139 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0106--N0140 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0106--N0173 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0106--N0174 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0139--N0140 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0139--N0173 | 2 | byte | byte |
| N0139--N0174 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0140--N0173 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0140--N0174 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0173--N0174 | 5 | not-recorded-per-pair | not-recorded-per-pair |

## D0006 -- 10 members over c, c, cpp, cpp, go, go, rust, rust, swift, swift

| language | label | arity |
| --- | --- | --- |
| c | `-` | binary |
| c | `-=` | assignment |
| cpp | `-` | binary |
| cpp | `-=` | assignment |
| go | `-` | binary |
| go | `-=` | assignment |
| rust | `-` | binary |
| rust | `-=` | assignment |
| swift | `-` | binary |
| swift | `-=` | assignment |

- classes spanned (55): A0160, A0161, A0162, A0163, A0164, A0165, A0166, A0167, A0168, A0169, A0170, A0171, A0172, A0173, A0174, A0175, A0176, A0177, A0178, A0179, A0180, A0181, A0182, A0183, A0184, A0185, A0186, A0187, A0188, A0189, A0190, A0191, A0192, A0193, A0194, A0195, A0725, A0726, A0727, K0167
  (and 15 more)
- classes any member touches: 55
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 38
  - N0016--N0059: 36 shared classes, 36 shared operand-type keys
  - N0016--N0110: 5 shared classes, 5 shared operand-type keys
  - N0016--N0112: 5 shared classes, 5 shared operand-type keys
  - N0016--N0143: 5 shared classes, 5 shared operand-type keys
  - N0016--N0145: 5 shared classes, 5 shared operand-type keys
  - N0016--N0178: 2 shared classes, 2 shared operand-type keys
  - N0016--N0180: 2 shared classes, 2 shared operand-type keys
  - N0020--N0063: 36 shared classes, 36 shared operand-type keys
  - N0020--N0110: 5 shared classes, 5 shared operand-type keys
  - N0020--N0112: 5 shared classes, 5 shared operand-type keys
  - N0020--N0143: 5 shared classes, 5 shared operand-type keys
  - N0020--N0145: 5 shared classes, 5 shared operand-type keys
  - N0020--N0178: 2 shared classes, 2 shared operand-type keys
  - N0020--N0180: 2 shared classes, 2 shared operand-type keys
  - N0059--N0110: 5 shared classes, 5 shared operand-type keys
  - N0059--N0112: 5 shared classes, 5 shared operand-type keys
  - N0059--N0143: 5 shared classes, 5 shared operand-type keys
  - N0059--N0145: 5 shared classes, 5 shared operand-type keys
  - N0059--N0178: 2 shared classes, 2 shared operand-type keys
  - N0059--N0180: 2 shared classes, 2 shared operand-type keys
  - N0063--N0110: 5 shared classes, 5 shared operand-type keys
  - N0063--N0112: 5 shared classes, 5 shared operand-type keys
  - N0063--N0143: 5 shared classes, 5 shared operand-type keys
  - N0063--N0145: 5 shared classes, 5 shared operand-type keys
  - N0063--N0178: 2 shared classes, 2 shared operand-type keys
  - N0063--N0180: 2 shared classes, 2 shared operand-type keys
  - N0110--N0143: 5 shared classes, 5 shared operand-type keys
  - N0110--N0145: 5 shared classes, 5 shared operand-type keys
  - N0110--N0178: 2 shared classes, 2 shared operand-type keys
  - N0110--N0180: 2 shared classes, 2 shared operand-type keys
  - N0112--N0143: 5 shared classes, 5 shared operand-type keys
  - N0112--N0145: 5 shared classes, 5 shared operand-type keys
  - N0112--N0178: 2 shared classes, 2 shared operand-type keys
  - N0112--N0180: 2 shared classes, 2 shared operand-type keys
  - N0143--N0178: 2 shared classes, 2 shared operand-type keys
  - N0143--N0180: 2 shared classes, 2 shared operand-type keys
  - N0145--N0178: 2 shared classes, 2 shared operand-type keys
  - N0145--N0180: 2 shared classes, 2 shared operand-type keys
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
| N0016--N0020 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0016--N0059 | 36 | byte | byte |
| N0016--N0063 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0016--N0110 | 5 | byte | sem |
| N0016--N0112 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0016--N0143 | 5 | byte | byte |
| N0016--N0145 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0016--N0178 | 2 | byte | byte |
| N0016--N0180 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0020--N0059 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0020--N0063 | 36 | not-recorded-per-pair | not-recorded-per-pair |
| N0020--N0110 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0020--N0112 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0020--N0143 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0020--N0145 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0020--N0178 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0020--N0180 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0059--N0063 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0059--N0110 | 5 | byte | sem |
| N0059--N0112 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0059--N0143 | 5 | byte | byte |
| N0059--N0145 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0059--N0178 | 2 | byte | byte |
| N0059--N0180 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0063--N0110 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0063--N0112 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0063--N0143 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0063--N0145 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0063--N0178 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0063--N0180 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0110--N0112 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0110--N0143 | 5 | byte | sem |
| N0110--N0145 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0110--N0178 | 2 | byte | byte |
| N0110--N0180 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0112--N0143 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0112--N0145 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0112--N0178 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0112--N0180 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0143--N0145 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0143--N0178 | 2 | byte | byte |
| N0143--N0180 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0145--N0178 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0145--N0180 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0178--N0180 | 5 | not-recorded-per-pair | not-recorded-per-pair |

## D0007 -- 10 members over c, c, cpp, cpp, go, go, rust, rust, swift, swift

| language | label | arity |
| --- | --- | --- |
| c | `/` | binary |
| c | `/=` | assignment |
| cpp | `/` | binary |
| cpp | `/=` | assignment |
| go | `/` | binary |
| go | `/=` | assignment |
| rust | `/` | binary |
| rust | `/=` | assignment |
| swift | `/` | binary |
| swift | `/=` | assignment |

- classes spanned (60): A0072, A0073, A0074, A0075, A0076, A0077, A0078, A0079, A0080, A0081, A0082, A0083, A0084, A0085, A0086, A0087, A0088, A0089, A0090, A0091, A0092, A0093, A0094, A0095, A0096, A0097, A0098, A0099, A0100, A0101, A0102, A0103, A0104, A0105, A0106, A0107, A0605, A0606, A0607, A0680
  (and 20 more)
- classes any member touches: 60
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: core-text
- surviving edges: 38
  - N0021--N0064: 36 shared classes, 36 shared operand-type keys
  - N0021--N0113: 2 shared classes, 2 shared operand-type keys
  - N0021--N0114: 2 shared classes, 2 shared operand-type keys
  - N0021--N0150: 2 shared classes, 2 shared operand-type keys
  - N0021--N0151: 2 shared classes, 2 shared operand-type keys
  - N0021--N0183: 2 shared classes, 2 shared operand-type keys
  - N0021--N0184: 2 shared classes, 2 shared operand-type keys
  - N0022--N0065: 36 shared classes, 36 shared operand-type keys
  - N0022--N0113: 2 shared classes, 2 shared operand-type keys
  - N0022--N0114: 2 shared classes, 2 shared operand-type keys
  - N0022--N0150: 2 shared classes, 2 shared operand-type keys
  - N0022--N0151: 2 shared classes, 2 shared operand-type keys
  - N0022--N0183: 2 shared classes, 2 shared operand-type keys
  - N0022--N0184: 2 shared classes, 2 shared operand-type keys
  - N0064--N0113: 2 shared classes, 2 shared operand-type keys
  - N0064--N0114: 2 shared classes, 2 shared operand-type keys
  - N0064--N0150: 2 shared classes, 2 shared operand-type keys
  - N0064--N0151: 2 shared classes, 2 shared operand-type keys
  - N0064--N0183: 2 shared classes, 2 shared operand-type keys
  - N0064--N0184: 2 shared classes, 2 shared operand-type keys
  - N0065--N0113: 2 shared classes, 2 shared operand-type keys
  - N0065--N0114: 2 shared classes, 2 shared operand-type keys
  - N0065--N0150: 2 shared classes, 2 shared operand-type keys
  - N0065--N0151: 2 shared classes, 2 shared operand-type keys
  - N0065--N0183: 2 shared classes, 2 shared operand-type keys
  - N0065--N0184: 2 shared classes, 2 shared operand-type keys
  - N0113--N0150: 3 shared classes, 3 shared operand-type keys
  - N0113--N0151: 3 shared classes, 3 shared operand-type keys
  - N0113--N0183: 2 shared classes, 2 shared operand-type keys
  - N0113--N0184: 2 shared classes, 2 shared operand-type keys
  - N0114--N0150: 3 shared classes, 3 shared operand-type keys
  - N0114--N0151: 3 shared classes, 3 shared operand-type keys
  - N0114--N0183: 2 shared classes, 2 shared operand-type keys
  - N0114--N0184: 2 shared classes, 2 shared operand-type keys
  - N0150--N0183: 2 shared classes, 2 shared operand-type keys
  - N0150--N0184: 2 shared classes, 2 shared operand-type keys
  - N0151--N0183: 2 shared classes, 2 shared operand-type keys
  - N0151--N0184: 2 shared classes, 2 shared operand-type keys
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
| N0021--N0022 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0021--N0064 | 36 | byte | byte |
| N0021--N0065 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0021--N0113 | 2 | byte | byte |
| N0021--N0114 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0021--N0150 | 2 | byte | byte |
| N0021--N0151 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0021--N0183 | 2 | byte | byte |
| N0021--N0184 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0022--N0064 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0022--N0065 | 36 | not-recorded-per-pair | not-recorded-per-pair |
| N0022--N0113 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0022--N0114 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0022--N0150 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0022--N0151 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0022--N0183 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0022--N0184 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0064--N0065 | 20 | not-recorded-per-pair | not-recorded-per-pair |
| N0064--N0113 | 2 | byte | byte |
| N0064--N0114 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0064--N0150 | 2 | byte | byte |
| N0064--N0151 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0064--N0183 | 2 | byte | byte |
| N0064--N0184 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0065--N0113 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0065--N0114 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0065--N0150 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0065--N0151 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0065--N0183 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0065--N0184 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0113--N0114 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0113--N0150 | 3 | byte | core-text |
| N0113--N0151 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0113--N0183 | 2 | byte | byte |
| N0113--N0184 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0114--N0150 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0114--N0151 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0114--N0183 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0114--N0184 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0150--N0151 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0150--N0183 | 2 | byte | byte |
| N0150--N0184 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0151--N0183 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0151--N0184 | 2 | not-recorded-per-pair | not-recorded-per-pair |
| N0183--N0184 | 5 | not-recorded-per-pair | not-recorded-per-pair |

## D0008 -- 9 members over c, c, c, c, cpp, cpp, cpp, go, swift

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
  - N0012--N0055: 6 shared classes, 6 shared operand-type keys
  - N0012--N0108: 2 shared classes, 2 shared operand-type keys
  - N0012--N0176: 5 shared classes, 5 shared operand-type keys
  - N0013--N0056: 5 shared classes, 5 shared operand-type keys
  - N0013--N0061: 5 shared classes, 5 shared operand-type keys
  - N0013--N0108: 2 shared classes, 2 shared operand-type keys
  - N0013--N0176: 5 shared classes, 5 shared operand-type keys
  - N0018--N0056: 5 shared classes, 5 shared operand-type keys
  - N0018--N0061: 5 shared classes, 5 shared operand-type keys
  - N0018--N0108: 2 shared classes, 2 shared operand-type keys
  - N0018--N0176: 5 shared classes, 5 shared operand-type keys
  - N0038--N0056: 5 shared classes, 5 shared operand-type keys
  - N0038--N0061: 5 shared classes, 5 shared operand-type keys
  - N0038--N0108: 2 shared classes, 2 shared operand-type keys
  - N0038--N0176: 5 shared classes, 5 shared operand-type keys
  - N0056--N0108: 2 shared classes, 2 shared operand-type keys
  - N0056--N0176: 5 shared classes, 5 shared operand-type keys
  - N0061--N0108: 2 shared classes, 2 shared operand-type keys
  - N0061--N0176: 5 shared classes, 5 shared operand-type keys
  - N0108--N0176: 2 shared classes, 2 shared operand-type keys
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
| N0012--N0013 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0012--N0018 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0012--N0038 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0012--N0055 | 6 | byte | byte |
| N0012--N0056 | 5 | byte | byte |
| N0012--N0061 | 5 | byte | byte |
| N0012--N0108 | 2 | byte | byte |
| N0012--N0176 | 5 | byte | byte |
| N0013--N0018 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0013--N0038 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0013--N0055 | 5 | byte | byte |
| N0013--N0056 | 5 | byte | byte |
| N0013--N0061 | 5 | byte | byte |
| N0013--N0108 | 2 | byte | byte |
| N0013--N0176 | 5 | byte | byte |
| N0018--N0038 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0018--N0055 | 5 | byte | byte |
| N0018--N0056 | 5 | byte | byte |
| N0018--N0061 | 5 | byte | byte |
| N0018--N0108 | 2 | byte | byte |
| N0018--N0176 | 5 | byte | byte |
| N0038--N0055 | 5 | byte | byte |
| N0038--N0056 | 5 | byte | byte |
| N0038--N0061 | 5 | byte | byte |
| N0038--N0108 | 2 | byte | byte |
| N0038--N0176 | 5 | byte | byte |
| N0055--N0056 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0055--N0061 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0055--N0108 | 2 | byte | byte |
| N0055--N0176 | 5 | byte | byte |
| N0056--N0061 | 5 | not-recorded-per-pair | not-recorded-per-pair |
| N0056--N0108 | 2 | byte | byte |
| N0056--N0176 | 5 | byte | byte |
| N0061--N0108 | 2 | byte | byte |
| N0061--N0176 | 5 | byte | byte |
| N0108--N0176 | 2 | byte | byte |

## D0009 -- 7 members over c, c, cpp, cpp, rust, rust, swift

| language | label | arity |
| --- | --- | --- |
| c | `<<` | binary |
| c | `<<=` | assignment |
| cpp | `<<` | binary |
| cpp | `<<=` | assignment |
| rust | `<<` | binary |
| rust | `<<=` | assignment |
| swift | `??` | binary |

- classes spanned (20): A0107, A0196, A0197, A0198, A0199, A0200, A0201, A0202, A0203, A0204, A0205, A0206, A0207, A0208, A0209, A0210, K0297, K0298, K0299, K0300
- classes any member touches: 25
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: byte
- surviving edges: 12
  - N0024--N0067: 16 shared classes, 16 shared operand-type keys
  - N0024--N0153: 9 shared classes, 9 shared operand-type keys
  - N0024--N0154: 9 shared classes, 9 shared operand-type keys
  - N0025--N0068: 16 shared classes, 16 shared operand-type keys
  - N0025--N0153: 9 shared classes, 9 shared operand-type keys
  - N0025--N0154: 9 shared classes, 9 shared operand-type keys
  - N0025--N0193: 1 shared classes, 1 shared operand-type keys
  - N0067--N0153: 9 shared classes, 9 shared operand-type keys
  - N0067--N0154: 9 shared classes, 9 shared operand-type keys
  - N0068--N0153: 9 shared classes, 9 shared operand-type keys
  - N0068--N0154: 9 shared classes, 9 shared operand-type keys
  - N0068--N0193: 1 shared classes, 1 shared operand-type keys
- bridges: 0
- fences: 12
  - in1 >= 32 (unsigned) -> None x3
  - in1 >= 64 (unsigned) -> None x9
- languages absent:
  - go: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0024--N0025 | 12 | not-recorded-per-pair | not-recorded-per-pair |
| N0024--N0067 | 16 | byte | byte |
| N0024--N0068 | 12 | not-recorded-per-pair | not-recorded-per-pair |
| N0024--N0153 | 9 | byte | byte |
| N0024--N0154 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0024--N0193 | 0 | -- | -- |
| N0025--N0067 | 12 | not-recorded-per-pair | not-recorded-per-pair |
| N0025--N0068 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0025--N0153 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0025--N0154 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0025--N0193 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0067--N0068 | 12 | not-recorded-per-pair | not-recorded-per-pair |
| N0067--N0153 | 9 | byte | byte |
| N0067--N0154 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0067--N0193 | 0 | -- | -- |
| N0068--N0153 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0068--N0154 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0068--N0193 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0153--N0154 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0153--N0193 | 0 | -- | -- |
| N0154--N0193 | 0 | -- | -- |

## D0010 -- 6 members over c, cpp, cpp, cpp, go, swift

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
  - N0019--N0062: 5 shared classes, 5 shared operand-type keys
  - N0019--N0095: 1 shared classes, 1 shared operand-type keys
  - N0019--N0167: 1 shared classes, 1 shared operand-type keys
  - N0044--N0095: 1 shared classes, 1 shared operand-type keys
  - N0044--N0167: 1 shared classes, 1 shared operand-type keys
  - N0084--N0095: 1 shared classes, 1 shared operand-type keys
  - N0084--N0167: 1 shared classes, 1 shared operand-type keys
  - N0095--N0167: 1 shared classes, 1 shared operand-type keys
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
| N0019--N0044 | 1 | byte | byte |
| N0019--N0062 | 5 | byte | byte |
| N0019--N0084 | 1 | byte | byte |
| N0019--N0095 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0019--N0167 | 1 | byte | byte |
| N0044--N0062 | 0 | -- | -- |
| N0044--N0084 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0044--N0095 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0044--N0167 | 1 | byte | byte |
| N0062--N0084 | 0 | -- | -- |
| N0062--N0095 | 0 | -- | -- |
| N0062--N0167 | 0 | -- | -- |
| N0084--N0095 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0084--N0167 | 1 | byte | byte |
| N0095--N0167 | 1 | not-recorded-per-pair | not-recorded-per-pair |

## D0011 -- 6 members over c, c, cpp, cpp, rust, rust

| language | label | arity |
| --- | --- | --- |
| c | `>>` | binary |
| c | `>>=` | assignment |
| cpp | `>>` | binary |
| cpp | `>>=` | assignment |
| rust | `>>` | binary |
| rust | `>>=` | assignment |

- classes spanned (20): A0212, A0213, A0214, A0215, A0216, A0217, A0218, A0219, A0220, A0221, A0222, A0223, A0224, A0225, A0226, A0227, K0304, K0305, K0306, K0307
- classes any member touches: 20
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: byte
- surviving edges: 10
  - N0031--N0075: 16 shared classes, 16 shared operand-type keys
  - N0031--N0160: 9 shared classes, 9 shared operand-type keys
  - N0031--N0161: 9 shared classes, 9 shared operand-type keys
  - N0032--N0076: 16 shared classes, 16 shared operand-type keys
  - N0032--N0160: 9 shared classes, 9 shared operand-type keys
  - N0032--N0161: 9 shared classes, 9 shared operand-type keys
  - N0075--N0160: 9 shared classes, 9 shared operand-type keys
  - N0075--N0161: 9 shared classes, 9 shared operand-type keys
  - N0076--N0160: 9 shared classes, 9 shared operand-type keys
  - N0076--N0161: 9 shared classes, 9 shared operand-type keys
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
| N0031--N0032 | 12 | not-recorded-per-pair | not-recorded-per-pair |
| N0031--N0075 | 16 | byte | byte |
| N0031--N0076 | 12 | not-recorded-per-pair | not-recorded-per-pair |
| N0031--N0160 | 9 | byte | byte |
| N0031--N0161 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0032--N0075 | 12 | not-recorded-per-pair | not-recorded-per-pair |
| N0032--N0076 | 16 | not-recorded-per-pair | not-recorded-per-pair |
| N0032--N0160 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0032--N0161 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0075--N0076 | 12 | not-recorded-per-pair | not-recorded-per-pair |
| N0075--N0160 | 9 | byte | byte |
| N0075--N0161 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0076--N0160 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0076--N0161 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0160--N0161 | 9 | not-recorded-per-pair | not-recorded-per-pair |

## D0012 -- 6 members over c, cpp, cpp, go, rust, swift

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
  - N0043--N0083: 4 shared classes, 4 shared operand-type keys
  - N0043--N0094: 4 shared classes, 4 shared operand-type keys
  - N0043--N0126: 3 shared classes, 3 shared operand-type keys
  - N0043--N0132: 3 shared classes, 3 shared operand-type keys
  - N0043--N0197: 3 shared classes, 3 shared operand-type keys
  - N0083--N0126: 3 shared classes, 3 shared operand-type keys
  - N0083--N0132: 3 shared classes, 3 shared operand-type keys
  - N0083--N0197: 3 shared classes, 3 shared operand-type keys
  - N0094--N0126: 3 shared classes, 3 shared operand-type keys
  - N0094--N0132: 3 shared classes, 3 shared operand-type keys
  - N0094--N0197: 3 shared classes, 3 shared operand-type keys
  - N0126--N0132: 3 shared classes, 3 shared operand-type keys
  - N0126--N0197: 3 shared classes, 3 shared operand-type keys
  - N0132--N0197: 3 shared classes, 3 shared operand-type keys
- bridges: 0
- fences: 1
  - in0 >= 64 (unsigned) -> None x1
- languages absent:
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0043--N0083 | 4 | byte | byte |
| N0043--N0094 | 4 | byte | byte |
| N0043--N0126 | 3 | sem | sem |
| N0043--N0132 | 3 | byte | byte |
| N0043--N0197 | 3 | byte | byte |
| N0083--N0094 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0083--N0126 | 3 | sem | sem |
| N0083--N0132 | 3 | byte | byte |
| N0083--N0197 | 3 | byte | byte |
| N0094--N0126 | 3 | sem | sem |
| N0094--N0132 | 3 | byte | byte |
| N0094--N0197 | 3 | byte | byte |
| N0126--N0132 | 3 | sem | sem |
| N0126--N0197 | 3 | sem | sem |
| N0132--N0197 | 3 | byte | byte |

## D0013 -- 5 members over c, cpp, go, rust, swift

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
  - N0017--N0060: 6 shared classes, 6 shared operand-type keys
  - N0017--N0111: 3 shared classes, 3 shared operand-type keys
  - N0017--N0144: 4 shared classes, 4 shared operand-type keys
  - N0017--N0179: 2 shared classes, 2 shared operand-type keys
  - N0060--N0111: 3 shared classes, 3 shared operand-type keys
  - N0060--N0144: 4 shared classes, 4 shared operand-type keys
  - N0060--N0179: 2 shared classes, 2 shared operand-type keys
  - N0111--N0144: 2 shared classes, 2 shared operand-type keys
  - N0144--N0179: 2 shared classes, 2 shared operand-type keys
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
| N0017--N0060 | 6 | byte | byte |
| N0017--N0111 | 3 | sem | sem |
| N0017--N0144 | 4 | byte | byte |
| N0017--N0179 | 2 | byte | byte |
| N0060--N0111 | 3 | sem | sem |
| N0060--N0144 | 4 | byte | byte |
| N0060--N0179 | 2 | byte | byte |
| N0111--N0144 | 2 | sem | sem |
| N0111--N0179 | 0 | -- | -- |
| N0144--N0179 | 2 | byte | byte |

## D0014 -- 5 members over c, cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| c | `=` | assignment |
| cpp | `=` | assignment |
| go | `=` | assignment |
| rust | `=` | assignment |
| swift | `=` | assignment |

- classes spanned (36): A0000, A0001, A0002, A0003, A0004, A0005, A0006, A0007, A0008, A0009, A0010, A0011, A0012, A0013, A0014, A0015, A0016, A0017, A0018, A0019, A0020, A0021, A0022, A0023, A0024, A0025, A0026, A0027, A0028, A0029, A0030, A0031, A0032, A0033, A0034, A0035
- classes any member touches: 36
- strongest evidence over the member pairs: not-recorded-per-pair
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 10
  - N0027--N0071: 36 shared classes, 36 shared operand-type keys
  - N0027--N0119: 6 shared classes, 6 shared operand-type keys
  - N0027--N0156: 6 shared classes, 6 shared operand-type keys
  - N0027--N0188: 6 shared classes, 6 shared operand-type keys
  - N0071--N0119: 6 shared classes, 6 shared operand-type keys
  - N0071--N0156: 6 shared classes, 6 shared operand-type keys
  - N0071--N0188: 6 shared classes, 6 shared operand-type keys
  - N0119--N0156: 6 shared classes, 6 shared operand-type keys
  - N0119--N0188: 6 shared classes, 6 shared operand-type keys
  - N0156--N0188: 6 shared classes, 6 shared operand-type keys
- bridges: 0
- fences: 0
- languages absent:
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0027--N0071 | 36 | not-recorded-per-pair | not-recorded-per-pair |
| N0027--N0119 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0027--N0156 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0027--N0188 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0071--N0119 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0071--N0156 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0071--N0188 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0119--N0156 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0119--N0188 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0156--N0188 | 6 | not-recorded-per-pair | not-recorded-per-pair |

## D0015 -- 5 members over c, c, c, c, cpp

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
  - N0035--N0088: 6 shared classes, 6 shared operand-type keys
  - N0036--N0088: 6 shared classes, 6 shared operand-type keys
  - N0037--N0088: 6 shared classes, 6 shared operand-type keys
  - N0039--N0088: 6 shared classes, 6 shared operand-type keys
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
| N0035--N0036 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0035--N0037 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0035--N0039 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0035--N0088 | 6 | byte | byte |
| N0036--N0037 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0036--N0039 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0036--N0088 | 6 | byte | byte |
| N0037--N0039 | 6 | not-recorded-per-pair | not-recorded-per-pair |
| N0037--N0088 | 6 | byte | byte |
| N0039--N0088 | 6 | byte | byte |

## D0016 -- 5 members over cpp, cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| cpp | `!=` | binary |
| cpp | `not_eq` | binary |
| go | `!=` | binary |
| rust | `!=` | binary |
| swift | `!=` | binary |

- classes spanned (36): A0190, A0191, A0192, A0193, A0194, A0195, K0062, K0063, K0064, K0065, K0066, K0352, K0353, K0354, K0732, K0733, K0734, K0735, K0736, K0737, K0738, K0739, K0740, K0741, K0742, K0743, K0744, K0745, K0746, K0747, K0748, K0749, K0750, K0751, K0752, K0753
- classes any member touches: 42
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 9
  - N0045--N0096: 4 shared classes, 4 shared operand-type keys
  - N0045--N0133: 6 shared classes, 6 shared operand-type keys
  - N0045--N0168: 8 shared classes, 8 shared operand-type keys
  - N0085--N0096: 4 shared classes, 4 shared operand-type keys
  - N0085--N0133: 6 shared classes, 6 shared operand-type keys
  - N0085--N0168: 8 shared classes, 8 shared operand-type keys
  - N0096--N0133: 4 shared classes, 4 shared operand-type keys
  - N0096--N0168: 4 shared classes, 4 shared operand-type keys
  - N0133--N0168: 6 shared classes, 6 shared operand-type keys
- bridges: 44
  - K0489 dominates K0062 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0497 dominates K0063 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0504 dominates K0064 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0511 dominates K0065 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0518 dominates K0066 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp,rust,swift
  - K0490 dominates K0352 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0496 dominates K0353 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0501 dominates K0354 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0492 dominates K0732 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0492 dominates K0732 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0493 dominates K0733 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - K0493 dominates K0733 on the low-8 projection; adapter `movzbl %al, %eax`; dominant c, dominated cpp
  - (and 32 more)
- fences: 26
  - in0 >= 64 (unsigned) -> None x18
  - in1 >= 64 (unsigned) -> None x8
- languages absent:
  - c: no mutual counterpart: the language has units in these classes, but no node of it was chosen back
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0045--N0085 | 36 | not-recorded-per-pair | not-recorded-per-pair |
| N0045--N0096 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0045--N0133 | 6 | byte | byte |
| N0045--N0168 | 8 | byte | not-recorded-per-pair |
| N0085--N0096 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0085--N0133 | 6 | byte | byte |
| N0085--N0168 | 8 | byte | not-recorded-per-pair |
| N0096--N0133 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0096--N0168 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0133--N0168 | 6 | byte | byte |

## D0017 -- 4 members over cpp, go, rust, swift

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
  - N0066--N0115: 5 shared classes, 5 shared operand-type keys
  - N0066--N0152: 6 shared classes, 6 shared operand-type keys
  - N0066--N0185: 7 shared classes, 7 shared operand-type keys
  - N0115--N0152: 5 shared classes, 5 shared operand-type keys
  - N0115--N0185: 5 shared classes, 5 shared operand-type keys
  - N0152--N0185: 5 shared classes, 5 shared operand-type keys
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
| N0066--N0115 | 5 | byte | not-recorded-per-pair |
| N0066--N0152 | 6 | byte | byte |
| N0066--N0185 | 7 | byte | not-recorded-per-pair |
| N0115--N0152 | 5 | byte | not-recorded-per-pair |
| N0115--N0185 | 5 | byte | not-recorded-per-pair |
| N0152--N0185 | 5 | byte | byte |

## D0018 -- 4 members over cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| cpp | `<=` | binary |
| go | `<=` | binary |
| rust | `<=` | binary |
| swift | `<=` | binary |

- classes spanned (8): K0058, K0059, K0358, K0359, K0360, K0361, K0817, K0822
- classes any member touches: 40
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 6
  - N0069--N0118: 5 shared classes, 5 shared operand-type keys
  - N0069--N0155: 6 shared classes, 6 shared operand-type keys
  - N0069--N0187: 7 shared classes, 7 shared operand-type keys
  - N0118--N0155: 5 shared classes, 5 shared operand-type keys
  - N0118--N0187: 5 shared classes, 5 shared operand-type keys
  - N0155--N0187: 5 shared classes, 5 shared operand-type keys
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
| N0069--N0118 | 5 | byte | not-recorded-per-pair |
| N0069--N0155 | 6 | byte | byte |
| N0069--N0187 | 7 | byte | not-recorded-per-pair |
| N0118--N0155 | 5 | byte | not-recorded-per-pair |
| N0118--N0187 | 5 | byte | sem |
| N0155--N0187 | 5 | byte | not-recorded-per-pair |

## D0019 -- 4 members over cpp, go, rust, swift

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
  - N0072--N0120: 4 shared classes, 4 shared operand-type keys
  - N0072--N0157: 6 shared classes, 6 shared operand-type keys
  - N0072--N0189: 8 shared classes, 8 shared operand-type keys
  - N0120--N0157: 4 shared classes, 4 shared operand-type keys
  - N0120--N0189: 4 shared classes, 4 shared operand-type keys
  - N0157--N0189: 6 shared classes, 6 shared operand-type keys
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
| N0072--N0120 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0072--N0157 | 6 | byte | byte |
| N0072--N0189 | 8 | byte | not-recorded-per-pair |
| N0120--N0157 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0120--N0189 | 4 | not-recorded-per-pair | not-recorded-per-pair |
| N0157--N0189 | 6 | byte | byte |

## D0020 -- 4 members over cpp, go, rust, swift

| language | label | arity |
| --- | --- | --- |
| cpp | `>` | binary |
| go | `>` | binary |
| rust | `>` | binary |
| swift | `>` | binary |

- classes spanned (8): K0056, K0057, K0362, K0363, K0364, K0365, K0757, K0762
- classes any member touches: 40
- strongest evidence over the member pairs: byte
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 6
  - N0073--N0121: 5 shared classes, 5 shared operand-type keys
  - N0073--N0158: 6 shared classes, 6 shared operand-type keys
  - N0073--N0190: 7 shared classes, 7 shared operand-type keys
  - N0121--N0158: 5 shared classes, 5 shared operand-type keys
  - N0121--N0190: 5 shared classes, 5 shared operand-type keys
  - N0158--N0190: 5 shared classes, 5 shared operand-type keys
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
| N0073--N0121 | 5 | byte | not-recorded-per-pair |
| N0073--N0158 | 6 | byte | byte |
| N0073--N0190 | 7 | byte | not-recorded-per-pair |
| N0121--N0158 | 5 | byte | not-recorded-per-pair |
| N0121--N0190 | 5 | byte | sem |
| N0158--N0190 | 5 | byte | not-recorded-per-pair |

## D0021 -- 4 members over cpp, go, rust, swift

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
  - N0074--N0122: 5 shared classes, 5 shared operand-type keys
  - N0074--N0159: 6 shared classes, 6 shared operand-type keys
  - N0074--N0191: 7 shared classes, 7 shared operand-type keys
  - N0122--N0159: 5 shared classes, 5 shared operand-type keys
  - N0122--N0191: 5 shared classes, 5 shared operand-type keys
  - N0159--N0191: 5 shared classes, 5 shared operand-type keys
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
| N0074--N0122 | 5 | byte | not-recorded-per-pair |
| N0074--N0159 | 6 | byte | byte |
| N0074--N0191 | 7 | byte | not-recorded-per-pair |
| N0122--N0159 | 5 | byte | not-recorded-per-pair |
| N0122--N0191 | 5 | byte | not-recorded-per-pair |
| N0159--N0191 | 5 | byte | byte |

## D0022 -- 4 members over go, go, rust, rust

| language | label | arity |
| --- | --- | --- |
| go | `%` | binary |
| go | `%=` | assignment |
| rust | `%` | binary |
| rust | `%=` | assignment |

- classes spanned (7): A0610, A0611, A0612, A0685, A0686, A0688, A0689
- classes any member touches: 7
- strongest evidence over the member pairs: core-text
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: core-text
- surviving edges: 4
  - N0097--N0134: 1 shared classes, 1 shared operand-type keys
  - N0097--N0135: 1 shared classes, 1 shared operand-type keys
  - N0098--N0134: 1 shared classes, 1 shared operand-type keys
  - N0098--N0135: 1 shared classes, 1 shared operand-type keys
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
| N0097--N0098 | 3 | not-recorded-per-pair | not-recorded-per-pair |
| N0097--N0134 | 1 | core-text | core-text |
| N0097--N0135 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0098--N0134 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0098--N0135 | 1 | not-recorded-per-pair | not-recorded-per-pair |
| N0134--N0135 | 5 | not-recorded-per-pair | not-recorded-per-pair |

## D0023 -- 3 members over go, rust, swift

| language | label | arity |
| --- | --- | --- |
| go | `&&` | binary |
| rust | `&&` | binary |
| swift | `&&` | binary |

- classes spanned (1): A0071
- classes any member touches: 1
- strongest evidence over the member pairs: byte
- weakest over the member pairs: anchored sem identity (the two lifted forms are identical)
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 3
  - N0101--N0137: 1 shared classes, 1 shared operand-type keys
  - N0101--N0172: 1 shared classes, 1 shared operand-type keys
  - N0137--N0172: 1 shared classes, 1 shared operand-type keys
- bridges: 0
- fences: 0
- languages absent:
  - c: no mutual counterpart: the language has units in these classes, but no node of it was chosen back
  - cpp: no mutual counterpart: the language has units in these classes, but no node of it was chosen back
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0101--N0137 | 1 | sem | sem |
| N0101--N0172 | 1 | sem | sem |
| N0137--N0172 | 1 | byte | byte |

## D0024 -- 3 members over go, go, swift

| language | label | arity |
| --- | --- | --- |
| go | `<<` | binary |
| go | `<<=` | assignment |
| swift | `<<` | binary |

- classes spanned (9): A0613, A0614, A0615, A0616, A0617, A0618, A0619, A0620, A0621
- classes any member touches: 17
- strongest evidence over the member pairs: z3
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 2
  - N0116--N0186: 1 shared classes, 1 shared operand-type keys
  - N0117--N0186: 1 shared classes, 1 shared operand-type keys
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
| N0116--N0117 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0116--N0186 | 1 | z3 | z3 |
| N0117--N0186 | 1 | not-recorded-per-pair | not-recorded-per-pair |

## D0025 -- 3 members over go, go, swift

| language | label | arity |
| --- | --- | --- |
| go | `>>` | binary |
| go | `>>=` | assignment |
| swift | `>>` | binary |

- classes spanned (9): A0622, A0623, A0624, A0625, A0626, A0627, A0628, A0629, A0630
- classes any member touches: 17
- strongest evidence over the member pairs: z3
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: z3
- surviving edges: 2
  - N0123--N0192: 1 shared classes, 1 shared operand-type keys
  - N0124--N0192: 1 shared classes, 1 shared operand-type keys
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
| N0123--N0124 | 9 | not-recorded-per-pair | not-recorded-per-pair |
| N0123--N0192 | 1 | z3 | z3 |
| N0124--N0192 | 1 | not-recorded-per-pair | not-recorded-per-pair |

## D0026 -- 3 members over go, rust, swift

| language | label | arity |
| --- | --- | --- |
| go | `\|\|` | binary |
| rust | `\|\|` | binary |
| swift | `\|\|` | binary |

- classes spanned (1): A0159
- classes any member touches: 1
- strongest evidence over the member pairs: byte
- weakest over the member pairs: anchored sem identity (the two lifted forms are identical)
- weakest the class table itself recorded on the spanned classes: sem
- surviving edges: 3
  - N0130--N0166: 1 shared classes, 1 shared operand-type keys
  - N0130--N0196: 1 shared classes, 1 shared operand-type keys
  - N0166--N0196: 1 shared classes, 1 shared operand-type keys
- bridges: 0
- fences: 0
- languages absent:
  - c: no mutual counterpart: the language has units in these classes, but no node of it was chosen back
  - cpp: no mutual counterpart: the language has units in these classes, but no node of it was chosen back
  - java: refused by the type checker, or measured and never equal: no accepted unit of this language sits in any class this dominant operator spans
- intention: null; hint proposed only, the owner settles

evidence trail, member pair by member pair:

| pair | unit pairs | strongest | weakest |
| --- | --- | --- | --- |
| N0130--N0166 | 1 | sem | sem |
| N0130--N0196 | 1 | sem | sem |
| N0166--N0196 | 1 | byte | byte |

## D0027 -- 2 members over c, cpp

| language | label | arity |
| --- | --- | --- |
| c | `%` | binary |
| cpp | `%` | binary |

- classes spanned (16): A0108, A0111, A0112, A0113, A0115, A0116, A0117, A0118, A0119, K0266, K0267, K0272, K0278, K0279, K0280, K0281
- classes any member touches: 16
- strongest evidence over the member pairs: byte
- weakest over the member pairs: byte identity (the two units are the same machine bytes)
- weakest the class table itself recorded on the spanned classes: byte
- surviving edges: 1
  - N0003--N0046: 16 shared classes, 16 shared operand-type keys
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
| N0003--N0046 | 16 | byte | byte |

## D0028 -- 2 members over c, cpp

| language | label | arity |
| --- | --- | --- |
| c | `%=` | assignment |
| cpp | `%=` | assignment |

- classes spanned (16): A0108, A0109, A0110, A0111, A0112, A0113, A0114, A0115, A0116, A0117, A0118, A0119, A0120, A0121, A0122, A0123
- classes any member touches: 16
- strongest evidence over the member pairs: not-recorded-per-pair
- weakest over the member pairs: verdicts3b records no ground for this unit pair.  That is a limit of the pair record, not a weak edge: the class this pair sits in was formed by canonical-byte identity or by a z3 edge, and those grounds are recorded on the CLASS, not on the pair.  Read `weakest_evidence_from_the_class_table` beside this.
- weakest the class table itself recorded on the spanned classes: byte
- surviving edges: 1
  - N0004--N0047: 16 shared classes, 16 shared operand-type keys
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
| N0004--N0047 | 16 | not-recorded-per-pair | not-recorded-per-pair |

## D0029 -- 2 members over c, cpp

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
  - N0006--N0049: 6 shared classes, 6 shared operand-type keys
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
| N0006--N0049 | 6 | byte | byte |

## D0030 -- 2 members over c, cpp

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
  - N0014--N0057: 5 shared classes, 5 shared operand-type keys
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
| N0014--N0057 | 5 | byte | byte |

