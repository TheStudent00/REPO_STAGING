# log 178 — task 69: pane 1 completed — context, rendered back, verdicts, interpreter source

Nodes: `hq.research.compiler_graph.dashboard`
(`Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_10_dashboard/CORE_0_3_5_10_dashboard.md`)
and `hq.research.compiler_graph.arch_unit.context`
(`.../node_0_3_5_1_arch_unit/node_0_3_5_1_6_context/CORE_0_3_5_1_6_context.md`).
Brief: log_172 task 69. Date: 2026-09-03.

# 1. What was done, in plain words, before any figure

The unit viewer had seven modes. It has eleven. The four new ones are in
one new file, `Research/op_pipeline/dashboard_pane1.js`, so that the two
other agents working on the same page this round never touch the same
lines: `dashboard.html` gained one script tag, `dashboard_join.js` gained
three small hooks, `viewer_build.py` gained one embed block.

The work behind the modes is one measurement and one join.

- **The measurement.** A compiled body often names a constant it needs
  without carrying it: it says "the thing sixteen bytes further along
  from here". Until today the constant's BYTES were written down nowhere,
  so a unit that needs one was not fully recorded. They are written down
  now, in a new sidecar `canon39_context.json`, for **300 of the 329
  units that reach something that way** — the other 29 are each named
  with the reason there is nothing to write.
- **The join.** The verdicts, both proof routes, the reasons, the
  counterexamples and the rendered-back text already existed in the
  stores; nothing on the page showed them. Each mode now opens the store
  file for the unit that was clicked, and says at the top what it counted
  and when.

# 2. The context measurement, with values in motion

## 2.1 The thing being measured, named first

`c/op_15` is the c probe for negating a 32-bit float — the source in the
probe manifest is `return -a;`. Its whole ship body, LITERAL, as
`canon39_wrapped_c.json` records it:

```
body_text : xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4; ret
body_bytes: 0f 57 05 00 00 00 00 c3
```

GLOSS, term by term:

- `%rip` is the instruction pointer — the address of the next
  instruction. `0x0(%rip)` means "the memory at the instruction pointer
  plus zero"; the zero is a placeholder the linker fills in.
- `!!reloc=R_X86_64_PC32:.LCPI0_0-0x4` is the relocation the compiler
  emitted beside it: the placeholder is to be filled so the address lands
  on the symbol `.LCPI0_0`.
- So the body says: read sixteen bytes from wherever `.LCPI0_0` ends up,
  and exclusive-or them into the argument.

What the sixteen bytes ARE is the whole computation: nothing else in the
unit says this is a negation. Before today they were stored nowhere.

## 2.2 Reading them, step by step, with the actual values

1. **The probe source is read back out of the manifest** —
   `probe_manifest_c.json`, probe 15 (the regenerated population is read
   out of `probe_manifest2_<lang>.json`).
2. **The lane's own ship build is repeated**, with the flags
   `lanes/op_asg_c.sh` states in its `compile_probe`
   (`clang -std=c17 -O1 -c`; rust `rustc --crate-type=lib --emit=obj -C
   opt-level=1 -C debug-assertions=off`; go `go build`).
3. **The rebuilt body is compared with the recorded body.** objdump's own
   byte column, flattened:

   ```
   $ objdump -dr --disassemble=op_15 unit_ship.o
   0000000000000000 <op_15>:
      0:	0f 57 05 00 00 00 00 	xorps  0x0(%rip),%xmm0        # 7 <op_15+0x7>
   			3: R_X86_64_PC32	.LCPI0_0-0x4
      7:	c3                   	ret
   ```

   `0f 57 05 00 00 00 00 c3` — the same eight bytes the unit records.
   **A unit whose rebuild does not match is refused**; its constant is
   never written down on a guess.
