Compiled languages only, since the four interpreted ones have no operator corpus yet.

**Table 1.** A compiler-operator counts if at least one of its arch-units lowers to one arch opcode after the calling-convention moves and `ret`.

| language | compiler-operators lowering to one arch opcode | of operators offered |
| -------- | ---------------------------------------------- | -------------------- |
| c        | 20                                             | 27                   |
| cpp      | 26                                             | 32                   |
| rust     | 14                                             | 21                   |
| go       | 10                                             | 20                   |
| swift    | 12                                             | 26                   |

**Table 2.** Distinct arch opcodes across all of the language's arch-units, wrapper opcodes included.

| language | distinct arch opcodes |
| -------- | --------------------- |
| c        | 127                   |
| cpp      | 130                   |
| rust     | 72                    |
| go       | 60                    |
| swift    | 96                    |



**Argument types per language.** Two populations exist, and the count differs by which one you mean:

| language | original probes, hand-written holders | regenerated probes, the compiler's own scalar core |
| -------- | ------------------------------------- | -------------------------------------------------- |
| c        | 6                                     | 56                                                 |
| cpp      | 6                                     | 56                                                 |
| go       | 6                                     | 14                                                 |
| rust     | 6                                     | 15                                                 |
| swift    | 6                                     | 17                                                 |


