# interp_ruby_handlers -- ruby handler slices (task 12, 2026-09-01)

Extends `interp_ruby.md`/`interp_ruby.json` (round 1, dispatch/tally only,
no arch-unit) with what that pilot named as not done: anchor and ship
builds of ruby 3.3.0, an objdump slice of the handler chain for `+`,
and instruction counts.  Does for ruby what `interp_cpython.md` did for
CPython.  Data: `interp_ruby_handlers.json`.

## the pin

- ruby `3.3.0` -- same pin as `interp_ruby.json`, quoted from that
  artifact's own `meta.pin.tag`, not re-typed from memory.
- source: `/persist/ruby-3.3.0.tar.gz` extracted once already at
  `/persist/ruby` (the round-1 coverage build's own source tree, used
  here as the pristine source for a fresh anchor build and a fresh
  ship build -- both start from `make distclean` in a copy of that
  tree, so no coverage instrumentation carries over).
- evidence class: artifact fact (the binaries' own `nm` output, the
  `__gcov` symbol count is 0 on both -- see guard below).

## the two builds

| build | configure | CFLAGS |
|---|---|---|
| anchor | `./configure CFLAGS="-O0 -g -fwrapv"` | optimizer off |
| ship | `./configure` (bare -- ruby's own default OPT) | optimized |

Both start from `make distclean` in a fresh copy of the coverage
build's source tree (`/persist/ruby`), so neither carries `--coverage`
forward.  Confirmed, not assumed: `nm ruby | grep -c __gcov` is `0` on
both `/persist/ruby_anchor/ruby` and `/persist/ruby_ship/ruby`.

## the four handler symbols

Located by source grep, then confirmed present with `nm -C --defined-only`
on both binaries (full listing in `interp_ruby_handlers.json`'s
sibling `ruby_nm.txt` product):

- `vm_opt_plus` (`vm_insnhelper.c`) -- the C function behind the
  `opt_plus` bytecode instruction (round 1's bytecode listing named
  this instruction; this pilot names the C function under it).
- `rb_fix_plus` / `fix_plus` (`numeric.c`) -- the Fixnum+Fixnum route.
- `rb_int_plus` (`numeric.c`) -- the type-dispatch layer above both.
- `rb_big_plus` (`bignum.c`) -- the Bignum+Bignum route.

## the anchor dispatch chain, pasted (rb_int_plus, -O0)

```
00000000000fedda <rb_int_plus>:
   fedda: endbr64
   feddf: push   rbp
   ...
   fedf5: call   f6fe7 <RB_FIXNUM_P>
   fedfa: test   al,al
   fedfc: je     fee13 <rb_int_plus+0x39>
   ...
   fee0c: call   fecb8 <fix_plus>
   fee11: jmp    fee55 <rb_int_plus+0x7b>
   fee13: ...
   fee1f: call   f7484 <RB_TYPE_P>
   fee24: test   al,al
   fee26: je     fee3d <rb_int_plus+0x63>
   ...
   fee36: call   3cfaa9 <rb_big_plus>
   fee3b: jmp    fee55 <rb_int_plus+0x7b>
   fee3d: ...
   fee50: call   f9158 <rb_num_coerce_bin>
   fee55: leave
   fee56: ret
```

Read off the bytes, not asserted: `rb_int_plus` checks
`RB_FIXNUM_P` first -> `fix_plus` on the Fixnum branch, else
`RB_TYPE_P(..., T_BIGNUM)` -> `rb_big_plus` on the Bignum branch,
else `rb_num_coerce_bin` (the generic coercion fallback -- the same
role as CPython's `PyNumber_Add`).  This MATCHES the type-pair
structure round 1's tally measured (Fixnum path light, Bignum path
heavy on `bignum.c`/`gc.c`), now shown as the actual dispatch code
rather than inferred from line counts.

## instruction counts (anchor -O0 vs ship optimized)

| symbol | anchor | ship | note |
|---|---|---|---|
| `vm_opt_plus` | 165 | 0 | **absorbed** at ship: no standalone body, confirmed by an empty `.text` disassembly for that symbol (objdump found no matching range) |
| `rb_fix_plus` | 13 | 136 | at ship, `fix_plus`'s tagged-int overflow-check body is INLINED into `rb_fix_plus` rather than called -- the call at anchor (`call fecb8 <fix_plus>`) is gone at ship |
| `rb_int_plus` | 37 | 201 | same inlining pattern: the anchor's three `call` sites collapse into inlined checks at ship |
| `rb_big_plus` | 85 | 146 | grows at ship too (loop unrolling / inlined `RB_FIXNUM_P`/`BIGNUM_SIGN` calls), but keeps a standalone symbol (never absorbed) |

This is the SAME "absorbed at ship, no separate address range" finding
`interp_cpython.md` recorded for `_PyLong_FromSTwoDigits` and
`long_normalize` -- here it happens to the whole `vm_opt_plus`
dispatcher, not a leaf helper.  Frontier, named rather than chased:
this pilot did not locate WHERE `vm_opt_plus`'s logic actually lives
at ship (presumably inlined into `vm_exec_core`'s computed-goto body,
the same frontier CPython's pilot left for `_PyEval_EvalFrameDefault`).

## evidence classes

- pin, instruction bytes and counts -- **artifact fact**.
- the anchor dispatch chain (`RB_FIXNUM_P` -> `fix_plus` /
  `RB_TYPE_P` -> `rb_big_plus` / else `rb_num_coerce_bin`) -- **artifact
  fact**, read directly off the disassembled `call` targets, not
  inferred from source.
- "ship inlines `fix_plus` into `rb_fix_plus`" -- **interpretation** of
  the instruction-count growth and the disappearance of the `call`
  site; no DWARF inlining record was consulted.

## what was NOT done

- No diary; order still unmeasured (same caveat as `interp_ruby.md`).
- No normalization to the canonical runnable form, no matching against
  the compiled-language dom_ops units, no bridge or dominance claim.
- `vm_opt_plus`'s ship-build logic was not chased into its absorbing
  caller.
- Scope unchanged from round 1: x86-64, gcc 15.2.0, ruby 3.3.0,
  Fixnum and Bignum operands, one operator (`+`).

## THE OPEN QUESTION (stated, not answered -- the owner's ontology call)

Do these four handler slices belong in the operator table at all, or
do they join through bridges/dominance, the way `SUPPORT_scaling_design.md`
predicted for python's arbitrary-precision `+`?  Evidence both ways:

- FOR joining directly: `rb_fix_plus`'s Fixnum-Fixnum small-value path
  (13 anchor instructions, a tagged-int add with an overflow check) is
  structurally close to the compiled-language `dom_ops` cores -- a
  bounded-width add with a branch, the same shape as C's `+` on `int`.
- AGAINST: `rb_big_plus` (Bignum path) is unbounded-width, matching
  `SUPPORT_scaling_design.md`'s prediction that this joins only through
  BRIDGES and DOMINANCE (fixed-width projection agrees; overflow-to-
  growth is `rb_big_plus`'s mode), not byte identity.
- `vm_opt_plus` itself is a DISPATCH function (inline-cache check +
  branch to one of `rb_fix_plus`/`rb_ary_plus`/generic), not a
  computation core at all -- structurally closer to a JIT's type-guard
  than to a `dom_ops` member.

Per the round-2 STOP RULE: this is presented as evidence both ways,
not decided here.

## provenance

`provenance_is_weaker: true` on every row here, same convention as
java's interpreter rows: the handler was located by source grep plus
`nm`, not by a probe-generator/tree-sitter pipeline; the anchor/ship
identity is a build convention (distinct `configure` invocations)
rather than the DWARF-anchored name->memory-home method the compiled-
language track uses.

## guard

```
$ python3 check_no_spelling_keys.py interp_ruby_handlers.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS interp_ruby_handlers.json -- no operator token in any key, grouping, pairing or row structure
```

## the lane

`interp_e2_handlers.sh` (Airlock, batch `task12-handlers`) -- 150.8s,
exit 0.  Built ruby anchor and ship from `/persist/ruby` (`make
distclean` + reconfigure each), confirmed zero `__gcov` symbols on
both, sliced four symbols with `objdump -d --disassemble=<sym> -M
intel`.  Full symbol tables at Airlock `agent/out/ruby_nm.txt`; raw
disassembly at `agent/out/asm/ruby_{anchor,ship}_<symbol>.txt`.