4. **The symbol is located, by the tools' own printing.**

   ```
   $ readelf -sW unit_ship.o | grep LCPI
        3: 0000000000000000     0 NOTYPE  LOCAL  DEFAULT    4 .LCPI0_0
   $ readelf -SW unit_ship.o
     [ 4] .rodata.cst16     PROGBITS  0000000000000000 000050 000010 10  AM
   ```

   `.LCPI0_0` sits at offset 0 of section 4, and section 4 is 0x10 = 16
   bytes long with no later symbol in it, so the constant is 16 bytes
   wide. The width is measured, not assumed from a table.
5. **The bytes are read.**

   ```
   $ objdump -s -j .rodata.cst16 unit_ship.o
   Contents of section .rodata.cst16:
    0000 00000080 00000080 00000080 00000080  ................
   ```

6. **What is stored**, in `canon39_context.json`, keyed by unit id:

   ```json
   "c/op_15": {
    "context": [{"symbol": ".LCPI0_0",
                 "bytes": "00 00 00 80 00 00 00 80 00 00 00 80 00 00 00 80",
                 "width": 16, "section": ".rodata.cst16",
                 "site": "xorps 0x0(%rip),%xmm0 !!reloc=R_X86_64_PC32:.LCPI0_0-0x4",
                 "read_with": "readelf -sW + objdump -s -j .rodata.cst16"}],
    "sites": 1, "rebuilt_body_bytes_match_the_record": true
   }
   ```

   GLOSS: `00 00 00 80` little-endian is `0x80000000` — the sign bit of a
   32-bit float, alone, repeated four times across the 16-byte vector.
   Exclusive-or with it flips the sign. The negation is now readable off
   the record.

## 2.3 Evidence class

**Forced by construction**, resting on the one assumption the whole line
already rests on (the compiler compiled the program we wrote), plus one
step of the tool's own testimony (objdump/readelf printing their own
object). The byte comparison at step 3 is what forces it: a rebuild that
is not the same code is thrown away rather than reported.

# 3. The population, computed, and every unit that got nothing

## 3.1 The population line

Computed over the whole corpus — 31,078 units, the five compiled
languages plus the 11 interpreter units — by walking
`canon39_wrapped_<lang>.json`, `canon39_interp.json` and the 326 shards
of `canon39_regen_store/`:

- **329 units** have a body that reaches something at an offset from the
  instruction pointer, over **524 sites**.
- **300 of the 329 have their bytes**; **29 do not**.

Per language:

| language | units reaching rip-relative | bytes read | no bytes |
|---|---:|---:|---:|
| c | 121 | 121 | 0 |
| cpp | 141 | 141 | 0 |
| go | 24 | 4 | 20 |
| rust | 38 | 34 | 4 |
| swift | 5 | 0 | 5 |
| **total** | **329** | **300** | **29** |

A note on a near-miss figure, because it is easy to mis-read: 4,771
units carry the string `reloc` in their body text. That is a larger
population and a different one — most of those relocations are on
`call` lines, naming a routine rather than a constant. The 329 counted
here are the bodies with `(%rip)` in them.

## 3.2 Every one of the 29, by cause

- **20 go units — the site takes an address, it reads no value.**
  `go/op_30`, `op_31`, `op_32`, `op_33`, `op_34`, `op_35`,
  `regen_52` … `regen_65`. Their site is a `lea` — "load effective
  address" — feeding `runtime.newobject`:

  ```
  lea 0x6d27(%rip),%rax; call 41a7a0 <runtime.newobject>
  ```

  GLOSS: the body is handing the allocator a pointer to a type
  descriptor. Nothing is read through the pointer inside the unit, so
  there is no constant of a stated width to store. The rebuild matched
  the recorded bytes for all 20; this is a fact about the site, not a
  failure of the route.
- **5 swift units — the ship build cannot be repeated on this machine.**
  `swift/op_15`, `op_16`, `regen_34`, `regen_35`, `regen_36`. The lane
  built swift with `/persist/swift/usr/bin/swiftc` inside the Airlock
  image; `swiftc` is not installed on the host (`command -v swiftc` finds
  nothing). Fixable by rebuilding these five inside Airlock; not done
  this lap, and the page says so rather than showing a blank.
