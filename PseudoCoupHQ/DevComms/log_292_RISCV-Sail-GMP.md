72 is what Sail's whole runtime can call, across printing, tracing, rationals and string parsing. One instruction reaches a handful. Let me trace DIV exactly.

Confirmed at `longlong.h:2200`: *"If udiv_qrnnd was not defined for this processor, use `__udiv_qrnnd_c`"*, then `#define udiv_qrnnd __udiv_qrnnd_c`.

And RISC-V has no `udiv_qrnnd`. Its only entry in `longlong.h` is a wide multiply using `mulhu`. So on RISC-V, **GMP's divide is pure C** and never reaches a divide instruction.

**The complete path for one `DIV`, every file named:**

```
execute DIV                                  model/extensions/M/mext_insts.sail:53

├─ signed(rs1_bits), signed(rs2_bits)        sail.c  sail_signed
│    ├─ mpz_set                              mpz/set.c
│    ├─ mpz_tstbit                           mpz/tstbit.c
│    ├─ mpz_set_ui                           mpz/set_ui.c
│    ├─ mpz_mul_2exp                         mpz/mul_2exp.c
│    ├─ mpz_combit                           mpz/combit.c
│    └─ mpz_sub                              mpz/aors.h
│
├─ quot_round_zero(a, b)                     sail.c  tdiv_int
│    └─ mpz_tdiv_q                           mpz/tdiv_q.c
│         └─ mpn_div_q                       mpn/generic/div_q.c     dn == 1
│              └─ mpn_divrem_1               mpn/generic/divrem_1.c
│                   └─ udiv_qrnnd            longlong.h:2203
│                        = __udiv_qrnnd_c    longlong.h:2147   pure C on RISC-V
│
└─ to_bits_truncate(quotient)                sail.c  get_slice_int
     ├─ mpz_get_ui                           gmp.h macro
     ├─ mpz_set_ui                           mpz/set_ui.c
     ├─ mpz_tstbit                           mpz/tstbit.c
     └─ mpz_setbit                           mpz/setbit.c
```

**Eleven GMP files, not 72.** Nine in `mpz/`, two in `mpn/generic/`, plus `longlong.h`. The other 61 entry points are printing, rationals, string parsing and features RISC-V never enters.

And the bottom is the macro I showed you earlier: two rounds of schoolbook long division on half-limbs, built from `/`, `*`, `-`, `|`, `<<`, `>>` and a compare-and-fixup, with `__q1--` and `__r1 += d` correcting an overestimate. That is the entire logic of a 64-bit divide as the emulator computes it.

So your route works, and on RISC-V it is cleaner than I said: no host divide instruction to get stuck on. The trace lands on ordinary C operators all the way down.