- **4 rust units — the site reaches a routine, not a constant.**
  `rust/op_699` and `regen_1079` reach `fmodf`; `rust/op_706` and
  `regen_1080` reach `fmod`. `readelf` reports both as section index
  `UND`: an undefined symbol the linker will resolve to a routine. A
  routine is the `callees` part of the context record, not
  `rip_constants`.

## 3.3 What this closes on the `context` node

`ArchUnit.context.rip_constants` is the CORE's first attribute and its
realization row said "the round-6 context record, carried on the unit"
with no bytes anywhere. The bytes now exist, per unit, in a sidecar —
**no `canon39_*` file was edited**, as the brief required. PROGRESS on
the node is written with this log as its evidence link.

# 4. The three other modes

## 4.1 Rendered back, beside the wrapped text

Screenshot: `DevComms/screens/log_178/pane1_p1rendered_c_op_101.png`.

Population line the mode prints, read live out of `render_back_tally.json`:

> rendered back: 5,909 of 26,040 units with a proved term have a rendered
> text; 5,909 assembled, 5,909 round-tripped through objdump, 0
> character-identical to the wrapped text.

For `c/op_101`, the two texts side by side, LITERAL from
`render_back_store/canon39_wrapped_c.json`:

| the wrapped text | the rendered text |
|---|---|
| `mov ledger+0x00(%rip),%rdi` | `mov ledger+0x00(%rip),%rdi` |
| `mov 0x0(%rdi),%rdi` | `mov 0x0(%rdi),%rdi` |
| | `mov %rdi,%r11` |
| `mov %edi,%eax` | `mov %r11d,%eax` |
| `mov ledger+0x38(%rip),%r11` | `mov ledger+0x38(%rip),%r11` |
| `mov %eax,0x0(%r11)` | `mov %eax,0x0(%r11)` |
| `ret` | `ret` |

GLOSS: the return path re-derived the same computation and parked the
value in `%r11` on the way — that one extra step is the whole of why
`character_identical_to_layer_3` is false here, and why it is false for
all 5,909. The mode shows the difference rather than asserting a verdict
about it.

## 4.2 Verdicts, both routes, with the counterexample

Screenshots: `pane1_p1verdicts_c_op_15.png` (one route, proved) and
`pane1_p1verdicts_c_op_117_counterexample.png` (two routes, disproved).

Population line, read out of `audit65.json`:

> verdicts: 30,432 units carry a record; 26,594 proved, 3,134 disproved,
> 285 undecided, 419 with no term.

For `c/op_117` the mode shows, LITERAL from `term65_store`:

| route | outcome | solver ceiling, ms |
|---|---|---:|
| the term against the unit's own ship body | DISPROVED | 3,000 |
| the term against the body walked in text order | UNDECIDED | 3,000 |

with both reason strings, the hole table (`GUARD-0`, line `js L0`), and
the counterexample:

```
[seed_xmm0 = 1596703311,
 seed_rdi = 7734352952421377967,
 fp.to_ieee_bv = [else -> fp.to_ieee_bv(Var(0))]]
```

Measured over the whole store while building this: **3,134 units carry a
counterexample, exactly the disproved population**; 3,419 carry a second
route (`verdict_text`), which is only run where the first did not prove.

## 4.3 The interpreter units

Screenshots: `pane1_p1interp_cpython.png` and
`pane1_p1interp_php_no_source.png`.

Population line, read out of the new sidecar `canon39_interp_source.json`:

> interpreter units: 11 in the corpus; 1 carry the handler's C source, 10
> have no source recorded.

- **1 with source: `cpython/long_add_fastpath`.** Its C source is in
  `interp_cpython.json`, from the gcov-instrumented build, and the mode
  prints it with its line numbers, LITERAL:

  ```
  3738  long_add(PyLongObject *a, PyLongObject *b)
  3740      if (_PyLong_BothAreCompact(a, b)) {
  3741          stwodigits z = medium_value(a) + medium_value(b);
  3742          return _PyLong_FromSTwoDigits(z);
  ```

  with its evidence class carried on the page: "tally (gcov line
  counters, per-run, order lost)".
- **10 with none, each with its cause on the page**: `java/op_1`,
  `java/op_2`, `php/add_function`, the three `php/ZEND_ADD_*` handlers,
  `ruby/rb_big_plus`, `ruby/rb_fix_plus`, `ruby/rb_int_plus`,
  `ruby/vm_opt_plus`. The cause the sidecar writes is the mechanical one:
  no artifact of the searched set carries a C line whose enclosing
  definition is that handler. The searched set is written into the
  sidecar's own `meta.searched`, so the scope of the search is on the
  page and not in an agent's memory.

# 5. THE SPELLING BAN, applied, and run rather than asserted

> THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
> second violation). No operator token may appear in ANY key, grouping,
> pairing, row structure, candidate selection, or comparison scope,
> anywhere in this line — not in matching, not in "which pairs get
> compared", not in report rows, not in dropdowns. The candidate set for
> comparison comes from machine-form evidence (clusters, connections,
> type pairs) or from ratified intention — never from the token. The
> token appears exactly once per unit: as a display label on the member.
> HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
> campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
> verdicts.py's row pairing (caught by the owner 2026-08-25 — the fix brief
> itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
> REQUIRED: every pipeline stage that groups or pairs units must run the
> spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
> its own output on failure. A brief handed to any subagent for this line
> MUST paste this paragraph verbatim.

## 5.1 How this work obeys it

Every key written this lap is a unit id (`c/op_15`), a file name
(`canon39_context.json`), a symbol the linker minted (`.LCPI0_0`), or a
machine-form field name (`width`, `section`, `sites`). Nothing groups,
pairs or compares. The two sidecars carry no operator field at all.

## 5.2 The guards, unmodified, one process each

```
$ git status --porcelain Research/op_pipeline/check_no_spelling_keys.py \
      Research/op_pipeline/check_dashboard_js_no_spelling.py
(no output: both unmodified)

$ /tmp/reconnect_venv/bin/python3 check_no_spelling_keys.py \
      canon39_context.json canon39_interp_source.json
operator inventory: 91 tokens read from probe_manifest_*.json
PASS canon39_context.json -- no operator token in any key, grouping, pairing or row structure
PASS canon39_interp_source.json -- no operator token in any key, grouping, pairing or row structure
exit=0

$ /tmp/reconnect_venv/bin/python3 check_dashboard_js_no_spelling.py \
      dashboard_pane1.js dashboard_pane1_harness.html
operator inventory: 91 tokens read from probe_manifest_*.json
     dashboard_pane1.js:118  '&' -- html escaping in esc()
     dashboard_pane1.js:121  '<' -- html escaping in esc()
PASS dashboard_pane1.js -- no operator token is written as a literal, so none can be a key (2 named coincidences above)
PASS dashboard_pane1_harness.html -- no operator token is written as a literal, so none can be a key (0 named coincidences above)
exit=0

$ grep -c exempt <both transcripts>
0
0
```

- **LITERAL:** the two flagged literals are `&` and `<` in this file's own
  HTML escaper.
- **GLOSS:** a key can only be written as a literal, so no literal means
  no key.

## 5.3 The glyph test, run

`?labels=glyph` replaces every operator label with `◆`. With it on, the
DOM of the verdicts mode reads:

```
c/op_15 operator ◆ signature (a: float) -> 64-bit arrival plain
population original PROVED_ON_SHIP … verdicts: 30,432 units carry a
record; 26,594 proved, 3,134 disproved, 285 undecided, 419 with no
term. … state TERM outcome PROVED_ON_SHIP proved true …
```

Screenshot: `DevComms/screens/log_178/pane1_glyph_test_context.png`.
Nothing in the four new modes reads the label, and all four still draw.

# 6. How it was verified in a browser, and the one step that is not

The live page's folder dialog belongs to the operating system and cannot
be clicked by any automation here — the limit log_176 §4.3 recorded. The
same rig is used: `dashboard_test_server.py` serves the folder over http
with byte ranges and `dashboard_test_shim.js` dresses those fetches as
directory handles. One new TEST RIG file was added,
`dashboard_pane1_harness.html` — a copy of `dashboard_test_harness.html`
that also loads `dashboard_pane1.js` and accepts a `filter=` parameter,
so a unit outside the first 600 rows (every interpreter unit) can be
reached by a script. `dashboard_join.js`, `dashboard_loader.js` and
`dashboard_pane1.js` run UNCHANGED against it.

The page's own console lines from those runs:

```
[dashboard] FIRST PAINT 601 ms after the folder was granted. 31,078 units counted from 336 summary reads.
[dashboard] INDEX COMPLETE 3949 ms after the folder was granted; 31,078 units, 162 arch opcodes.
[dashboard] harness ready
```

Screenshots, all under `DevComms/screens/log_178/` (9 files):

| file | what it shows |
|---|---|
| `pane1_p1context_c_op_15.png` | context mode, `.LCPI0_0` = `00 00 00 80 …`, the population line |
| `pane1_p1context_go_op_10.png` | context mode on go, the constant read out of the linked binary's `.rodata` at `0x497c28` |
| `pane1_p1context_go_op_30_no_bytes.png` | the `lea` cause, stated on the page |
| `pane1_p1context_swift_no_bytes.png` | the swiftc cause, stated on the page |
| `pane1_p1rendered_c_op_101.png` | rendered text beside wrapped text, with the verdict |
| `pane1_p1verdicts_c_op_15.png` | one route, proved |
| `pane1_p1verdicts_c_op_117_counterexample.png` | both routes, reasons, counterexample, hole table |
| `pane1_p1interp_cpython.png` | the handler's C source with line numbers |
| `pane1_p1interp_php_no_source.png` | "no source recorded", with the cause |

The snapshot build was re-run and checked too:

```
$ /tmp/reconnect_venv/bin/python3 viewer_build.py
operator inventory: 91 tokens read from probe_manifest_*.json
PASS dashboard_snapshot_data.json -- no operator token in any key, grouping, pairing or row structure
wrote …/dashboard_snapshot.html  (19.7 MB, 2456 unit bodies carried, 31078 units counted, 1019 files read)
the join embedded above is dashboard_join.js, verbatim (43902 bytes)
panes 2 and 3 embedded verbatim from dashboard_pane23.js (32158 bytes), before the snapshot script
pane 1's modes embedded verbatim from dashboard_pane1.js (15373 bytes), before the snapshot script
pane 6 embedded verbatim from dashboard_pane6.js (15891 bytes) with chronology.json (56904 bytes)
```

and the embedded copy is the file, byte for byte:

```
$ diff <(the pane-1 block extracted from dashboard_snapshot.html) dashboard_pane1.js
(no output: identical)
$ sha256sum embedded_pane1.js dashboard_pane1.js
40b46c94464c528b39b7e43013e087981700793055aa19188a8770e0a890c150  embedded_pane1.js
40b46c94464c528b39b7e43013e087981700793055aa19188a8770e0a890c150  dashboard_pane1.js
```

In the snapshot the four modes are present and say the true thing, driven
in a real browser tab:

```
> document.querySelector('div[data-id="c/op_100"]').click();
  document.querySelector('.modes button[data-m="p1verdicts"]').click();
  document.querySelector('#upane').innerText
"… context / rendered back, beside the wrapped / verdicts / interpreter
 handler source

 this mode reads a file on disk when the unit is opened, so it needs the
 live page; the snapshot carries no folder to read."
```

**The one step still not driven end to end** is the same one log_176
named: the click inside the operating system's folder dialog.

# 7. The three files that are shared, and exactly what each gained

Two other agents were editing the page at the same time, so every edit
outside the new module is additive and was made against the file as it
stood at that moment.

- **`dashboard.html`** — one line:

  ```html
  <script src="dashboard_pane1.js"></script>
  ```

- **`dashboard_join.js`** — three hooks, 18 lines, nothing rewritten
  (`git diff --stat` at the time of the edit: `18 ++++++++++`):

  ```js
  672:    if (typeof window !== "undefined" && window.DashboardPane1) {
  673:      MODES = MODES.concat(window.DashboardPane1.modes);
  742:      if (typeof window !== "undefined" && window.DashboardPane1) {
  743:        var extra = window.DashboardPane1.body(u, state.mode);
  799:        if (u && typeof window !== "undefined" && window.DashboardPane1) {
  800:          return window.DashboardPane1.enrich(source, u);
  ```

  GLOSS: the first appends the four modes to the mode row; the second
  lets this module draw a mode the join does not know; the third gives
  it one step to read its files before the unit is drawn. With the module
  absent, all three are skipped and the page is exactly what it was.
- **`viewer_build.py`** — one embed block at the same seam panes 2 and 3
  use (24 lines added), plus the build line that names it.

# 8. Complete file inventory

New:

| bytes | file | what |
|---|---|---|
| 15,385 | `Research/op_pipeline/dashboard_pane1.js` | the four modes; all of pane 1's new code |
| 17,582 | `Research/op_pipeline/context.py` | reads the constants' bytes; writes the sidecar |
| 5,738 | `Research/op_pipeline/unit_viewer_interp_source.py` | joins the interpreter handlers to a recorded C source |
| 239,275 | `Research/op_pipeline/canon39_context.json` | the sidecar: 329 units, 524 sites, 300 with bytes |
| 5,705 | `Research/op_pipeline/canon39_interp_source.json` | the sidecar: 11 interpreter units, 1 with source |
| 81,966 / 97,022 / 9,186 / 45,906 / 1,123 | `canon39_context_part_{c,cpp,go,rust,swift}.json` | the per-language parts `context.py --join` reads |
| 3,655 | `Research/op_pipeline/dashboard_pane1_harness.html` | TEST RIG ONLY — the unchanged loader plus this module |
| — | `DevComms/screens/log_178/*.png` | 9 screenshots, listed in section 6 |
| — | `DevComms/log_178_task69_pane1_context_verdicts.md` | this file |

Changed, each additively and each re-read immediately before the edit:

| file | what changed |
|---|---|
| `Research/op_pipeline/dashboard.html` | one `<script>` line |
| `Research/op_pipeline/dashboard_join.js` | three hooks, 18 lines |
| `Research/op_pipeline/viewer_build.py` | one embed block, 24 lines |
| `Research/op_pipeline/dashboard_snapshot.html` | rebuilt (19.7 MB) |

Plan tree:

- `Planning/…/node_0_3_5_1_arch_unit/node_0_3_5_1_6_context/PROGRESS.md` —
  two entries: the bytes with their population and their 29 named
  exceptions, and the guard.
- `Planning/…/node_0_3_5_10_dashboard/PROGRESS.md` — three entries: the
  four modes with their populations, the additive edits, the glyph test
  and the guards.

Unmodified, and checked to be: `check_no_spelling_keys.py`,
`check_dashboard_js_no_spelling.py` (section 5.2).

# 9. Two lists

**Decided, recorded for audit.**

- The constant's WIDTH is measured from the symbol's extent in its own
  section (next symbol, or the section's end), not from a table of
  instruction access sizes. The table is used only for go, whose linked
  binary has no local symbol at the site.
- A rebuild whose bytes differ from the recorded body is refused rather
  than reported as the unit's constant. Zero units are in that state
  today.
- `go`'s 20 `lea` sites are recorded as sites with no value read, not as
  failures. They are addresses handed to the allocator.
- The interpreter join searches a declared list of ten artifacts, written
  into the sidecar's `meta.searched`, and matches a row to a handler by
  the row's enclosing definition. It is not hand-wired per unit.
- `dashboard_pane1_harness.html` is a measurement rig, named as one in
  its own first lines; no dashboard file references it.

**Awaiting the owner.**

- Nothing. The 5 swift units without their constants need a swiftc that
  exists only inside the Airlock image; that is a scheduling matter for
  the next lap, not a question — it is written on the page and in the
  node's PROGRESS.
