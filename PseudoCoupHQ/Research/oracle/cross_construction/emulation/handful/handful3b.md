# handful3b.md -- task g1b: task g1's forty runs again, on the rebuilt image, with a swift compiler reachable

The same ten cells of the arch-opcode model table tasks h1 and h2 ran, on four targets (c, rust, go and swift) and by a route that is tried before the term route: does the target have an OPERATOR whose whole lowered body IS this cell? Where it does, that operator on holders of the operand types the corpus recorded is what is rendered, and nothing else; where it does not, the term route of tasks h1 and h2 runs unchanged, with task h2's two printing fixes still on. Never hand-edited. The products of tasks h1, h2 and the other runs of this family are not written by this task: they sit beside these as `handful.json` / `handful.md`, `handful2.json` / `handful2.md`, `handful3*` and `handful3b*`.

**A swift compiler is reachable in this run.** Task g1's `g1` instance mounted an EMPTY persist volume, so `/persist/swift/usr/bin/swiftc` -- the path the whole swift corpus was built at -- did not exist and every swift place was refused there. `g1.conf` now mounts `sandbox-persist` read-only, as `t101b.conf` and `t103.conf` already do for the same toolchain, and the container was re-created on the rebuilt image, which carries `libncurses6`. `swiftc --version` answers `Swift version 6.0.3 (swift-6.0.3-RELEASE)`. The swift spelling table is still UNMEASURED row by row: what these runs measure is the renderer's OUTPUT through the real compiler, not each spelling by its own probe.

**What a run is, one sentence.** `find_emulation(cell, lang)` asks first whether `lang` has an operator whose whole lowered body IS this cell and, where it has, renders that operator on holders of the operand types the corpus recorded for it; where it has not, it takes the z3 term the reference simulator's own builder writes into each place the cell's opcode writes and has the existing renderer write that term in the target's own operators. Either way the source is compiled at that corpus's own ship flags, the body is carved back out, and z3 is asked whether it answers as the cell's term says for every input.

Table 0 -- what this run was.

| what | value |
|---|---|
| runs | 40 |
| c ship flags | lane_gen.py compile_probe: `[CLANG, "-std=c17"] + ["-O1"] + ["-c", src, "-o", obj]` -- the ship build of every c unit in the corpus |
| rust ship flags | lane_gen.py compile_probe, rust branch: `opt = ["-C", "opt-level=1", "-C", "debug-assertions=off"]` then `["rustc", "--crate-type=lib", "--emit=obj"] + opt + ["-o", obj, src]` -- the ship build of every rust unit in the corpus |
| go ship flags | lane_gen.py compile_probe, go branch: `open(go.mod).write(GOMOD)`; `open(main.go).write(p["source"])`; `cmd = ["go", "build"]` with no gcflags in the ship mode, then `cmd.extend(["-o", obj, "."])` run with cwd=the module directory -- the ship build of every go unit in the corpus |
| swift ship flags | lane_gen.py compile_probe, swift branch: `opt = ["-Onone", "-g"] if mode == "anchor" else ["-O"]`; `cmd = [SWIFTC] + opt + ["-c", src, "-o", obj]` -- the ship build of every swift unit in the corpus |
| swiftc, as this machine answers it | Swift version 6.0.3 (swift-6.0.3-RELEASE) |
| solver ceiling | 3000 ms |
| memory bound | 4194304 kB, named abort ABORT_MEMORY_G1B |
| peak resident | 488376 kB |

## 1. The runs, one section each

### 1.1 `add` gpr_gpr 32 -> c

The row, LITERAL: `add %esi,%edi` (`r00138`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 11 unit(s), 11 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, Extract(31, 0, seed_rdi) + Extract(31, 0, seed_rsi))
```

The source, LITERAL (`src3b/add_gpr_gpr_32__reg_rdi__c.c`):

```
/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of add_gpr_gpr_32__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1)) */
#include <stdint.h>

uint64_t
emu_add_gpr_gpr_32__reg_rdi__c(uint32_t a, uint32_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)((uint32_t)((uint32_t)a) + (uint32_t)((uint32_t)b)))));
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
lea (%rdi,%rsi,1),%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
lea (%rdi,%rsi,1),%eax
```

Against the cell's own arch opcode: **LANDED_ELSEWHERE** (landed on `lea`).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rsi | rsi |

#### place `flags`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(31, 0, v0), Extract(31, 0, v1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(Extract(31, 0, seed_rdi), Extract(31, 0, seed_rsi))
```

The source, LITERAL (`src3b/add_gpr_gpr_32__flags__c.c`):

```
/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of add_gpr_gpr_32__flags__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(31, 0, v0), Extract(31, 0, v1)) */
#include <stdint.h>

uint64_t
emu_add_gpr_gpr_32__flags__c(uint32_t a, uint32_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)((uint32_t)a) << 32) | (uint64_t)((uint32_t)b)));
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
shl $0x20,%rdi; mov %esi,%eax; or %rdi,%rax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
shl $0x20,%rdi; or %rdi,%rax
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (2 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rsi | rsi |

### 1.2 `add` gpr_gpr 32 -> rust

The row, LITERAL: `add %esi,%edi` (`r00138`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 11 unit(s), 11 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, Extract(31, 0, seed_rdi) + Extract(31, 0, seed_rsi))
```

The source, LITERAL (`src3b/add_gpr_gpr_32__reg_rdi__rust.rs`):

```
#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of add_gpr_gpr_32__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1))
#[no_mangle]
pub extern "C" fn emu_add_gpr_gpr_32__reg_rdi__rust(a: u32, b: u32) -> u64
{
    (((((((0x0u32) as u64) << 32) | ((((((((a as u32)) as u32)).wrapping_add((((b as u32)) as u32))) as u32)) as u64)) as u64)) as u64)
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
lea (%rdi,%rsi,1),%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
lea (%rdi,%rsi,1),%eax
```

Against the cell's own arch opcode: **LANDED_ELSEWHERE** (landed on `lea`).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rsi | rsi |

#### place `flags`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(31, 0, v0), Extract(31, 0, v1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(Extract(31, 0, seed_rdi), Extract(31, 0, seed_rsi))
```

The source, LITERAL (`src3b/add_gpr_gpr_32__flags__rust.rs`):

```
#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of add_gpr_gpr_32__flags__rust.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(31, 0, v0), Extract(31, 0, v1))
#[no_mangle]
pub extern "C" fn emu_add_gpr_gpr_32__flags__rust(a: u32, b: u32) -> u64
{
    ((((((((a as u32)) as u64) << 32) | (((b as u32)) as u64)) as u64)) as u64)
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
shl $0x20,%rdi; mov %esi,%eax; or %rdi,%rax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
shl $0x20,%rdi; or %rdi,%rax
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (2 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rsi | rsi |

### 1.3 `add` gpr_gpr 32 -> go

The row, LITERAL: `add %esi,%edi` (`r00138`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 11 unit(s), 11 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
a + b
```

The source, LITERAL (`src3b/add_gpr_gpr_32__primitive__go.go`):

```
// probe 312 -- binary +
package main

//go:noinline
func emu_add_gpr_gpr_32__primitive__go(a int32, b int32) int32 {
	return a + b
}

var ga int32
var gb int32
var sink interface{}

func main() {
	sink = emu_add_gpr_gpr_32__primitive__go(ga, gb)
	_ = sink
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
add %ebx,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
add %ebx,%eax
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rax |
| IN-1 | rsi | rbx |

#### place `flags`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(31, 0, v0), Extract(31, 0, v1))
```

**Step 2, the render.** REFUSED: the primitive route renders the operator's own answer, and the flags place is not a value an operator answers with (the operator's own answer is the value it hands back, and this cell's flags place is a second place the opcode writes).

### 1.4 `add` gpr_gpr 32 -> swift

The row, LITERAL: `add %esi,%edi` (`r00138`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 11 unit(s), 11 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, Extract(31, 0, seed_rdi) + Extract(31, 0, seed_rsi))
```

The source, LITERAL (`src3b/add_gpr_gpr_32__reg_rdi__swift.swift`):

```
// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of add_gpr_gpr_32__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0) + Extract(31, 0, v1))
@_cdecl("emu_add_gpr_gpr_32__reg_rdi__swift")
public func emu_add_gpr_gpr_32__reg_rdi__swift(_ a: UInt32, _ b: UInt32) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt32(a)))) &+ (UInt32(truncatingIfNeeded: (UInt32(b)))))))))))
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
lea (%rdi,%rsi,1),%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
lea (%rdi,%rsi,1),%eax
```

Against the cell's own arch opcode: **LANDED_ELSEWHERE** (landed on `lea`).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rsi | rsi |

#### place `flags`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(31, 0, v0), Extract(31, 0, v1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(Extract(31, 0, seed_rdi), Extract(31, 0, seed_rsi))
```

The source, LITERAL (`src3b/add_gpr_gpr_32__flags__swift.swift`):

```
// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of add_gpr_gpr_32__flags__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(31, 0, v0), Extract(31, 0, v1))
@_cdecl("emu_add_gpr_gpr_32__flags__swift")
public func emu_add_gpr_gpr_32__flags__swift(_ a: UInt32, _ b: UInt32) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: (UInt32(a)))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32(b)))))))
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
shl $0x20,%rdi; mov %esi,%eax; or %rdi,%rax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
shl $0x20,%rdi; or %rdi,%rax
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (2 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rsi | rsi |

### 1.5 `sub` imm_gpr 64 -> c

The row, LITERAL: `sub $0x3,%rdi` (`r14165`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 0 unit(s), 0 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
v0 + 18446744073709551613
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
seed_rdi + 18446744073709551613
```

The source, LITERAL (`src3b/sub_imm_gpr_64__reg_rdi__c.c`):

```
/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of sub_imm_gpr_64__reg_rdi__c.  The term's layer-5 text, LITERAL:
   v0 + 18446744073709551613 */
#include <stdint.h>

uint64_t
emu_sub_imm_gpr_64__reg_rdi__c(uint64_t a)
{
    return (uint64_t)((uint64_t)((uint64_t)((uint64_t)a) + (uint64_t)(UINT64_C(0xfffffffffffffffd))));
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
lea -0x3(%rdi),%rax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
lea -0x3(%rdi),%rax
```

Against the cell's own arch opcode: **LANDED_ELSEWHERE** (landed on `lea`).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |

#### place `flags`, 128 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(v0, 3)
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(seed_rdi, 3)
```

The source, LITERAL (`src3b/sub_imm_gpr_64__flags__c.c`):

```
/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of sub_imm_gpr_64__flags__c.  The term's layer-5 text, LITERAL:
   Concat(v0, 3) */
#include <stdint.h>

unsigned __int128
emu_sub_imm_gpr_64__flags__c(uint64_t a)
{
    return (unsigned __int128)((unsigned __int128)(((unsigned __int128)((uint64_t)a) << 64) | (unsigned __int128)(UINT64_C(0x3))));
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov $0x3,%eax; mov %rdi,%rdx; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
mov $0x3,%eax
```

Against the cell's own arch opcode: **LANDED_ELSEWHERE** (landed on `mov`).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 128 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |

### 1.6 `sub` imm_gpr 64 -> rust

The row, LITERAL: `sub $0x3,%rdi` (`r14165`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 0 unit(s), 0 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
v0 + 18446744073709551613
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
seed_rdi + 18446744073709551613
```

The source, LITERAL (`src3b/sub_imm_gpr_64__reg_rdi__rust.rs`):

```
#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of sub_imm_gpr_64__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   v0 + 18446744073709551613
#[no_mangle]
pub extern "C" fn emu_sub_imm_gpr_64__reg_rdi__rust(a: u64) -> u64
{
    ((((((((a as u64)) as u64)).wrapping_add(((0xfffffffffffffffdu64) as u64))) as u64)) as u64)
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
lea -0x3(%rdi),%rax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
lea -0x3(%rdi),%rax
```

Against the cell's own arch opcode: **LANDED_ELSEWHERE** (landed on `lea`).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |

#### place `flags`, 128 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(v0, 3)
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(seed_rdi, 3)
```

The source, LITERAL (`src3b/sub_imm_gpr_64__flags__rust.rs`):

```
#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of sub_imm_gpr_64__flags__rust.
// The term's layer-5 text, LITERAL:
//   Concat(v0, 3)
#[no_mangle]
pub extern "C" fn emu_sub_imm_gpr_64__flags__rust(a: u64) -> u128
{
    ((((((((a as u64)) as u128) << 64) | ((0x3u64) as u128)) as u128)) as u128)
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov $0x3,%eax; mov %rdi,%rdx; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
mov $0x3,%eax
```

Against the cell's own arch opcode: **LANDED_ELSEWHERE** (landed on `mov`).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 128 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |

### 1.7 `sub` imm_gpr 64 -> go

The row, LITERAL: `sub $0x3,%rdi` (`r14165`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 0 unit(s), 0 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
v0 + 18446744073709551613
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
seed_rdi + 18446744073709551613
```

The source, LITERAL (`src3b/sub_imm_gpr_64__reg_rdi__go.go`):

```
// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of sub_imm_gpr_64__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   v0 + 18446744073709551613
package main

//go:noinline
func emu_sub_imm_gpr_64__reg_rdi__go(a uint64) uint64 {
	return uint64((uint64((uint64(uint64(a))) + (uint64(uint64(0xfffffffffffffffd))))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_sub_imm_gpr_64__reg_rdi__go(g0)
	_ = sink
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
add $0xfffffffffffffffd,%rax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
add $0xfffffffffffffffd,%rax
```

Against the cell's own arch opcode: **LANDED_ELSEWHERE** (landed on `add`).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rax |

#### place `flags`, 128 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(v0, 3)
```

**Step 2, the render.** REFUSED: a width c has no holder for (go has no 128-bit integer holder: `go build` refuses `uint128` with "undefined: uint128" (measured, probe wide_holder_128)).

### 1.8 `sub` imm_gpr 64 -> swift

The row, LITERAL: `sub $0x3,%rdi` (`r14165`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 0 unit(s), 0 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
v0 + 18446744073709551613
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
seed_rdi + 18446744073709551613
```

The source, LITERAL (`src3b/sub_imm_gpr_64__reg_rdi__swift.swift`):

```
// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of sub_imm_gpr_64__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   v0 + 18446744073709551613
@_cdecl("emu_sub_imm_gpr_64__reg_rdi__swift")
public func emu_sub_imm_gpr_64__reg_rdi__swift(_ a: UInt64) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(a)))) &+ (UInt64(truncatingIfNeeded: UInt64(0xfffffffffffffffd))))))
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
lea -0x3(%rdi),%rax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
lea -0x3(%rdi),%rax
```

Against the cell's own arch opcode: **LANDED_ELSEWHERE** (landed on `lea`).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |

#### place `flags`, 128 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(v0, 3)
```

**Step 2, the render.** REFUSED: a width c has no holder for (swift's 128-bit integer holder is not spelled by this renderer: whether this toolchain has Int128/UInt128 is UNMEASURED, there being no swiftc in the image).

### 1.9 `imul` gpr_gpr 32 -> c

The row, LITERAL: `imul %esi,%edi` (`r07499`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 266 unit(s), 266 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, v0)*Extract(31, 0, v1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
a * b
```

The source, LITERAL (`src3b/imul_gpr_gpr_32__primitive__c.c`):

```
/* probe 174 -- binary * */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} * (int32_t){0})
emu_imul_gpr_gpr_32__primitive__c(int32_t a, int32_t b)
{
    return a * b;
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov %edi,%eax; imul %esi,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
imul %esi,%eax
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rsi | rsi |

#### place `flags`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(31, 0, v0), Extract(31, 0, v1))
```

**Step 2, the render.** REFUSED: the primitive route renders the operator's own answer, and the flags place is not a value an operator answers with (the operator's own answer is the value it hands back, and this cell's flags place is a second place the opcode writes).

### 1.10 `imul` gpr_gpr 32 -> rust

The row, LITERAL: `imul %esi,%edi` (`r07499`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 266 unit(s), 266 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, v0)*Extract(31, 0, v1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
a * b
```

The source, LITERAL (`src3b/imul_gpr_gpr_32__primitive__rust.rs`):

```
// probe 606 -- binary *
#[no_mangle]
pub fn emu_imul_gpr_gpr_32__primitive__rust(a: i32, b: i32) -> <i32 as core::ops::Mul<i32>>::Output {
    a * b
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov %edi,%eax; imul %esi,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
imul %esi,%eax
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rsi | rsi |

#### place `flags`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(31, 0, v0), Extract(31, 0, v1))
```

**Step 2, the render.** REFUSED: the primitive route renders the operator's own answer, and the flags place is not a value an operator answers with (the operator's own answer is the value it hands back, and this cell's flags place is a second place the opcode writes).

### 1.11 `imul` gpr_gpr 32 -> go

The row, LITERAL: `imul %esi,%edi` (`r07499`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 266 unit(s), 266 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, v0)*Extract(31, 0, v1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
a * b
```

The source, LITERAL (`src3b/imul_gpr_gpr_32__primitive__go.go`):

```
// probe 60 -- binary *
package main

//go:noinline
func emu_imul_gpr_gpr_32__primitive__go(a int32, b int32) int32 {
	return a * b
}

var ga int32
var gb int32
var sink interface{}

func main() {
	sink = emu_imul_gpr_gpr_32__primitive__go(ga, gb)
	_ = sink
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
imul %ebx,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
imul %ebx,%eax
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rax |
| IN-1 | rsi | rbx |

#### place `flags`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(31, 0, v0), Extract(31, 0, v1))
```

**Step 2, the render.** REFUSED: the primitive route renders the operator's own answer, and the flags place is not a value an operator answers with (the operator's own answer is the value it hands back, and this cell's flags place is a second place the opcode writes).

### 1.12 `imul` gpr_gpr 32 -> swift

The row, LITERAL: `imul %esi,%edi` (`r07499`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 266 unit(s), 266 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, v0)*Extract(31, 0, v1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, Extract(31, 0, seed_rdi)*Extract(31, 0, seed_rsi))
```

The source, LITERAL (`src3b/imul_gpr_gpr_32__reg_rdi__swift.swift`):

```
// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of imul_gpr_gpr_32__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0)*Extract(31, 0, v1))
@_cdecl("emu_imul_gpr_gpr_32__reg_rdi__swift")
public func emu_imul_gpr_gpr_32__reg_rdi__swift(_ a: UInt32, _ b: UInt32) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt32(a)))) &* (UInt32(truncatingIfNeeded: (UInt32(b)))))))))))
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov %edi,%eax; imul %esi,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
imul %esi,%eax
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rsi | rsi |

#### place `flags`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(31, 0, v0), Extract(31, 0, v1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(Extract(31, 0, seed_rdi), Extract(31, 0, seed_rsi))
```

The source, LITERAL (`src3b/imul_gpr_gpr_32__flags__swift.swift`):

```
// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of imul_gpr_gpr_32__flags__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(31, 0, v0), Extract(31, 0, v1))
@_cdecl("emu_imul_gpr_gpr_32__flags__swift")
public func emu_imul_gpr_gpr_32__flags__swift(_ a: UInt32, _ b: UInt32) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: (UInt32(a)))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32(b)))))))
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
shl $0x20,%rdi; mov %esi,%eax; or %rdi,%rax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
shl $0x20,%rdi; or %rdi,%rax
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (2 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rsi | rsi |

### 1.13 `sar` cl_gpr 32 -> c

The row, LITERAL: `sar %cl,%edi` (`r12211`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 335 unit(s), 335 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1)))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
a >> b
```

The source, LITERAL (`src3b/sar_cl_gpr_32__primitive__c.c`):

```
/* probe 714 -- binary >> */
#include <stdint.h>
#include <stdbool.h>

__typeof__((int32_t){0} >> (int32_t){0})
emu_sar_cl_gpr_32__primitive__c(int32_t a, int32_t b)
{
    return a >> b;
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov %esi,%ecx; mov %edi,%eax; sar %cl,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
sar %cl,%eax
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rcx | rsi |

### 1.14 `sar` cl_gpr 32 -> rust

The row, LITERAL: `sar %cl,%edi` (`r12211`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 335 unit(s), 335 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1)))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
a >> b
```

The source, LITERAL (`src3b/sar_cl_gpr_32__primitive__rust.rs`):

```
// probe 499 -- binary >>
#[no_mangle]
pub fn emu_sar_cl_gpr_32__primitive__rust(a: i32, b: i64) -> <i32 as core::ops::Shr<i64>>::Output {
    a >> b
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov %rsi,%rcx; mov %edi,%eax; sar %cl,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
sar %cl,%eax
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rcx | rsi |

### 1.15 `sar` cl_gpr 32 -> go

The row, LITERAL: `sar %cl,%edi` (`r12211`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 335 unit(s), 335 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1)))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, Extract(31, 0, seed_rdi) >> Concat(0, Extract(4, 0, seed_rcx)))
```

The source, LITERAL (`src3b/sar_cl_gpr_32__reg_rdi__go.go`):

```
// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of sar_cl_gpr_32__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1)))
package main

//go:noinline
func emu_sar_cl_gpr_32__reg_rdi__go(a uint32, b uint8) uint64 {
	return uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32(uint32((int32(uint32(a))) >> ((uint32((uint32(((uint32(uint32(0x0))) << 5) | (uint32(((uint32((uint32(b)) >> 0)) & uint32(0x1f)))))))) & uint32(0x1f))))))))))
}

var g0 uint32
var g1 uint8
var sink interface{}

func main() {
	sink = emu_sar_cl_gpr_32__reg_rdi__go(g0, g1)
	_ = sink
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
movzbl %bl,%ecx; sar %cl,%eax; mov %eax,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
movzbl %bl,%ecx; sar %cl,%eax
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (2 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rax |
| IN-1 | rcx | rbx |

### 1.16 `sar` cl_gpr 32 -> swift

The row, LITERAL: `sar %cl,%edi` (`r12211`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 335 unit(s), 335 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1)))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, Extract(31, 0, seed_rdi) >> Concat(0, Extract(4, 0, seed_rcx)))
```

The source, LITERAL (`src3b/sar_cl_gpr_32__reg_rdi__swift.swift`):

```
// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of sar_cl_gpr_32__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1)))
@_cdecl("emu_sar_cl_gpr_32__reg_rdi__swift")
public func emu_sar_cl_gpr_32__reg_rdi__swift(_ a: UInt32, _ b: UInt8) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32(truncatingIfNeeded: UInt32(bitPattern: ((Int32(bitPattern: (UInt32(a))))) &>> (UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: UInt32(0x0))) &<< 5) | (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(b))) &>> 0)) & UInt32(0x1f))))))))))))))))
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov %esi,%ecx; mov %edi,%eax; sar %cl,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
sar %cl,%eax
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rcx | rsi |

### 1.17 `shr` cl_gpr 64 -> c

The row, LITERAL: `shr %cl,%rdi` (`r13982`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 251 unit(s), 251 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
LShR(v0, Concat(0, Extract(5, 0, v1)))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
a >> b
```

The source, LITERAL (`src3b/shr_cl_gpr_64__primitive__c.c`):

```
/* probe 726 -- binary >> */
#include <stdint.h>
#include <stdbool.h>

__typeof__((uint64_t){0} >> (int32_t){0})
emu_shr_cl_gpr_64__primitive__c(uint64_t a, int32_t b)
{
    return a >> b;
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov %esi,%ecx; mov %rdi,%rax; shr %cl,%rax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
shr %cl,%rax
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rcx | rsi |

### 1.18 `shr` cl_gpr 64 -> rust

The row, LITERAL: `shr %cl,%rdi` (`r13982`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 251 unit(s), 251 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
LShR(v0, Concat(0, Extract(5, 0, v1)))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
a >> b
```

The source, LITERAL (`src3b/shr_cl_gpr_64__primitive__rust.rs`):

```
// probe 511 -- binary >>
#[no_mangle]
pub fn emu_shr_cl_gpr_64__primitive__rust(a: u64, b: i64) -> <u64 as core::ops::Shr<i64>>::Output {
    a >> b
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov %rsi,%rcx; mov %rdi,%rax; shr %cl,%rax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
shr %cl,%rax
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rcx | rsi |

### 1.19 `shr` cl_gpr 64 -> go

The row, LITERAL: `shr %cl,%rdi` (`r13982`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 251 unit(s), 251 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
LShR(v0, Concat(0, Extract(5, 0, v1)))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
LShR(seed_rdi, Concat(0, Extract(5, 0, seed_rcx)))
```

The source, LITERAL (`src3b/shr_cl_gpr_64__reg_rdi__go.go`):

```
// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of shr_cl_gpr_64__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   LShR(v0, Concat(0, Extract(5, 0, v1)))
package main

//go:noinline
func emu_shr_cl_gpr_64__reg_rdi__go(a uint64, b uint8) uint64 {
	return uint64((uint64((uint64(uint64(a))) >> ((uint64((uint64(((uint64(uint64(0x0))) << 6) | (uint64(((uint32((uint32(b)) >> 0)) & uint32(0x3f)))))))) & uint64(0x3f)))))
}

var g0 uint64
var g1 uint8
var sink interface{}

func main() {
	sink = emu_shr_cl_gpr_64__reg_rdi__go(g0, g1)
	_ = sink
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
movzbl %bl,%ecx; shr %cl,%rax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
movzbl %bl,%ecx; shr %cl,%rax
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (2 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rax |
| IN-1 | rcx | rbx |

### 1.20 `shr` cl_gpr 64 -> swift

The row, LITERAL: `shr %cl,%rdi` (`r13982`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 251 unit(s), 251 ledger row(s).

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
LShR(v0, Concat(0, Extract(5, 0, v1)))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
LShR(seed_rdi, Concat(0, Extract(5, 0, seed_rcx)))
```

The source, LITERAL (`src3b/shr_cl_gpr_64__reg_rdi__swift.swift`):

```
// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of shr_cl_gpr_64__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   LShR(v0, Concat(0, Extract(5, 0, v1)))
@_cdecl("emu_shr_cl_gpr_64__reg_rdi__swift")
public func emu_shr_cl_gpr_64__reg_rdi__swift(_ a: UInt64, _ b: UInt8) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(a)))) &>> (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt64(0x0))) &<< 6) | (UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(b))) &>> 0)) & UInt32(0x3f)))))))))))
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov %esi,%ecx; mov %rdi,%rax; shr %cl,%rax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
shr %cl,%rax
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rcx | rsi |

### 1.21 `idiv` gpr_one 32 -> c

The row, LITERAL: `idiv %edi` (`r07409`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 389 unit(s), 778 ledger row(s).

#### place `reg_rax`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, seed_rdx), Extract(31, 0, seed_rax)), Concat(Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 0, seed_rdi)))))
```

The source, LITERAL (`src3b/idiv_gpr_one_32__reg_rax__c.c`):

```
/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of idiv_gpr_one_32__reg_rax__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2))))) */
#include <stdint.h>

uint64_t
emu_idiv_gpr_one_32__reg_rax__c(uint32_t a, uint32_t b, uint32_t c)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)((uint64_t)((uint64_t)((int64_t)((int64_t)((uint64_t)(((uint64_t)((uint32_t)a) << 32) | (uint64_t)((uint32_t)b)))) / (int64_t)((int64_t)((uint64_t)(((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 63) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 62) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 61) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 60) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 59) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 58) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 57) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 56) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 55) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 54) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 53) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 52) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 51) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 50) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 49) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 48) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 47) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 46) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 45) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 44) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 43) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 42) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 41) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 40) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 39) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 38) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 37) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 36) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 35) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 34) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 33) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 32) | (uint64_t)((uint32_t)c)))))) >> 0))));
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
shl $0x20,%rdi; mov %esi,%eax; or %rdi,%rax; mov %edx,%ecx; mov %edx,%esi; shr $0x1f,%esi; mov %rsi,%rdx; mov %rsi,%rdi; shl $0x32,%rdi; mov %rsi,%r8; shl $0x31,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x30,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x2f,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x2e,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x2d,%r8; or %rdi,%r8; mov %rsi,%r9; shl $0x2c,%r9; or %r8,%r9; mov %rsi,%rdi; shl $0x2b,%rdi; mov %rsi,%r8; shl $0x2a,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x29,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x28,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x27,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x26,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x25,%rdi; or %r8,%rdi; or %r9,%rdi; mov %rsi,%r8; shl $0x24,%r8; mov %rsi,%r9; shl $0x23,%r9; or %r8,%r9; mov %rsi,%r8; shl $0x22,%r8; or %r9,%r8; mov %rsi,%r9; shl $0x21,%r9; or %r8,%r9; mov %rsi,%r8; movabs $0xf8000000000000,%r10; imul %rsi,%r10; shl $0x39,%rsi; neg %rsi; shl $0x38,%rdx; shl $0x20,%r8; or %r9,%r8; or %rsi,%r8; or %rdx,%rcx; or %rcx,%r10; or %r8,%r10; or %rdi,%r10; cqto; idiv %r10; mov %eax,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
shl $0x20,%rdi; or %rdi,%rax; shr $0x1f,%esi; shl $0x32,%rdi; shl $0x31,%r8; or %rdi,%r8; shl $0x30,%rdi; or %r8,%rdi; shl $0x2f,%r8; or %rdi,%r8; shl $0x2e,%rdi; or %r8,%rdi; shl $0x2d,%r8; or %rdi,%r8; shl $0x2c,%r9; or %r8,%r9; shl $0x2b,%rdi; shl $0x2a,%r8; or %rdi,%r8; shl $0x29,%rdi; or %r8,%rdi; shl $0x28,%r8; or %rdi,%r8; shl $0x27,%rdi; or %r8,%rdi; shl $0x26,%r8; or %rdi,%r8; shl $0x25,%rdi; or %r8,%rdi; or %r9,%rdi; shl $0x24,%r8; shl $0x23,%r9; or %r8,%r9; shl $0x22,%r8; or %r9,%r8; shl $0x21,%r9; or %r8,%r9; movabs $0xf8000000000000,%r10; imul %rsi,%r10; shl $0x39,%rsi; neg %rsi; shl $0x38,%rdx; shl $0x20,%r8; or %r9,%r8; or %rsi,%r8; or %rdx,%rcx; or %rcx,%r10; or %r8,%r10; or %rdi,%r10; cqto; idiv %r10
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (51 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **UNDECIDED** -- the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

Re-posed with more solver room (300000 ms instead of 3,000): **UNDECIDED** -- the solver did not answer inside its 300000 ms limit, so the verdict is undecided and never disproved

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdx | rdi |
| IN-1 | rax | rsi |
| IN-2 | rdi | rdx |

#### place `reg_rdx`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, bvsrem_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, Extract(31, 0, bvsrem_i(Concat(Extract(31, 0, seed_rdx), Extract(31, 0, seed_rax)), Concat(Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 0, seed_rdi)))))
```

The source, LITERAL (`src3b/idiv_gpr_one_32__reg_rdx__c.c`):

```
/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of idiv_gpr_one_32__reg_rdx__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 0, bvsrem_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2))))) */
#include <stdint.h>

uint64_t
emu_idiv_gpr_one_32__reg_rdx__c(uint32_t a, uint32_t b, uint32_t c)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)((uint64_t)((uint64_t)((int64_t)((int64_t)((uint64_t)(((uint64_t)((uint32_t)a) << 32) | (uint64_t)((uint32_t)b)))) % (int64_t)((int64_t)((uint64_t)(((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 63) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 62) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 61) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 60) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 59) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 58) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 57) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 56) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 55) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 54) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 53) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 52) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 51) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 50) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 49) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 48) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 47) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 46) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 45) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 44) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 43) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 42) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 41) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 40) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 39) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 38) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 37) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 36) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 35) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 34) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 33) | ((uint64_t)(((uint32_t)((uint32_t)c >> 31) & UINT32_C(0x1))) << 32) | (uint64_t)((uint32_t)c)))))) >> 0))));
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
shl $0x20,%rdi; mov %esi,%eax; or %rdi,%rax; mov %edx,%ecx; mov %edx,%esi; shr $0x1f,%esi; mov %rsi,%rdx; mov %rsi,%rdi; shl $0x32,%rdi; mov %rsi,%r8; shl $0x31,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x30,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x2f,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x2e,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x2d,%r8; or %rdi,%r8; mov %rsi,%r9; shl $0x2c,%r9; or %r8,%r9; mov %rsi,%rdi; shl $0x2b,%rdi; mov %rsi,%r8; shl $0x2a,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x29,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x28,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x27,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x26,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x25,%rdi; or %r8,%rdi; or %r9,%rdi; mov %rsi,%r8; shl $0x24,%r8; mov %rsi,%r9; shl $0x23,%r9; or %r8,%r9; mov %rsi,%r8; shl $0x22,%r8; or %r9,%r8; mov %rsi,%r9; shl $0x21,%r9; or %r8,%r9; mov %rsi,%r8; movabs $0xf8000000000000,%r10; imul %rsi,%r10; shl $0x39,%rsi; neg %rsi; shl $0x38,%rdx; shl $0x20,%r8; or %r9,%r8; or %rsi,%r8; or %rdx,%rcx; or %rcx,%r10; or %r8,%r10; or %rdi,%r10; cqto; idiv %r10; mov %edx,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
shl $0x20,%rdi; or %rdi,%rax; shr $0x1f,%esi; shl $0x32,%rdi; shl $0x31,%r8; or %rdi,%r8; shl $0x30,%rdi; or %r8,%rdi; shl $0x2f,%r8; or %rdi,%r8; shl $0x2e,%rdi; or %r8,%rdi; shl $0x2d,%r8; or %rdi,%r8; shl $0x2c,%r9; or %r8,%r9; shl $0x2b,%rdi; shl $0x2a,%r8; or %rdi,%r8; shl $0x29,%rdi; or %r8,%rdi; shl $0x28,%r8; or %rdi,%r8; shl $0x27,%rdi; or %r8,%rdi; shl $0x26,%r8; or %rdi,%r8; shl $0x25,%rdi; or %r8,%rdi; or %r9,%rdi; shl $0x24,%r8; shl $0x23,%r9; or %r8,%r9; shl $0x22,%r8; or %r9,%r8; shl $0x21,%r9; or %r8,%r9; movabs $0xf8000000000000,%r10; imul %rsi,%r10; shl $0x39,%rsi; neg %rsi; shl $0x38,%rdx; shl $0x20,%r8; or %r9,%r8; or %rsi,%r8; or %rdx,%rcx; or %rcx,%r10; or %r8,%r10; or %rdi,%r10; cqto; idiv %r10
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (51 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **UNDECIDED** -- the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

Re-posed with more solver room (300000 ms instead of 3,000): **UNDECIDED** -- the solver did not answer inside its 300000 ms limit, so the verdict is undecided and never disproved

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdx | rdi |
| IN-1 | rax | rsi |
| IN-2 | rdi | rdx |

### 1.22 `idiv` gpr_one 32 -> rust

The row, LITERAL: `idiv %edi` (`r07409`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 389 unit(s), 778 ledger row(s).

#### place `reg_rax`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, seed_rdx), Extract(31, 0, seed_rax)), Concat(Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 0, seed_rdi)))))
```

The source, LITERAL (`src3b/idiv_gpr_one_32__reg_rax__rust.rs`):

```
#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of idiv_gpr_one_32__reg_rax__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
#[no_mangle]
pub extern "C" fn emu_idiv_gpr_one_32__reg_rax__rust(a: u32, b: u32, c: u32) -> u64
{
    (((((((0x0u32) as u64) << 32) | ((((((((({ let n1: i64 = ((((((((((a as u32)) as u64) << 32) | (((b as u32)) as u64)) as u64)) as i64)) as i64); let d1: i64 = ((((((((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 63) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 62) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 61) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 60) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 59) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 58) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 57) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 56) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 55) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 54) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 53) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 52) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 51) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 50) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 49) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 48) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 47) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 46) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 45) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 44) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 43) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 42) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 41) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 40) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 39) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 38) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 37) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 36) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 35) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 34) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 33) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 32) | (((c as u32)) as u64)) as u64)) as i64)) as i64); unsafe { if d1 == 0 || (n1 == i64::MIN && d1 == -1) { core::hint::unreachable_unchecked(); } } n1 / d1 })) as u64)) as u64) >> 0) as u32)) as u64)) as u64)) as u64)
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
shl $0x20,%rdi; mov %esi,%eax; or %rdi,%rax; mov %edx,%ecx; mov %edx,%esi; shr $0x1f,%esi; mov %rsi,%rdx; mov %rsi,%rdi; shl $0x32,%rdi; mov %rsi,%r8; shl $0x31,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x30,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x2f,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x2e,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x2d,%r8; or %rdi,%r8; mov %rsi,%r9; shl $0x2c,%r9; or %r8,%r9; mov %rsi,%rdi; shl $0x2b,%rdi; mov %rsi,%r8; shl $0x2a,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x29,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x28,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x27,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x26,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x25,%rdi; or %r8,%rdi; or %r9,%rdi; mov %rsi,%r8; shl $0x24,%r8; mov %rsi,%r9; shl $0x23,%r9; or %r8,%r9; mov %rsi,%r8; shl $0x22,%r8; or %r9,%r8; mov %rsi,%r9; shl $0x21,%r9; or %r8,%r9; mov %rsi,%r8; movabs $0xf8000000000000,%r10; imul %rsi,%r10; shl $0x39,%rsi; neg %rsi; shl $0x38,%rdx; shl $0x20,%r8; or %r9,%r8; or %rsi,%r8; or %rdx,%rcx; or %rcx,%r10; or %r8,%r10; or %rdi,%r10; cqto; idiv %r10; mov %eax,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
shl $0x20,%rdi; or %rdi,%rax; shr $0x1f,%esi; shl $0x32,%rdi; shl $0x31,%r8; or %rdi,%r8; shl $0x30,%rdi; or %r8,%rdi; shl $0x2f,%r8; or %rdi,%r8; shl $0x2e,%rdi; or %r8,%rdi; shl $0x2d,%r8; or %rdi,%r8; shl $0x2c,%r9; or %r8,%r9; shl $0x2b,%rdi; shl $0x2a,%r8; or %rdi,%r8; shl $0x29,%rdi; or %r8,%rdi; shl $0x28,%r8; or %rdi,%r8; shl $0x27,%rdi; or %r8,%rdi; shl $0x26,%r8; or %rdi,%r8; shl $0x25,%rdi; or %r8,%rdi; or %r9,%rdi; shl $0x24,%r8; shl $0x23,%r9; or %r8,%r9; shl $0x22,%r8; or %r9,%r8; shl $0x21,%r9; or %r8,%r9; movabs $0xf8000000000000,%r10; imul %rsi,%r10; shl $0x39,%rsi; neg %rsi; shl $0x38,%rdx; shl $0x20,%r8; or %r9,%r8; or %rsi,%r8; or %rdx,%rcx; or %rcx,%r10; or %r8,%r10; or %rdi,%r10; cqto; idiv %r10
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (51 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **UNDECIDED** -- the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

Re-posed with more solver room (300000 ms instead of 3,000): **UNDECIDED** -- the solver did not answer inside its 300000 ms limit, so the verdict is undecided and never disproved

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdx | rdi |
| IN-1 | rax | rsi |
| IN-2 | rdi | rdx |

#### place `reg_rdx`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, bvsrem_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, Extract(31, 0, bvsrem_i(Concat(Extract(31, 0, seed_rdx), Extract(31, 0, seed_rax)), Concat(Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 0, seed_rdi)))))
```

The source, LITERAL (`src3b/idiv_gpr_one_32__reg_rdx__rust.rs`):

```
#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of idiv_gpr_one_32__reg_rdx__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, bvsrem_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
#[no_mangle]
pub extern "C" fn emu_idiv_gpr_one_32__reg_rdx__rust(a: u32, b: u32, c: u32) -> u64
{
    (((((((0x0u32) as u64) << 32) | ((((((((({ let n1: i64 = ((((((((((a as u32)) as u64) << 32) | (((b as u32)) as u64)) as u64)) as i64)) as i64); let d1: i64 = ((((((((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 63) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 62) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 61) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 60) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 59) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 58) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 57) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 56) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 55) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 54) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 53) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 52) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 51) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 50) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 49) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 48) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 47) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 46) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 45) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 44) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 43) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 42) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 41) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 40) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 39) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 38) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 37) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 36) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 35) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 34) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 33) | ((((((((c as u32)) >> 31) as u32) & 0x1u32)) as u64) << 32) | (((c as u32)) as u64)) as u64)) as i64)) as i64); unsafe { if d1 == 0 || (n1 == i64::MIN && d1 == -1) { core::hint::unreachable_unchecked(); } } n1 % d1 })) as u64)) as u64) >> 0) as u32)) as u64)) as u64)) as u64)
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
shl $0x20,%rdi; mov %esi,%eax; or %rdi,%rax; mov %edx,%ecx; mov %edx,%esi; shr $0x1f,%esi; mov %rsi,%rdx; mov %rsi,%rdi; shl $0x32,%rdi; mov %rsi,%r8; shl $0x31,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x30,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x2f,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x2e,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x2d,%r8; or %rdi,%r8; mov %rsi,%r9; shl $0x2c,%r9; or %r8,%r9; mov %rsi,%rdi; shl $0x2b,%rdi; mov %rsi,%r8; shl $0x2a,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x29,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x28,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x27,%rdi; or %r8,%rdi; mov %rsi,%r8; shl $0x26,%r8; or %rdi,%r8; mov %rsi,%rdi; shl $0x25,%rdi; or %r8,%rdi; or %r9,%rdi; mov %rsi,%r8; shl $0x24,%r8; mov %rsi,%r9; shl $0x23,%r9; or %r8,%r9; mov %rsi,%r8; shl $0x22,%r8; or %r9,%r8; mov %rsi,%r9; shl $0x21,%r9; or %r8,%r9; mov %rsi,%r8; movabs $0xf8000000000000,%r10; imul %rsi,%r10; shl $0x39,%rsi; neg %rsi; shl $0x38,%rdx; shl $0x20,%r8; or %r9,%r8; or %rsi,%r8; or %rdx,%rcx; or %rcx,%r10; or %r8,%r10; or %rdi,%r10; cqto; idiv %r10; mov %edx,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
shl $0x20,%rdi; or %rdi,%rax; shr $0x1f,%esi; shl $0x32,%rdi; shl $0x31,%r8; or %rdi,%r8; shl $0x30,%rdi; or %r8,%rdi; shl $0x2f,%r8; or %rdi,%r8; shl $0x2e,%rdi; or %r8,%rdi; shl $0x2d,%r8; or %rdi,%r8; shl $0x2c,%r9; or %r8,%r9; shl $0x2b,%rdi; shl $0x2a,%r8; or %rdi,%r8; shl $0x29,%rdi; or %r8,%rdi; shl $0x28,%r8; or %rdi,%r8; shl $0x27,%rdi; or %r8,%rdi; shl $0x26,%r8; or %rdi,%r8; shl $0x25,%rdi; or %r8,%rdi; or %r9,%rdi; shl $0x24,%r8; shl $0x23,%r9; or %r8,%r9; shl $0x22,%r8; or %r9,%r8; shl $0x21,%r9; or %r8,%r9; movabs $0xf8000000000000,%r10; imul %rsi,%r10; shl $0x39,%rsi; neg %rsi; shl $0x38,%rdx; shl $0x20,%r8; or %r9,%r8; or %rsi,%r8; or %rdx,%rcx; or %rcx,%r10; or %r8,%r10; or %rdi,%r10; cqto; idiv %r10
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (51 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **UNDECIDED** -- the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

Re-posed with more solver room (300000 ms instead of 3,000): **UNDECIDED** -- the solver did not answer inside its 300000 ms limit, so the verdict is undecided and never disproved

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdx | rdi |
| IN-1 | rax | rsi |
| IN-2 | rdi | rdx |

### 1.23 `idiv` gpr_one 32 -> go

The row, LITERAL: `idiv %edi` (`r07409`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 389 unit(s), 778 ledger row(s).

#### place `reg_rax`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, seed_rdx), Extract(31, 0, seed_rax)), Concat(Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 0, seed_rdi)))))
```

The source, LITERAL (`src3b/idiv_gpr_one_32__reg_rax__go.go`):

```
// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of idiv_gpr_one_32__reg_rax__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
package main

//go:noinline
func emu_idiv_gpr_one_32__reg_rax__go(a uint32, b uint32, c uint32) uint64 {
	return uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64((uint64(uint64((int64((uint64(((uint64(uint32(a))) << 32) | (uint64(uint32(b))))))) / (int64((uint64(((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 63) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 62) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 61) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 60) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 59) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 58) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 57) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 56) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 55) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 54) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 53) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 52) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 51) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 50) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 49) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 48) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 47) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 46) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 45) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 44) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 43) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 42) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 41) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 40) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 39) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 38) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 37) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 36) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 35) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 34) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 33) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 32) | (uint64(uint32(c)))))))))))) >> 0)))))))
}

var g0 uint32
var g1 uint32
var g2 uint32
var sink interface{}

func main() {
	sink = emu_idiv_gpr_one_32__reg_rax__go(g0, g1, g2)
	_ = sink
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
lea -0x40(%rsp),%r12; cmp 0x10(%r14),%r12; jbe 47a929 <main.emu_idiv_gpr_one_32__reg_rax__go+0x2c9>; push %rbp; mov %rsp,%rbp; sub $0xb8,%rsp; mov %eax,%eax; shl $0x20,%rax; mov %ebx,%edx; mov %rdx,0x28(%rsp); mov %ecx,%ebx; shr $0x1f,%ecx; and $0x1,%ecx; mov %rcx,0x20(%rsp); mov %rcx,%rsi; shl $0x3f,%rcx; mov %ebx,%ebx; mov %rbx,0x18(%rsp); mov %rsi,%rdi; shl $0x20,%rsi; mov %rsi,0x10(%rsp); mov %rdi,%r8; shl $0x21,%rdi; mov %rdi,0x8(%rsp); mov %r8,%r9; shl $0x22,%r8; mov %r8,(%rsp); mov %r9,%r10; shl $0x23,%r9; mov %r9,0xb0(%rsp); mov %r10,%r11; shl $0x24,%r10; mov %r10,0xa8(%rsp); mov %r11,%r12; shl $0x25,%r11; mov %r11,0xa0(%rsp); mov %r12,%r13; shl $0x26,%r12; mov %r12,0x98(%rsp); mov %r13,%r15; shl $0x27,%r13; mov %r13,0x90(%rsp); shl $0x28,%r15; mov %r15,0x88(%rsp); mov 0x20(%rsp),%rdx; shl $0x29,%rdx; mov %rdx,0x80(%rsp); mov 0x20(%rsp),%rbx; shl $0x2a,%rbx; mov %rbx,0x78(%rsp); mov 0x20(%rsp),%rsi; shl $0x2b,%rsi; mov %rsi,0x70(%rsp); mov 0x20(%rsp),%rdi; shl $0x2c,%rdi; mov %rdi,0x68(%rsp); mov 0x20(%rsp),%r8; shl $0x2d,%r8; mov %r8,0x60(%rsp); mov 0x20(%rsp),%r9; shl $0x2e,%r9; mov %r9,0x58(%rsp); mov 0x20(%rsp),%r10; shl $0x2f,%r10; mov %r10,0x50(%rsp); mov 0x20(%rsp),%r11; shl $0x30,%r11; mov %r11,0x48(%rsp); mov 0x20(%rsp),%r12; shl $0x31,%r12; mov %r12,0x40(%rsp); mov 0x20(%rsp),%r13; shl $0x32,%r13; mov %r13,0x38(%rsp); mov 0x20(%rsp),%r15; shl $0x33,%r15; mov %r15,0x30(%rsp); mov 0x20(%rsp),%rdx; shl $0x34,%rdx; mov 0x20(%rsp),%rbx; shl $0x35,%rbx; mov 0x20(%rsp),%rsi; shl $0x36,%rsi; mov 0x20(%rsp),%rdi; shl $0x37,%rdi; mov 0x20(%rsp),%r8; shl $0x38,%r8; mov 0x20(%rsp),%r9; shl $0x39,%r9; mov 0x20(%rsp),%r10; shl $0x3a,%r10; mov 0x20(%rsp),%r11; shl $0x3b,%r11; mov 0x20(%rsp),%r12; shl $0x3c,%r12; mov 0x20(%rsp),%r13; shl $0x3d,%r13; mov 0x20(%rsp),%r15; shl $0x3e,%r15; or %rcx,%r15; or %r15,%r13; or %r13,%r12; or %r12,%r11; or %r11,%r10; or %r10,%r9; or %r9,%r8; or %r8,%rdi; or %rdi,%rsi; or %rsi,%rbx; or %rbx,%rdx; mov 0x30(%rsp),%rcx; or %rdx,%rcx; mov 0x38(%rsp),%rdx; or %rcx,%rdx; mov 0x40(%rsp),%rcx; or %rdx,%rcx; mov 0x48(%rsp),%rdx; or %rcx,%rdx; mov 0x50(%rsp),%rcx; or %rdx,%rcx; mov 0x58(%rsp),%rdx; or %rcx,%rdx; mov 0x60(%rsp),%rcx; or %rdx,%rcx; mov 0x68(%rsp),%rdx; or %rcx,%rdx; mov 0x70(%rsp),%rcx; or %rdx,%rcx; mov 0x78(%rsp),%rdx; or %rcx,%rdx; mov 0x80(%rsp),%rcx; or %rdx,%rcx; mov 0x88(%rsp),%rdx; or %rcx,%rdx; mov 0x90(%rsp),%rcx; or %rdx,%rcx; mov 0x98(%rsp),%rdx; or %rcx,%rdx; mov 0xa0(%rsp),%rcx; or %rdx,%rcx; mov 0xa8(%rsp),%rdx; or %rcx,%rdx; mov 0xb0(%rsp),%rcx; or %rdx,%rcx; mov (%rsp),%rdx; or %rcx,%rdx; mov 0x8(%rsp),%rcx; or %rdx,%rcx; mov 0x10(%rsp),%rdx; or %rdx,%rcx; mov 0x18(%rsp),%rdx; or %rdx,%rcx; mov 0x28(%rsp),%rdx; or %rdx,%rax; test %rcx,%rcx; je 47a923 <main.emu_idiv_gpr_one_32__reg_rax__go+0x2c3>; cmp $0xffffffffffffffff,%rcx; jne 47a913 <main.emu_idiv_gpr_one_32__reg_rax__go+0x2b3>; neg %rax; xor %edx,%edx; jmp 47a918 <main.emu_idiv_gpr_one_32__reg_rax__go+0x2b8>; cqto; idiv %rcx; mov %eax,%eax; add $0xb8,%rsp; pop %rbp; ret; call 43f360 <runtime.panicdivide>; nop; mov %eax,0x8(%rsp); mov %ebx,0xc(%rsp); mov %ecx,0x10(%rsp); call 475b80 <runtime.morestack_noctxt.abi0>; mov 0x8(%rsp),%eax; mov 0xc(%rsp),%ebx; mov 0x10(%rsp),%ecx; jmp 47a660 <main.emu_idiv_gpr_one_32__reg_rax__go>
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
lea -0x40(%rsp),%r12; cmp 0x10(%r14),%r12; jbe 47a929 <main.emu_idiv_gpr_one_32__reg_rax__go+0x2c9>; sub $0xb8,%rsp; shl $0x20,%rax; shr $0x1f,%ecx; and $0x1,%ecx; shl $0x3f,%rcx; shl $0x20,%rsi; shl $0x21,%rdi; shl $0x22,%r8; shl $0x23,%r9; shl $0x24,%r10; shl $0x25,%r11; shl $0x26,%r12; shl $0x27,%r13; shl $0x28,%r15; shl $0x29,%rdx; shl $0x2a,%rbx; shl $0x2b,%rsi; shl $0x2c,%rdi; shl $0x2d,%r8; shl $0x2e,%r9; shl $0x2f,%r10; shl $0x30,%r11; shl $0x31,%r12; shl $0x32,%r13; shl $0x33,%r15; shl $0x34,%rdx; shl $0x35,%rbx; shl $0x36,%rsi; shl $0x37,%rdi; shl $0x38,%r8; shl $0x39,%r9; shl $0x3a,%r10; shl $0x3b,%r11; shl $0x3c,%r12; shl $0x3d,%r13; shl $0x3e,%r15; or %rcx,%r15; or %r15,%r13; or %r13,%r12; or %r12,%r11; or %r11,%r10; or %r10,%r9; or %r9,%r8; or %r8,%rdi; or %rdi,%rsi; or %rsi,%rbx; or %rbx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rdx,%rcx; or %rdx,%rcx; or %rdx,%rax; test %rcx,%rcx; je 47a923 <main.emu_idiv_gpr_one_32__reg_rax__go+0x2c3>; cmp $0xffffffffffffffff,%rcx; jne 47a913 <main.emu_idiv_gpr_one_32__reg_rax__go+0x2b3>; neg %rax; xor %edx,%edx; jmp 47a918 <main.emu_idiv_gpr_one_32__reg_rax__go+0x2b8>; cqto; idiv %rcx; add $0xb8,%rsp; call 43f360 <runtime.panicdivide>; call 475b80 <runtime.morestack_noctxt.abi0>; jmp 47a660 <main.emu_idiv_gpr_one_32__reg_rax__go>
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (85 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **UNDECIDED** -- the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

Re-posed with more solver room (300000 ms instead of 3,000): **UNDECIDED** -- the solver did not answer inside its 300000 ms limit, so the verdict is undecided and never disproved

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdx | rax |
| IN-1 | rax | rbx |
| IN-2 | rdi | rcx |

#### place `reg_rdx`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, bvsrem_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, Extract(31, 0, bvsrem_i(Concat(Extract(31, 0, seed_rdx), Extract(31, 0, seed_rax)), Concat(Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 0, seed_rdi)))))
```

The source, LITERAL (`src3b/idiv_gpr_one_32__reg_rdx__go.go`):

```
// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of idiv_gpr_one_32__reg_rdx__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, bvsrem_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
package main

//go:noinline
func emu_idiv_gpr_one_32__reg_rdx__go(a uint32, b uint32, c uint32) uint64 {
	return uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64((uint64(uint64((int64((uint64(((uint64(uint32(a))) << 32) | (uint64(uint32(b))))))) % (int64((uint64(((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 63) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 62) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 61) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 60) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 59) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 58) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 57) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 56) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 55) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 54) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 53) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 52) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 51) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 50) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 49) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 48) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 47) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 46) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 45) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 44) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 43) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 42) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 41) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 40) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 39) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 38) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 37) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 36) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 35) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 34) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 33) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 32) | (uint64(uint32(c)))))))))))) >> 0)))))))
}

var g0 uint32
var g1 uint32
var g2 uint32
var sink interface{}

func main() {
	sink = emu_idiv_gpr_one_32__reg_rdx__go(g0, g1, g2)
	_ = sink
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
lea -0x40(%rsp),%r12; cmp 0x10(%r14),%r12; jbe 47a929 <main.emu_idiv_gpr_one_32__reg_rdx__go+0x2c9>; push %rbp; mov %rsp,%rbp; sub $0xb8,%rsp; mov %eax,%eax; shl $0x20,%rax; mov %ebx,%edx; mov %rdx,0x28(%rsp); mov %ecx,%ebx; shr $0x1f,%ecx; and $0x1,%ecx; mov %rcx,0x20(%rsp); mov %rcx,%rsi; shl $0x3f,%rcx; mov %ebx,%ebx; mov %rbx,0x18(%rsp); mov %rsi,%rdi; shl $0x20,%rsi; mov %rsi,0x10(%rsp); mov %rdi,%r8; shl $0x21,%rdi; mov %rdi,0x8(%rsp); mov %r8,%r9; shl $0x22,%r8; mov %r8,(%rsp); mov %r9,%r10; shl $0x23,%r9; mov %r9,0xb0(%rsp); mov %r10,%r11; shl $0x24,%r10; mov %r10,0xa8(%rsp); mov %r11,%r12; shl $0x25,%r11; mov %r11,0xa0(%rsp); mov %r12,%r13; shl $0x26,%r12; mov %r12,0x98(%rsp); mov %r13,%r15; shl $0x27,%r13; mov %r13,0x90(%rsp); shl $0x28,%r15; mov %r15,0x88(%rsp); mov 0x20(%rsp),%rdx; shl $0x29,%rdx; mov %rdx,0x80(%rsp); mov 0x20(%rsp),%rbx; shl $0x2a,%rbx; mov %rbx,0x78(%rsp); mov 0x20(%rsp),%rsi; shl $0x2b,%rsi; mov %rsi,0x70(%rsp); mov 0x20(%rsp),%rdi; shl $0x2c,%rdi; mov %rdi,0x68(%rsp); mov 0x20(%rsp),%r8; shl $0x2d,%r8; mov %r8,0x60(%rsp); mov 0x20(%rsp),%r9; shl $0x2e,%r9; mov %r9,0x58(%rsp); mov 0x20(%rsp),%r10; shl $0x2f,%r10; mov %r10,0x50(%rsp); mov 0x20(%rsp),%r11; shl $0x30,%r11; mov %r11,0x48(%rsp); mov 0x20(%rsp),%r12; shl $0x31,%r12; mov %r12,0x40(%rsp); mov 0x20(%rsp),%r13; shl $0x32,%r13; mov %r13,0x38(%rsp); mov 0x20(%rsp),%r15; shl $0x33,%r15; mov %r15,0x30(%rsp); mov 0x20(%rsp),%rdx; shl $0x34,%rdx; mov 0x20(%rsp),%rbx; shl $0x35,%rbx; mov 0x20(%rsp),%rsi; shl $0x36,%rsi; mov 0x20(%rsp),%rdi; shl $0x37,%rdi; mov 0x20(%rsp),%r8; shl $0x38,%r8; mov 0x20(%rsp),%r9; shl $0x39,%r9; mov 0x20(%rsp),%r10; shl $0x3a,%r10; mov 0x20(%rsp),%r11; shl $0x3b,%r11; mov 0x20(%rsp),%r12; shl $0x3c,%r12; mov 0x20(%rsp),%r13; shl $0x3d,%r13; mov 0x20(%rsp),%r15; shl $0x3e,%r15; or %rcx,%r15; or %r15,%r13; or %r13,%r12; or %r12,%r11; or %r11,%r10; or %r10,%r9; or %r9,%r8; or %r8,%rdi; or %rdi,%rsi; or %rsi,%rbx; or %rbx,%rdx; mov 0x30(%rsp),%rcx; or %rdx,%rcx; mov 0x38(%rsp),%rdx; or %rcx,%rdx; mov 0x40(%rsp),%rcx; or %rdx,%rcx; mov 0x48(%rsp),%rdx; or %rcx,%rdx; mov 0x50(%rsp),%rcx; or %rdx,%rcx; mov 0x58(%rsp),%rdx; or %rcx,%rdx; mov 0x60(%rsp),%rcx; or %rdx,%rcx; mov 0x68(%rsp),%rdx; or %rcx,%rdx; mov 0x70(%rsp),%rcx; or %rdx,%rcx; mov 0x78(%rsp),%rdx; or %rcx,%rdx; mov 0x80(%rsp),%rcx; or %rdx,%rcx; mov 0x88(%rsp),%rdx; or %rcx,%rdx; mov 0x90(%rsp),%rcx; or %rdx,%rcx; mov 0x98(%rsp),%rdx; or %rcx,%rdx; mov 0xa0(%rsp),%rcx; or %rdx,%rcx; mov 0xa8(%rsp),%rdx; or %rcx,%rdx; mov 0xb0(%rsp),%rcx; or %rdx,%rcx; mov (%rsp),%rdx; or %rcx,%rdx; mov 0x8(%rsp),%rcx; or %rdx,%rcx; mov 0x10(%rsp),%rdx; or %rdx,%rcx; mov 0x18(%rsp),%rdx; or %rdx,%rcx; mov 0x28(%rsp),%rdx; or %rdx,%rax; test %rcx,%rcx; je 47a923 <main.emu_idiv_gpr_one_32__reg_rdx__go+0x2c3>; cmp $0xffffffffffffffff,%rcx; jne 47a913 <main.emu_idiv_gpr_one_32__reg_rdx__go+0x2b3>; neg %rax; xor %edx,%edx; jmp 47a918 <main.emu_idiv_gpr_one_32__reg_rdx__go+0x2b8>; cqto; idiv %rcx; mov %edx,%eax; add $0xb8,%rsp; pop %rbp; ret; call 43f360 <runtime.panicdivide>; nop; mov %eax,0x8(%rsp); mov %ebx,0xc(%rsp); mov %ecx,0x10(%rsp); call 475b80 <runtime.morestack_noctxt.abi0>; mov 0x8(%rsp),%eax; mov 0xc(%rsp),%ebx; mov 0x10(%rsp),%ecx; jmp 47a660 <main.emu_idiv_gpr_one_32__reg_rdx__go>
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
lea -0x40(%rsp),%r12; cmp 0x10(%r14),%r12; jbe 47a929 <main.emu_idiv_gpr_one_32__reg_rdx__go+0x2c9>; sub $0xb8,%rsp; shl $0x20,%rax; shr $0x1f,%ecx; and $0x1,%ecx; shl $0x3f,%rcx; shl $0x20,%rsi; shl $0x21,%rdi; shl $0x22,%r8; shl $0x23,%r9; shl $0x24,%r10; shl $0x25,%r11; shl $0x26,%r12; shl $0x27,%r13; shl $0x28,%r15; shl $0x29,%rdx; shl $0x2a,%rbx; shl $0x2b,%rsi; shl $0x2c,%rdi; shl $0x2d,%r8; shl $0x2e,%r9; shl $0x2f,%r10; shl $0x30,%r11; shl $0x31,%r12; shl $0x32,%r13; shl $0x33,%r15; shl $0x34,%rdx; shl $0x35,%rbx; shl $0x36,%rsi; shl $0x37,%rdi; shl $0x38,%r8; shl $0x39,%r9; shl $0x3a,%r10; shl $0x3b,%r11; shl $0x3c,%r12; shl $0x3d,%r13; shl $0x3e,%r15; or %rcx,%r15; or %r15,%r13; or %r13,%r12; or %r12,%r11; or %r11,%r10; or %r10,%r9; or %r9,%r8; or %r8,%rdi; or %rdi,%rsi; or %rsi,%rbx; or %rbx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rcx,%rdx; or %rdx,%rcx; or %rdx,%rcx; or %rdx,%rcx; or %rdx,%rax; test %rcx,%rcx; je 47a923 <main.emu_idiv_gpr_one_32__reg_rdx__go+0x2c3>; cmp $0xffffffffffffffff,%rcx; jne 47a913 <main.emu_idiv_gpr_one_32__reg_rdx__go+0x2b3>; neg %rax; xor %edx,%edx; jmp 47a918 <main.emu_idiv_gpr_one_32__reg_rdx__go+0x2b8>; cqto; idiv %rcx; add $0xb8,%rsp; call 43f360 <runtime.panicdivide>; call 475b80 <runtime.morestack_noctxt.abi0>; jmp 47a660 <main.emu_idiv_gpr_one_32__reg_rdx__go>
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (85 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **UNDECIDED** -- the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

Re-posed with more solver room (300000 ms instead of 3,000): **UNDECIDED** -- the solver did not answer inside its 300000 ms limit, so the verdict is undecided and never disproved

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdx | rax |
| IN-1 | rax | rbx |
| IN-2 | rdi | rcx |

### 1.24 `idiv` gpr_one 32 -> swift

The row, LITERAL: `idiv %edi` (`r07409`), chosen: the one TRANSLATED row at this cell.

The corpus's attestation of this cell: 389 unit(s), 778 ledger row(s).

#### place `reg_rax`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, seed_rdx), Extract(31, 0, seed_rax)), Concat(Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 0, seed_rdi)))))
```

The source, LITERAL (`src3b/idiv_gpr_one_32__reg_rax__swift.swift`):

```
// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of idiv_gpr_one_32__reg_rax__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
@_cdecl("emu_idiv_gpr_one_32__reg_rax__swift")
public func emu_idiv_gpr_one_32__reg_rax__swift(_ a: UInt32, _ b: UInt32, _ c: UInt32) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: UInt64(bitPattern: ((Int64(bitPattern: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: (UInt32(a)))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32(b))))))))) / ((Int64(bitPattern: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 63) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 62) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 61) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 60) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 59) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 58) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 57) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 56) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 55) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 54) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 53) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 52) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 51) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 50) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 49) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 48) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 47) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 46) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 45) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 44) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 43) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 42) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 41) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 40) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 39) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 38) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 37) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 36) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 35) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 34) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 33) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32(c)))))))))))))) &>> 0)))))))
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
jmp 5 <emu_idiv_gpr_one_32__reg_rax__swift+0x5> !!reloc=R_X86_64_PLT32:$s9unit_ship35emu_idiv_gpr_one_32__reg_rax__swiftys6UInt64Vs6UInt32V_A2FtF-0x4
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
jmp 5 <emu_idiv_gpr_one_32__reg_rax__swift+0x5> !!reloc=R_X86_64_PLT32:$s9unit_ship35emu_idiv_gpr_one_32__reg_rax__swiftys6UInt64Vs6UInt32V_A2FtF-0x4
```

Against the cell's own arch opcode: **LANDED_ELSEWHERE** (landed on `jmp`).

**Step 4, the check.** . Verdict: **UNDECIDED** -- the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either

Re-posed with more solver room (300000 ms instead of 3,000): **UNDECIDED** -- the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either

#### place `reg_rdx`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, Extract(31, 0, bvsrem_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, Extract(31, 0, bvsrem_i(Concat(Extract(31, 0, seed_rdx), Extract(31, 0, seed_rax)), Concat(Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 31, seed_rdi), Extract(31, 0, seed_rdi)))))
```

The source, LITERAL (`src3b/idiv_gpr_one_32__reg_rdx__swift.swift`):

```
// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of idiv_gpr_one_32__reg_rdx__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, bvsrem_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
@_cdecl("emu_idiv_gpr_one_32__reg_rdx__swift")
public func emu_idiv_gpr_one_32__reg_rdx__swift(_ a: UInt32, _ b: UInt32, _ c: UInt32) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: UInt64(bitPattern: ((Int64(bitPattern: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: (UInt32(a)))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32(b))))))))) % ((Int64(bitPattern: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 63) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 62) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 61) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 60) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 59) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 58) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 57) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 56) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 55) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 54) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 53) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 52) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 51) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 50) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 49) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 48) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 47) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 46) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 45) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 44) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 43) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 42) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 41) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 40) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 39) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 38) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 37) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 36) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 35) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 34) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 33) | ((UInt64(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ((UInt32(c))) &>> 31)) & UInt32(0x1)))) &<< 32) | (UInt64(truncatingIfNeeded: (UInt32(c)))))))))))))) &>> 0)))))))
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
jmp 5 <emu_idiv_gpr_one_32__reg_rdx__swift+0x5> !!reloc=R_X86_64_PLT32:$s9unit_ship35emu_idiv_gpr_one_32__reg_rdx__swiftys6UInt64Vs6UInt32V_A2FtF-0x4
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
jmp 5 <emu_idiv_gpr_one_32__reg_rdx__swift+0x5> !!reloc=R_X86_64_PLT32:$s9unit_ship35emu_idiv_gpr_one_32__reg_rdx__swiftys6UInt64Vs6UInt32V_A2FtF-0x4
```

Against the cell's own arch opcode: **LANDED_ELSEWHERE** (landed on `jmp`).

**Step 4, the check.** . Verdict: **UNDECIDED** -- the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either

Re-posed with more solver room (300000 ms instead of 3,000): **UNDECIDED** -- the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either

### 1.25 `cmovne` gpr_gpr 32 -> c

The row, LITERAL: `cmovne %esi,%edi` (`r27756`), chosen: of the 11 TRANSLATED rows at this cell, the one whose arriving flag state was written by the setter the cell's own attestation records the most ledger rows for.

The corpus's attestation of this cell: 2 unit(s), 2 ledger row(s).

This cell's mapping reads the flags, so the PAIR is rendered as one function. The setter this cell's attestation records the most ledger rows for is `test`; its own row is `r14507`, LITERAL: `test %esi,%edi`. The composition, LITERAL:

```
seed_FLAG_L := Extract(31, 0, seed_rdx) & Extract(31, 0, seed_rcx) ; seed_FLAG_R := 0
```

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, If(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)) == 0, Extract(31, 0, v2), Extract(31, 0, v3)))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, If(~(~Extract(31, 0, seed_rcx) | ~Extract(31, 0, seed_rdx)) == 0, Extract(31, 0, seed_rdi), Extract(31, 0, seed_rsi)))
```

The source, LITERAL (`src3b/cmovne_gpr_gpr_32__reg_rdi__c.c`):

```
/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of cmovne_gpr_gpr_32__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(0, If(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)) == 0, Extract(31, 0, v2), Extract(31, 0, v3))) */
#include <stdint.h>

uint64_t
emu_cmovne_gpr_gpr_32__reg_rdi__c(uint32_t a, uint32_t b, uint32_t c, uint32_t d)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)(((((uint32_t)((uint32_t)(~(uint32_t)((uint32_t)((uint32_t)((uint32_t)(~(uint32_t)((uint32_t)b))) | (uint32_t)((uint32_t)(~(uint32_t)((uint32_t)a))))))) == (uint32_t)(UINT32_C(0x0)))) ? (uint32_t)((uint32_t)d) : (uint32_t)((uint32_t)c)))));
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov %edx,%eax; test %edi,%esi; cmove %ecx,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
test %edi,%esi; cmove %ecx,%eax
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (2 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdx | rdi |
| IN-1 | rcx | rsi |
| IN-2 | rsi | rdx |
| IN-3 | rdi | rcx |

#### place `flags`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)), 0)
```

**Step 2, the render.** REFUSED: the flags place of a preseeded row is the flag state that ARRIVED, not a place this opcode writes (None).

### 1.26 `cmovne` gpr_gpr 32 -> rust

The row, LITERAL: `cmovne %esi,%edi` (`r27756`), chosen: of the 11 TRANSLATED rows at this cell, the one whose arriving flag state was written by the setter the cell's own attestation records the most ledger rows for.

The corpus's attestation of this cell: 2 unit(s), 2 ledger row(s).

This cell's mapping reads the flags, so the PAIR is rendered as one function. The setter this cell's attestation records the most ledger rows for is `test`; its own row is `r14507`, LITERAL: `test %esi,%edi`. The composition, LITERAL:

```
seed_FLAG_L := Extract(31, 0, seed_rdx) & Extract(31, 0, seed_rcx) ; seed_FLAG_R := 0
```

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, If(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)) == 0, Extract(31, 0, v2), Extract(31, 0, v3)))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, If(~(~Extract(31, 0, seed_rcx) | ~Extract(31, 0, seed_rdx)) == 0, Extract(31, 0, seed_rdi), Extract(31, 0, seed_rsi)))
```

The source, LITERAL (`src3b/cmovne_gpr_gpr_32__reg_rdi__rust.rs`):

```
#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of cmovne_gpr_gpr_32__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)) == 0, Extract(31, 0, v2), Extract(31, 0, v3)))
#[no_mangle]
pub extern "C" fn emu_cmovne_gpr_gpr_32__reg_rdi__rust(a: u32, b: u32, c: u32, d: u32) -> u64
{
    (((((((0x0u32) as u64) << 32) | (((if ((((((!((((((((!(((b as u32)) as u32)) as u32)) as u32) | ((((!(((a as u32)) as u32)) as u32)) as u32)) as u32)) as u32)) as u32)) as u32) == ((0x0u32) as u32))) { (((d as u32)) as u32) } else { (((c as u32)) as u32) })) as u64)) as u64)) as u64)
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov %edx,%eax; test %edi,%esi; cmove %ecx,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
test %edi,%esi; cmove %ecx,%eax
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (2 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdx | rdi |
| IN-1 | rcx | rsi |
| IN-2 | rsi | rdx |
| IN-3 | rdi | rcx |

#### place `flags`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)), 0)
```

**Step 2, the render.** REFUSED: the flags place of a preseeded row is the flag state that ARRIVED, not a place this opcode writes (None).

### 1.27 `cmovne` gpr_gpr 32 -> go

The row, LITERAL: `cmovne %esi,%edi` (`r27756`), chosen: of the 11 TRANSLATED rows at this cell, the one whose arriving flag state was written by the setter the cell's own attestation records the most ledger rows for.

The corpus's attestation of this cell: 2 unit(s), 2 ledger row(s).

This cell's mapping reads the flags, so the PAIR is rendered as one function. The setter this cell's attestation records the most ledger rows for is `test`; its own row is `r14507`, LITERAL: `test %esi,%edi`. The composition, LITERAL:

```
seed_FLAG_L := Extract(31, 0, seed_rdx) & Extract(31, 0, seed_rcx) ; seed_FLAG_R := 0
```

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, If(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)) == 0, Extract(31, 0, v2), Extract(31, 0, v3)))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, If(~(~Extract(31, 0, seed_rcx) | ~Extract(31, 0, seed_rdx)) == 0, Extract(31, 0, seed_rdi), Extract(31, 0, seed_rsi)))
```

The source, LITERAL (`src3b/cmovne_gpr_gpr_32__reg_rdi__go.go`):

```
// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of cmovne_gpr_gpr_32__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)) == 0, Extract(31, 0, v2), Extract(31, 0, v3)))
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_cmovne_gpr_gpr_32__reg_rdi__go(a uint32, b uint32, c uint32, d uint32) uint64 {
	return uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64(sel32(((uint32((uint32(^(uint32((uint32((uint32((uint32(^(uint32(uint32(b))))))) | (uint32((uint32(^(uint32(uint32(a))))))))))))))) == (uint32(uint32(0x0)))), uint32(uint32(d)), uint32(uint32(c))))))))
}

var g0 uint32
var g1 uint32
var g2 uint32
var g3 uint32
var sink interface{}

func main() {
	sink = emu_cmovne_gpr_gpr_32__reg_rdi__go(g0, g1, g2, g3)
	_ = sink
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
test %ebx,%eax; cmove %edi,%ecx; mov %ecx,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
test %ebx,%eax; cmove %edi,%ecx
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (2 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdx | rax |
| IN-1 | rcx | rbx |
| IN-2 | rsi | rcx |
| IN-3 | rdi | rdi |

#### place `flags`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)), 0)
```

**Step 2, the render.** REFUSED: the flags place of a preseeded row is the flag state that ARRIVED, not a place this opcode writes (None).

### 1.28 `cmovne` gpr_gpr 32 -> swift

The row, LITERAL: `cmovne %esi,%edi` (`r27756`), chosen: of the 11 TRANSLATED rows at this cell, the one whose arriving flag state was written by the setter the cell's own attestation records the most ledger rows for.

The corpus's attestation of this cell: 2 unit(s), 2 ledger row(s).

This cell's mapping reads the flags, so the PAIR is rendered as one function. The setter this cell's attestation records the most ledger rows for is `test`; its own row is `r14507`, LITERAL: `test %esi,%edi`. The composition, LITERAL:

```
seed_FLAG_L := Extract(31, 0, seed_rdx) & Extract(31, 0, seed_rcx) ; seed_FLAG_R := 0
```

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, If(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)) == 0, Extract(31, 0, v2), Extract(31, 0, v3)))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, If(~(~Extract(31, 0, seed_rcx) | ~Extract(31, 0, seed_rdx)) == 0, Extract(31, 0, seed_rdi), Extract(31, 0, seed_rsi)))
```

The source, LITERAL (`src3b/cmovne_gpr_gpr_32__reg_rdi__swift.swift`):

```
// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of cmovne_gpr_gpr_32__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)) == 0, Extract(31, 0, v2), Extract(31, 0, v3)))
@_cdecl("emu_cmovne_gpr_gpr_32__reg_rdi__swift")
public func emu_cmovne_gpr_gpr_32__reg_rdi__swift(_ a: UInt32, _ b: UInt32, _ c: UInt32, _ d: UInt32) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) | (UInt64(truncatingIfNeeded: ((((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: (UInt32(b)))))))) | (UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: (UInt32(a)))))))))))))))) == (UInt32(truncatingIfNeeded: UInt32(0x0))))) ? ((UInt32(d))) : ((UInt32(c)))))))))
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
mov %edx,%eax; test %edi,%esi; cmove %ecx,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
test %edi,%esi; cmove %ecx,%eax
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (2 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdx | rdi |
| IN-1 | rcx | rsi |
| IN-2 | rsi | rdx |
| IN-3 | rdi | rcx |

#### place `flags`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(~(~Extract(31, 0, v0) | ~Extract(31, 0, v1)), 0)
```

**Step 2, the render.** REFUSED: the flags place of a preseeded row is the flag state that ARRIVED, not a place this opcode writes (None).

### 1.29 `setne` gpr_one 8 -> c

The row, LITERAL: `setne %dil` (`r64972`), chosen: of the 11 TRANSLATED rows at this cell, the one whose arriving flag state was written by the setter the cell's own attestation records the most ledger rows for.

The corpus's attestation of this cell: 6691 unit(s), 10335 ledger row(s).

This cell's mapping reads the flags, so the PAIR is rendered as one function. The setter this cell's attestation records the most ledger rows for is `test`; its own row is `r14461`, LITERAL: `test %sil,%dil`. The composition, LITERAL:

```
seed_FLAG_L := Extract(7, 0, seed_rdi) & Extract(7, 0, seed_rsi) ; seed_FLAG_R := 0
```

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, If(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)) == 0, 0, 1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, If(~(~Extract(7, 0, seed_rdi) | ~Extract(7, 0, seed_rsi)) == 0, 0, 1))
```

The source, LITERAL (`src3b/setne_gpr_one_8__reg_rdi__c.c`):

```
/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of setne_gpr_one_8__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(0, If(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)) == 0, 0, 1)) */
#include <stdint.h>

uint64_t
emu_setne_gpr_one_8__reg_rdi__c(uint8_t a, uint8_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 8) | (uint64_t)(((((uint32_t)(((uint32_t)(~(uint32_t)(((uint32_t)((uint32_t)(((uint32_t)(~(uint32_t)((uint32_t)a)) & UINT32_C(0xff))) | (uint32_t)(((uint32_t)(~(uint32_t)((uint32_t)b)) & UINT32_C(0xff)))) & UINT32_C(0xff)))) & UINT32_C(0xff))) == (uint32_t)(UINT32_C(0x0)))) ? (uint32_t)(UINT32_C(0x0)) : (uint32_t)(UINT32_C(0x1))))));
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
xor %eax,%eax; test %edi,%esi; setne %al; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
xor %eax,%eax; test %edi,%esi; setne %al
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (3 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **DISPROVED** -- z3 found a starting state under which the two sides differ

Widths: the cell's place is 64 bits and the carved body answers 8, so the gate's own rule cut both to 8.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rsi | rsi |

The counterexample, LITERAL:

```
[IN_1 = 3841776640, IN_0 = 3841776640]
```

Re-posed with every narrow-holder input row zero-extended from its holder width: **PROVED_ON_SHIP** -- z3 proved the two equal for every input whose narrow arguments are zero-extended to the register

#### place `flags`, 16 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)), 0)
```

**Step 2, the render.** REFUSED: the flags place of a preseeded row is the flag state that ARRIVED, not a place this opcode writes (None).

### 1.30 `setne` gpr_one 8 -> rust

The row, LITERAL: `setne %dil` (`r64972`), chosen: of the 11 TRANSLATED rows at this cell, the one whose arriving flag state was written by the setter the cell's own attestation records the most ledger rows for.

The corpus's attestation of this cell: 6691 unit(s), 10335 ledger row(s).

This cell's mapping reads the flags, so the PAIR is rendered as one function. The setter this cell's attestation records the most ledger rows for is `test`; its own row is `r14461`, LITERAL: `test %sil,%dil`. The composition, LITERAL:

```
seed_FLAG_L := Extract(7, 0, seed_rdi) & Extract(7, 0, seed_rsi) ; seed_FLAG_R := 0
```

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, If(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)) == 0, 0, 1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, If(~(~Extract(7, 0, seed_rdi) | ~Extract(7, 0, seed_rsi)) == 0, 0, 1))
```

The source, LITERAL (`src3b/setne_gpr_one_8__reg_rdi__rust.rs`):

```
#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of setne_gpr_one_8__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)) == 0, 0, 1))
#[no_mangle]
pub extern "C" fn emu_setne_gpr_one_8__reg_rdi__rust(a: u8, b: u8) -> u64
{
    (((((((0x0u64) as u64) << 8) | (((if (((((((!((((((((((!(((a as u32)) as u32)) as u32) & 0xffu32)) as u32) | (((((!(((b as u32)) as u32)) as u32) & 0xffu32)) as u32)) as u32) & 0xffu32)) as u32)) as u32) & 0xffu32)) as u32) == ((0x0u32) as u32))) { ((0x0u32) as u32) } else { ((0x1u32) as u32) })) as u64)) as u64)) as u64)
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
xor %eax,%eax; test %edi,%esi; setne %al; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
xor %eax,%eax; test %edi,%esi; setne %al
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (3 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **DISPROVED** -- z3 found a starting state under which the two sides differ

Widths: the cell's place is 64 bits and the carved body answers 8, so the gate's own rule cut both to 8.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rsi | rsi |

The counterexample, LITERAL:

```
[IN_1 = 3841776640, IN_0 = 3841776640]
```

Re-posed with every narrow-holder input row zero-extended from its holder width: **PROVED_ON_SHIP** -- z3 proved the two equal for every input whose narrow arguments are zero-extended to the register

#### place `flags`, 16 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)), 0)
```

**Step 2, the render.** REFUSED: the flags place of a preseeded row is the flag state that ARRIVED, not a place this opcode writes (None).

### 1.31 `setne` gpr_one 8 -> go

The row, LITERAL: `setne %dil` (`r64972`), chosen: of the 11 TRANSLATED rows at this cell, the one whose arriving flag state was written by the setter the cell's own attestation records the most ledger rows for.

The corpus's attestation of this cell: 6691 unit(s), 10335 ledger row(s).

This cell's mapping reads the flags, so the PAIR is rendered as one function. The setter this cell's attestation records the most ledger rows for is `test`; its own row is `r14461`, LITERAL: `test %sil,%dil`. The composition, LITERAL:

```
seed_FLAG_L := Extract(7, 0, seed_rdi) & Extract(7, 0, seed_rsi) ; seed_FLAG_R := 0
```

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, If(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)) == 0, 0, 1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, If(~(~Extract(7, 0, seed_rdi) | ~Extract(7, 0, seed_rsi)) == 0, 0, 1))
```

The source, LITERAL (`src3b/setne_gpr_one_8__reg_rdi__go.go`):

```
// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of setne_gpr_one_8__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)) == 0, 0, 1))
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_setne_gpr_one_8__reg_rdi__go(a uint8, b uint8) uint64 {
	return uint64((uint64(((uint64(uint64(0x0))) << 8) | (uint64(sel32(((uint32(((uint32(^(uint32(((uint32((uint32(((uint32(^(uint32(uint32(a))))) & uint32(0xff)))) | (uint32(((uint32(^(uint32(uint32(b))))) & uint32(0xff)))))) & uint32(0xff)))))) & uint32(0xff)))) == (uint32(uint32(0x0)))), uint32(uint32(0x0)), uint32(uint32(0x1))))))))
}

var g0 uint8
var g1 uint8
var sink interface{}

func main() {
	sink = emu_setne_gpr_one_8__reg_rdi__go(g0, g1)
	_ = sink
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
movzbl %al,%ecx; not %ecx; movzbl %cl,%ecx; movzbl %bl,%edx; not %edx; movzbl %dl,%edx; or %edx,%ecx; movzbl %cl,%ecx; not %ecx; movzbl %cl,%ecx; test %ecx,%ecx; setne %cl; movzbl %cl,%eax; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
movzbl %al,%ecx; not %ecx; movzbl %cl,%ecx; movzbl %bl,%edx; not %edx; movzbl %dl,%edx; or %edx,%ecx; movzbl %cl,%ecx; not %ecx; movzbl %cl,%ecx; test %ecx,%ecx; setne %cl; movzbl %cl,%eax
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (13 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

Widths: the cell's place is 64 bits and the carved body answers 32, so the gate's own rule cut both to 32.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rax |
| IN-1 | rsi | rbx |

#### place `flags`, 16 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)), 0)
```

**Step 2, the render.** REFUSED: the flags place of a preseeded row is the flag state that ARRIVED, not a place this opcode writes (None).

### 1.32 `setne` gpr_one 8 -> swift

The row, LITERAL: `setne %dil` (`r64972`), chosen: of the 11 TRANSLATED rows at this cell, the one whose arriving flag state was written by the setter the cell's own attestation records the most ledger rows for.

The corpus's attestation of this cell: 6691 unit(s), 10335 ledger row(s).

This cell's mapping reads the flags, so the PAIR is rendered as one function. The setter this cell's attestation records the most ledger rows for is `test`; its own row is `r14461`, LITERAL: `test %sil,%dil`. The composition, LITERAL:

```
seed_FLAG_L := Extract(7, 0, seed_rdi) & Extract(7, 0, seed_rsi) ; seed_FLAG_R := 0
```

#### place `reg_rdi`, 64 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(0, If(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)) == 0, 0, 1))
```

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
Concat(0, If(~(~Extract(7, 0, seed_rdi) | ~Extract(7, 0, seed_rsi)) == 0, 0, 1))
```

The source, LITERAL (`src3b/setne_gpr_one_8__reg_rdi__swift.swift`):

```
// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of setne_gpr_one_8__reg_rdi__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)) == 0, 0, 1))
@_cdecl("emu_setne_gpr_one_8__reg_rdi__swift")
public func emu_setne_gpr_one_8__reg_rdi__swift(_ a: UInt8, _ b: UInt8) -> UInt64
{
    return UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt64(0x0))) &<< 8) | (UInt64(truncatingIfNeeded: ((((UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: (UInt32(a)))))) & UInt32(0xff)))) | (UInt32(truncatingIfNeeded: ((UInt32(truncatingIfNeeded: ~(UInt32(truncatingIfNeeded: (UInt32(b)))))) & UInt32(0xff)))))) & UInt32(0xff)))))) & UInt32(0xff)))) == (UInt32(truncatingIfNeeded: UInt32(0x0))))) ? (UInt32(0x0)) : (UInt32(0x1))))))))
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
xor %eax,%eax; test %edi,%esi; setne %al; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
xor %eax,%eax; test %edi,%esi; setne %al
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (3 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **DISPROVED** -- z3 found a starting state under which the two sides differ

Widths: the cell's place is 64 bits and the carved body answers 8, so the gate's own rule cut both to 8.

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |
| IN-1 | rsi | rsi |

The counterexample, LITERAL:

```
[IN_1 = 3841776640, IN_0 = 3841776640]
```

Re-posed with every narrow-holder input row zero-extended from its holder width: **PROVED_ON_SHIP** -- z3 proved the two equal for every input whose narrow arguments are zero-extended to the register

#### place `flags`, 16 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)), 0)
```

**Step 2, the render.** REFUSED: the flags place of a preseeded row is the flag state that ARRIVED, not a place this opcode writes (None).

### 1.33 `addss` xmm_xmm 32 -> c

The row, LITERAL: `addss %xmm1,%xmm0` (`r00332`), chosen: of the 4 TRANSLATED rows at this cell, the one whose own sweep width equals the cell's key_width.

The corpus's attestation of this cell: 198 unit(s), 210 ledger row(s).

#### place `reg_xmm0`, 128 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(127, 32, v0), fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1))))
```

**Fix 2, the lane.** This place is a vector register, 128 bits, and the cell's own `key_width` is 32, so the driver rendered `Extract(31, 0, the cell's own term for this place)`. The projected lane, LITERAL:

```
fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1)))
```

The bits above the lane, LITERAL: `Extract(127, 32, v0)` -- put to the gate against `Extract(127, 32, seed_xmm0)`: **PROVED_ON_SHIP**.

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
fp.to_ieee_bv(fpToFP(Extract(31, 0, seed_xmm0)) + fpToFP(Extract(31, 0, seed_xmm1)))
```

The source, LITERAL (`src3b/addss_xmm_xmm_32__reg_xmm0__c.c`):

```
/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of addss_xmm_xmm_32__reg_xmm0__c.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1))) */
#include <stdint.h>
#include <string.h>
static inline float bits_to_f32(uint32_t b) { float f; memcpy(&f, &b, 4); return f; }
static inline uint32_t f32_to_bits(float f) { uint32_t b; memcpy(&b, &f, 4); return b; }

float
emu_addss_xmm_xmm_32__reg_xmm0__c(float a, float b)
{
    return bits_to_f32((uint32_t)((uint32_t)f32_to_bits(((float)((b) + (a))))));
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
addss %xmm1,%xmm0; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
addss %xmm1,%xmm0
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | xmm1 | xmm0 |
| IN-1 | xmm0 | xmm1 |

### 1.34 `addss` xmm_xmm 32 -> rust

The row, LITERAL: `addss %xmm1,%xmm0` (`r00332`), chosen: of the 4 TRANSLATED rows at this cell, the one whose own sweep width equals the cell's key_width.

The corpus's attestation of this cell: 198 unit(s), 210 ledger row(s).

#### place `reg_xmm0`, 128 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(127, 32, v0), fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1))))
```

**Fix 2, the lane.** This place is a vector register, 128 bits, and the cell's own `key_width` is 32, so the driver rendered `Extract(31, 0, the cell's own term for this place)`. The projected lane, LITERAL:

```
fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1)))
```

The bits above the lane, LITERAL: `Extract(127, 32, v0)` -- put to the gate against `Extract(127, 32, seed_xmm0)`: **PROVED_ON_SHIP**.

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
fp.to_ieee_bv(fpToFP(Extract(31, 0, seed_xmm0)) + fpToFP(Extract(31, 0, seed_xmm1)))
```

The source, LITERAL (`src3b/addss_xmm_xmm_32__reg_xmm0__rust.rs`):

```
#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of addss_xmm_xmm_32__reg_xmm0__rust.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1)))
#[no_mangle]
pub extern "C" fn emu_addss_xmm_xmm_32__reg_xmm0__rust(a: f32, b: f32) -> f32
{
    f32::from_bits((((((b) + (a))).to_bits() as u32)) as u32)
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
addss %xmm1,%xmm0; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
addss %xmm1,%xmm0
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | xmm1 | xmm0 |
| IN-1 | xmm0 | xmm1 |

### 1.35 `addss` xmm_xmm 32 -> go

The row, LITERAL: `addss %xmm1,%xmm0` (`r00332`), chosen: of the 4 TRANSLATED rows at this cell, the one whose own sweep width equals the cell's key_width.

The corpus's attestation of this cell: 198 unit(s), 210 ledger row(s).

#### place `reg_xmm0`, 128 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(127, 32, v0), fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1))))
```

**Fix 2, the lane.** This place is a vector register, 128 bits, and the cell's own `key_width` is 32, so the driver rendered `Extract(31, 0, the cell's own term for this place)`. The projected lane, LITERAL:

```
fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1)))
```

The bits above the lane, LITERAL: `Extract(127, 32, v0)` -- put to the gate against `Extract(127, 32, seed_xmm0)`: **PROVED_ON_SHIP**.

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
fp.to_ieee_bv(fpToFP(Extract(31, 0, seed_xmm0)) + fpToFP(Extract(31, 0, seed_xmm1)))
```

The source, LITERAL (`src3b/addss_xmm_xmm_32__reg_xmm0__go.go`):

```
// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of addss_xmm_xmm_32__reg_xmm0__go.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1)))
package main

import "math"

//go:noinline
func emu_addss_xmm_xmm_32__reg_xmm0__go(a float32, b float32) float32 {
	return math.Float32frombits(uint32(uint32(math.Float32bits(((b) + (a))))))
}

var g0 float32
var g1 float32
var sink interface{}

func main() {
	sink = emu_addss_xmm_xmm_32__reg_xmm0__go(g0, g1)
	_ = sink
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
push %rbp; mov %rsp,%rbp; sub $0x8,%rsp; addss %xmm0,%xmm1; movss %xmm1,0x4(%rsp); movss 0x4(%rsp),%xmm0; add $0x8,%rsp; pop %rbp; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
sub $0x8,%rsp; addss %xmm0,%xmm1; add $0x8,%rsp
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (3 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | xmm1 | xmm0 |
| IN-1 | xmm0 | xmm1 |

### 1.36 `addss` xmm_xmm 32 -> swift

The row, LITERAL: `addss %xmm1,%xmm0` (`r00332`), chosen: of the 4 TRANSLATED rows at this cell, the one whose own sweep width equals the cell's key_width.

The corpus's attestation of this cell: 198 unit(s), 210 ledger row(s).

#### place `reg_xmm0`, 128 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(127, 32, v0), fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1))))
```

**Fix 2, the lane.** This place is a vector register, 128 bits, and the cell's own `key_width` is 32, so the driver rendered `Extract(31, 0, the cell's own term for this place)`. The projected lane, LITERAL:

```
fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1)))
```

The bits above the lane, LITERAL: `Extract(127, 32, v0)` -- put to the gate against `Extract(127, 32, seed_xmm0)`: **PROVED_ON_SHIP**.

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
fp.to_ieee_bv(fpToFP(Extract(31, 0, seed_xmm0)) + fpToFP(Extract(31, 0, seed_xmm1)))
```

The source, LITERAL (`src3b/addss_xmm_xmm_32__reg_xmm0__swift.swift`):

```
// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of addss_xmm_xmm_32__reg_xmm0__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1)))
@_cdecl("emu_addss_xmm_xmm_32__reg_xmm0__swift")
public func emu_addss_xmm_xmm_32__reg_xmm0__swift(_ a: Float, _ b: Float) -> Float
{
    return Float(bitPattern: UInt32(truncatingIfNeeded: (UInt32((((b) + (a))).bitPattern))))
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
addss %xmm1,%xmm0; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
addss %xmm1,%xmm0
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | xmm1 | xmm0 |
| IN-1 | xmm0 | xmm1 |

### 1.37 `cvtsi2sd` gpr_xmm 64 -> c

The row, LITERAL: `cvtsi2sd %rdi,%xmm0` (`r02658`), chosen: of the 4 TRANSLATED rows at this cell, the one whose own sweep width equals the cell's key_width.

The corpus's attestation of this cell: 860 unit(s), 860 ledger row(s).

#### place `reg_xmm0`, 128 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(127, 64, v0), fp.to_ieee_bv(fpToFP(RNE(), v1)))
```

**Fix 2, the lane.** This place is a vector register, 128 bits, and the cell's own `key_width` is 64, so the driver rendered `Extract(63, 0, the cell's own term for this place)`. The projected lane, LITERAL:

```
fp.to_ieee_bv(fpToFP(RNE(), v0))
```

The bits above the lane, LITERAL: `Extract(127, 64, v0)` -- put to the gate against `Extract(127, 64, seed_xmm0)`: **PROVED_ON_SHIP**.

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
fp.to_ieee_bv(fpToFP(RNE(), seed_rdi))
```

The source, LITERAL (`src3b/cvtsi2sd_gpr_xmm_64__reg_xmm0__c.c`):

```
/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of cvtsi2sd_gpr_xmm_64__reg_xmm0__c.  The term's layer-5 text, LITERAL:
   fp.to_ieee_bv(fpToFP(RNE(), v0)) */
#include <stdint.h>
#include <string.h>
static inline double bits_to_f64(uint64_t b) { double f; memcpy(&f, &b, 8); return f; }
static inline uint64_t f64_to_bits(double f) { uint64_t b; memcpy(&b, &f, 8); return b; }

double
emu_cvtsi2sd_gpr_xmm_64__reg_xmm0__c(uint64_t a)
{
    return bits_to_f64((uint64_t)((uint64_t)f64_to_bits(((double)(int64_t)((uint64_t)a)))));
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
cvtsi2sd %rdi,%xmm0; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
cvtsi2sd %rdi,%xmm0
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |

### 1.38 `cvtsi2sd` gpr_xmm 64 -> rust

The row, LITERAL: `cvtsi2sd %rdi,%xmm0` (`r02658`), chosen: of the 4 TRANSLATED rows at this cell, the one whose own sweep width equals the cell's key_width.

The corpus's attestation of this cell: 860 unit(s), 860 ledger row(s).

#### place `reg_xmm0`, 128 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(127, 64, v0), fp.to_ieee_bv(fpToFP(RNE(), v1)))
```

**Fix 2, the lane.** This place is a vector register, 128 bits, and the cell's own `key_width` is 64, so the driver rendered `Extract(63, 0, the cell's own term for this place)`. The projected lane, LITERAL:

```
fp.to_ieee_bv(fpToFP(RNE(), v0))
```

The bits above the lane, LITERAL: `Extract(127, 64, v0)` -- put to the gate against `Extract(127, 64, seed_xmm0)`: **PROVED_ON_SHIP**.

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
fp.to_ieee_bv(fpToFP(RNE(), seed_rdi))
```

The source, LITERAL (`src3b/cvtsi2sd_gpr_xmm_64__reg_xmm0__rust.rs`):

```
#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of cvtsi2sd_gpr_xmm_64__reg_xmm0__rust.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(RNE(), v0))
#[no_mangle]
pub extern "C" fn emu_cvtsi2sd_gpr_xmm_64__reg_xmm0__rust(a: u64) -> f64
{
    f64::from_bits(((((((((a as u64)) as i64)) as f64)).to_bits() as u64)) as u64)
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
cvtsi2sd %rdi,%xmm0; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
cvtsi2sd %rdi,%xmm0
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |

### 1.39 `cvtsi2sd` gpr_xmm 64 -> go

The row, LITERAL: `cvtsi2sd %rdi,%xmm0` (`r02658`), chosen: of the 4 TRANSLATED rows at this cell, the one whose own sweep width equals the cell's key_width.

The corpus's attestation of this cell: 860 unit(s), 860 ledger row(s).

#### place `reg_xmm0`, 128 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(127, 64, v0), fp.to_ieee_bv(fpToFP(RNE(), v1)))
```

**Fix 2, the lane.** This place is a vector register, 128 bits, and the cell's own `key_width` is 64, so the driver rendered `Extract(63, 0, the cell's own term for this place)`. The projected lane, LITERAL:

```
fp.to_ieee_bv(fpToFP(RNE(), v0))
```

The bits above the lane, LITERAL: `Extract(127, 64, v0)` -- put to the gate against `Extract(127, 64, seed_xmm0)`: **PROVED_ON_SHIP**.

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
fp.to_ieee_bv(fpToFP(RNE(), seed_rdi))
```

The source, LITERAL (`src3b/cvtsi2sd_gpr_xmm_64__reg_xmm0__go.go`):

```
// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of cvtsi2sd_gpr_xmm_64__reg_xmm0__go.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(RNE(), v0))
package main

import "math"

//go:noinline
func emu_cvtsi2sd_gpr_xmm_64__reg_xmm0__go(a uint64) float64 {
	return math.Float64frombits(uint64(uint64(math.Float64bits(float64((int64(uint64(a))))))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_cvtsi2sd_gpr_xmm_64__reg_xmm0__go(g0)
	_ = sink
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
push %rbp; mov %rsp,%rbp; sub $0x8,%rsp; xorps %xmm1,%xmm1; cvtsi2sd %rax,%xmm1; movsd %xmm1,(%rsp); movsd (%rsp),%xmm0; add $0x8,%rsp; pop %rbp; nop; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
sub $0x8,%rsp; xorps %xmm1,%xmm1; cvtsi2sd %rax,%xmm1; add $0x8,%rsp
```

Against the cell's own arch opcode: **NOT_COLLAPSED** (4 arch opcodes remain).

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rax |

### 1.40 `cvtsi2sd` gpr_xmm 64 -> swift

The row, LITERAL: `cvtsi2sd %rdi,%xmm0` (`r02658`), chosen: of the 4 TRANSLATED rows at this cell, the one whose own sweep width equals the cell's key_width.

The corpus's attestation of this cell: 860 unit(s), 860 ledger row(s).

#### place `reg_xmm0`, 128 bits

**Step 1, the input.** The cell's term for this place, LITERAL, as the model table prints it:

```
Concat(Extract(127, 64, v0), fp.to_ieee_bv(fpToFP(RNE(), v1)))
```

**Fix 2, the lane.** This place is a vector register, 128 bits, and the cell's own `key_width` is 64, so the driver rendered `Extract(63, 0, the cell's own term for this place)`. The projected lane, LITERAL:

```
fp.to_ieee_bv(fpToFP(RNE(), v0))
```

The bits above the lane, LITERAL: `Extract(127, 64, v0)` -- put to the gate against `Extract(127, 64, seed_xmm0)`: **PROVED_ON_SHIP**.

**Step 2, the render.** The term the renderer was handed, LITERAL:

```
fp.to_ieee_bv(fpToFP(RNE(), seed_rdi))
```

The source, LITERAL (`src3b/cvtsi2sd_gpr_xmm_64__reg_xmm0__swift.swift`):

```
// task g1 emulation -- rendered by swift_render.py
// SwiftRenderer from the layer-4 term of cvtsi2sd_gpr_xmm_64__reg_xmm0__swift.
// EVERY SPELLING IN THIS SOURCE IS UNMEASURED: there is no swiftc in
// the image, so nothing here has been compiled or carved.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(RNE(), v0))
@_cdecl("emu_cvtsi2sd_gpr_xmm_64__reg_xmm0__swift")
public func emu_cvtsi2sd_gpr_xmm_64__reg_xmm0__swift(_ a: UInt64) -> Double
{
    return Double(bitPattern: UInt64(truncatingIfNeeded: (UInt64((Double((Int64(bitPattern: (UInt64(a)))))).bitPattern))))
}
```

**Step 3, the compile and carve.** The object's body, LITERAL:

```
cvtsi2sd %rdi,%xmm0; ret
```

Chaff-stripped by task o2's own narrow rule, LITERAL:

```
cvtsi2sd %rdi,%xmm0
```

Against the cell's own arch opcode: **LANDED**.

**Step 4, the check.** body: the reference's answer for the carved body; cell: the cell's own term, as the model table holds it. Verdict: **PROVED_ON_SHIP** -- z3 proved the carved body's answer equal to the cell's term for every value of every aligned input row

| row | the cell reads | the body reads |
|---|---|---|
| IN-0 | rdi | rdi |


## 2. The forty runs, one row each

Table 1 -- one row per (cell, target). `route` is `primitive` where the target has an operator whose whole lowered body IS this cell (task o2's own single-opcode rows, classified by task m1b's own classifier) and `term` where it has not. `rendered` is a GLOSS: the destination place's rendered expression on one line with the casts stripped for reading; the LITERAL source sits in that run's own section above. `gate` carries the verdict and, beside it, WHERE it holds -- every input, or a region with z3's own counterexample. `composition` is a GLOSS, task h1b's own: the RAW carved body of the destination place, each table-cell instruction by its mnemonic, `ret` and calling-convention moves counted as chaff, an instruction that maps to no table cell starred.

| cell | lang | route | rendered (GLOSS) | landed | composition (GLOSS) | gate (verdict, and where it holds) | cause if refused |
|---|---|---|---|---|---|---|---|
| `add` gpr_gpr 32 | c | term | `((((UINT32_C(0x0)) << 32) \| (((a) + (b)))))` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `add` gpr_gpr 32 | rust | term | `(((((((0x0u32)) << 32) \| ((((((((a)))).wrapping_add((((b))))))))))))` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `add` gpr_gpr 32 | go | primitive | `a + b` | LANDED | `add` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `add` gpr_gpr 32 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) \| (UInt64(truncatingIfNeeded: (UInt32(truncatingIf...` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sub` imm_gpr 64 | c | term | `(((a) + (UINT64_C(0xfffffffffffffffd))))` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sub` imm_gpr 64 | rust | term | `((((((((a)))).wrapping_add(((0xfffffffffffffffdu64)))))))` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sub` imm_gpr 64 | go | term | `uint64((uint64((uint64(uint64(a))) + (uint64(uint64(0xfffffffffffffffd))))))` | LANDED_ELSEWHERE on `add` | `add` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sub` imm_gpr 64 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(a)))) &+ (UInt64(truncatingIfNeeded: UInt64(0xfffffffffffffffd))))))` | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `imul` gpr_gpr 32 | c | primitive | `a * b` | LANDED | `imul` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `imul` gpr_gpr 32 | rust | primitive | `a * b` | LANDED | `imul` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `imul` gpr_gpr 32 | go | primitive | `a * b` | LANDED | `imul` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `imul` gpr_gpr 32 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) \| (UInt64(truncatingIfNeeded: (UInt32(truncatingIf...` | LANDED | `imul` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sar` cl_gpr 32 | c | primitive | `a >> b` | LANDED | `sar` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sar` cl_gpr 32 | rust | primitive | `a >> b` | LANDED | `sar` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sar` cl_gpr 32 | go | term | `uint64((uint64(((uint64(uint32(0x0))) << 32) \| (uint64((uint32(uint32((int32(uint32(a))) >> ((uint32((uint32(((uint32(uint32(0x0))) << 5) \| (uint32(((uint3...` | NOT_COLLAPSED (2) | `movzbl` `sar` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `sar` cl_gpr 32 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) \| (UInt64(truncatingIfNeeded: (UInt32(truncatingIf...` | LANDED | `sar` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `shr` cl_gpr 64 | c | primitive | `a >> b` | LANDED | `shr` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `shr` cl_gpr 64 | rust | primitive | `a >> b` | LANDED | `shr` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `shr` cl_gpr 64 | go | term | `uint64((uint64((uint64(uint64(a))) >> ((uint64((uint64(((uint64(uint64(0x0))) << 6) \| (uint64(((uint32((uint32(b)) >> 0)) & uint32(0x3f)))))))) & uint64(0x3...` | NOT_COLLAPSED (2) | `movzbl` `shr` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `shr` cl_gpr 64 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: (UInt64(a)))) &>> (UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ...` | LANDED | `shr` (+3 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `idiv` gpr_one 32 | c | term | `((((UINT32_C(0x0)) << 32) \| (((((((((a) << 32) \| (b)))) / (((((((c >> 31) & UINT32_C(0x1))) << 63) \| ((((c >> 31) & UINT32_C(0x1))) << 62) \| ((((c >> 31)...` | NOT_COLLAPSED (51) | `shl` `or` `shr` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `or` `shl` `shl` `or` `s... (+25 chaff) | UNDECIDED, UNDECIDED at 300000 ms -- not decided: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |  |
| `idiv` gpr_one 32 | rust | term | `(((((((0x0u32)) << 32) \| ((((((((({ let n1: i64 = ((((((((((a))) << 32) \| (((b))))))))); let d1: i64 = ((((((((((((((c)) >> 31)) & 0x1u32))) << 63) \| ((((...` | NOT_COLLAPSED (51) | `shl` `or` `shr` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `or` `shl` `shl` `or` `s... (+25 chaff) | UNDECIDED, UNDECIDED at 300000 ms -- not decided: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |  |
| `idiv` gpr_one 32 | go | term | `uint64((uint64(((uint64(uint32(0x0))) << 32) \| (uint64((uint32((uint64((uint64(uint64((int64((uint64(((uint64(uint32(a))) << 32) \| (uint64(uint32(b))))))) ...` | NOT_COLLAPSED (85) | `lea` `cmp` `sub` `shl` `shr` `and` `shl` `shl` `shl` `shl` `shl` `shl` `shl` `shl` `shl` `shl` `shl` `shl` ... -- maps to no cell: `jbe`\* `je`\* `jne`\* `jmp`\* `call`\* `call`\* `jmp`\* (+92 chaff) | UNDECIDED, UNDECIDED at 300000 ms -- not decided: the solver did not answer inside its 3000 ms limit, so the verdict is undecided and never disproved |  |
| `idiv` gpr_one 32 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) \| (UInt64(truncatingIfNeeded: (UInt32(truncatingIf...` | LANDED_ELSEWHERE on `jmp` |  -- maps to no cell: `jmp`\* | UNDECIDED, UNDECIDED at 300000 ms -- not decided: the carved body: the reference: this unit record carries no body, so there is no ship code to walk; and no term either |  |
| `cmovne` gpr_gpr 32 | c | term | `((((UINT32_C(0x0)) << 32) \| ((((((~((((~(b))) \| ((~(a))))))) == (UINT32_C(0x0)))) ? (d) : (c)))))` | NOT_COLLAPSED (2) | `test` `cmove` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cmovne` gpr_gpr 32 | rust | term | `(((((((0x0u32)) << 32) \| (((if ((((((!((((((((!(((b))))))) \| ((((!(((a))))))))))))))) == ((0x0u32)))) { (((d))) } else { (((c))) })))))))` | NOT_COLLAPSED (2) | `test` `cmove` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cmovne` gpr_gpr 32 | go | term | `uint64((uint64(((uint64(uint32(0x0))) << 32) \| (uint64(sel32(((uint32((uint32(^(uint32((uint32((uint32((uint32(^(uint32(uint32(b))))))) \| (uint32((uint32(^...` | NOT_COLLAPSED (2) | `test` `cmove` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cmovne` gpr_gpr 32 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt32(0x0))) &<< 32) \| (UInt64(truncatingIfNeeded: ((((UInt32(truncatin...` | NOT_COLLAPSED (2) | `test` `cmove` (+2 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `setne` gpr_one 8 | c | term | `((((UINT64_C(0x0)) << 8) \| (((((((~((((((~(a)) & UINT32_C(0xff))) \| (((~(b)) & UINT32_C(0xff)))) & UINT32_C(0xff)))) & UINT32_C(0xff))) == (UINT32_C(0x0)))...` | NOT_COLLAPSED (3) | `xor` `test` `setne` (+1 chaff) | DISPROVED, PROVED_ON_SHIP under caller extension -- holds on every input once each narrow-holder row is zero-extended to the register |  |
| `setne` gpr_one 8 | rust | term | `(((((((0x0u64)) << 8) \| (((if (((((((!((((((((((!(((a))))) & 0xffu32))) \| (((((!(((b))))) & 0xffu32))))) & 0xffu32))))) & 0xffu32))) == ((0x0u32)))) { ((0x...` | NOT_COLLAPSED (3) | `xor` `test` `setne` (+1 chaff) | DISPROVED, PROVED_ON_SHIP under caller extension -- holds on every input once each narrow-holder row is zero-extended to the register |  |
| `setne` gpr_one 8 | go | term | `uint64((uint64(((uint64(uint64(0x0))) << 8) \| (uint64(sel32(((uint32(((uint32(^(uint32(((uint32((uint32(((uint32(^(uint32(uint32(a))))) & uint32(0xff)))) \|...` | NOT_COLLAPSED (13) | `movzbl` `not` `movzbl` `movzbl` `not` `movzbl` `or` `movzbl` `not` `movzbl` `test` `setne` `movzbl` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `setne` gpr_one 8 | swift | term | `UInt64(truncatingIfNeeded: (UInt64(truncatingIfNeeded: ((UInt64(truncatingIfNeeded: UInt64(0x0))) &<< 8) \| (UInt64(truncatingIfNeeded: ((((UInt32(truncating...` | NOT_COLLAPSED (3) | `xor` `test` `setne` (+1 chaff) | DISPROVED, PROVED_ON_SHIP under caller extension -- holds on every input once each narrow-holder row is zero-extended to the register |  |
| `addss` xmm_xmm 32 | c | term | `bits_to_f32((f32_to_bits(((float)((b) + (a))))))` | LANDED |  -- maps to no cell: `addss`\* (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `addss` xmm_xmm 32 | rust | term | `f32::from_bits((((((b) + (a))).to_bits())))` | LANDED |  -- maps to no cell: `addss`\* (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `addss` xmm_xmm 32 | go | term | `math.Float32frombits(uint32(uint32(math.Float32bits(((b) + (a))))))` | NOT_COLLAPSED (3) | `sub` `add` -- maps to no cell: `addss`\* (+6 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `addss` xmm_xmm 32 | swift | term | `Float(bitPattern: UInt32(truncatingIfNeeded: (UInt32((((b) + (a))).bitPattern))))` | LANDED |  -- maps to no cell: `addss`\* (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cvtsi2sd` gpr_xmm 64 | c | term | `bits_to_f64((f64_to_bits(((double)(a)))))` | LANDED | `cvtsi2sd` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cvtsi2sd` gpr_xmm 64 | rust | term | `f64::from_bits(((((((((a)))))).to_bits())))` | LANDED | `cvtsi2sd` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cvtsi2sd` gpr_xmm 64 | go | term | `math.Float64frombits(uint64(uint64(math.Float64bits(float64((int64(uint64(a))))))))` | NOT_COLLAPSED (4) | `sub` `cvtsi2sd` `add` -- maps to no cell: `xorps`\* (+7 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |
| `cvtsi2sd` gpr_xmm 64 | swift | term | `Double(bitPattern: UInt64(truncatingIfNeeded: (UInt64((Double((Int64(bitPattern: (UInt64(a)))))).bitPattern))))` | LANDED | `cvtsi2sd` (+1 chaff) | PROVED_ON_SHIP -- holds on every input of every aligned row |  |

## 3. What did not work, by cause

### 3.1 Refusals and gate calls that did not prove

- `a width c has no holder for`: 2 -- sub imm_gpr 64/go [flags], sub imm_gpr 64/swift [flags]
- `the flags place of a preseeded row is the flag state that ARRIVED, not a place this opcode writes`: 8 -- cmovne gpr_gpr 32/c [flags], cmovne gpr_gpr 32/rust [flags], cmovne gpr_gpr 32/go [flags], cmovne gpr_gpr 32/swift [flags], setne gpr_one 8/c [flags], setne gpr_one 8/rust [flags], setne gpr_one 8/go [flags], setne gpr_one 8/swift [flags]
- `the gate answered UNDECIDED at 3,000 ms and again at 300000 ms`: 8 -- idiv gpr_one 32/c [reg_rax], idiv gpr_one 32/c [reg_rdx], idiv gpr_one 32/rust [reg_rax], idiv gpr_one 32/rust [reg_rdx], idiv gpr_one 32/go [reg_rax], idiv gpr_one 32/go [reg_rdx], idiv gpr_one 32/swift [reg_rax], idiv gpr_one 32/swift [reg_rdx]
- `the primitive route renders the operator's own answer, and the flags place is not a value an operator answers with`: 4 -- add gpr_gpr 32/go [flags], imul gpr_gpr 32/c [flags], imul gpr_gpr 32/rust [flags], imul gpr_gpr 32/go [flags]

### 3.2 The landings that were not LANDED, by cause

- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (2 remain): 2 -- sar cl_gpr 32/go [reg_rdi], shr cl_gpr 64/go [reg_rdi]
- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (3 remain): 1 -- addss xmm_xmm 32/go [reg_xmm0]
- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (4 remain): 1 -- cvtsi2sd gpr_xmm 64/go [reg_xmm0]
- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (51 remain): 4 -- idiv gpr_one 32/c [reg_rax], idiv gpr_one 32/c [reg_rdx], idiv gpr_one 32/rust [reg_rax], idiv gpr_one 32/rust [reg_rdx]
- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (85 remain): 2 -- idiv gpr_one 32/go [reg_rax], idiv gpr_one 32/go [reg_rdx]
- the compiler chose another arch opcode for the same computation (`add`): 1 -- sub imm_gpr 64/go [reg_rdi]
- the compiler chose another arch opcode for the same computation (`jmp`): 2 -- idiv gpr_one 32/swift [reg_rax], idiv gpr_one 32/swift [reg_rdx]
- the compiler chose another arch opcode for the same computation (`lea`): 6 -- add gpr_gpr 32/c [reg_rdi], add gpr_gpr 32/rust [reg_rdi], add gpr_gpr 32/swift [reg_rdi], sub imm_gpr 64/c [reg_rdi], sub imm_gpr 64/rust [reg_rdi], sub imm_gpr 64/swift [reg_rdi]
- the compiler chose another arch opcode for the same computation (`mov`): 2 -- sub imm_gpr 64/c [flags], sub imm_gpr 64/rust [flags]
- the emulation is a PAIR by construction (the setter's comparison, then the select), so more than one arch opcode was never possible (13 remain): 1 -- setne gpr_one 8/go [reg_rdi]
- the emulation is a PAIR by construction (the setter's comparison, then the select), so more than one arch opcode was never possible (2 remain): 4 -- cmovne gpr_gpr 32/c [reg_rdi], cmovne gpr_gpr 32/rust [reg_rdi], cmovne gpr_gpr 32/go [reg_rdi], cmovne gpr_gpr 32/swift [reg_rdi]
- the emulation is a PAIR by construction (the setter's comparison, then the select), so more than one arch opcode was never possible (3 remain): 3 -- setne gpr_one 8/c [reg_rdi], setne gpr_one 8/rust [reg_rdi], setne gpr_one 8/swift [reg_rdi]
- the flags place is the reference's flag model -- the two values the setter compared, repacked -- so it is not one operation and no single arch opcode is its landing (2 remain): 4 -- add gpr_gpr 32/c [flags], add gpr_gpr 32/rust [flags], add gpr_gpr 32/swift [flags], imul gpr_gpr 32/swift [flags]

## 4. Task g1's verdict beside this run's

Table 4 -- one row per (cell, target) THIS run holds, with task g1's own answer for the same pair from `handful3.json` beside it. A row whose two sides differ is a row the change moved; a row whose two sides agree is the check that nothing else did.

| cell | lang | g1 route | g1 verdict | this route | this verdict | moved |
|---|---|---|---|---|---|---|
| `add` gpr_gpr 32 | c | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `add` gpr_gpr 32 | rust | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `add` gpr_gpr 32 | go | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `add` gpr_gpr 32 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |
| `sub` imm_gpr 64 | c | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `sub` imm_gpr 64 | rust | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `sub` imm_gpr 64 | go | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `sub` imm_gpr 64 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |
| `imul` gpr_gpr 32 | c | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `imul` gpr_gpr 32 | rust | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `imul` gpr_gpr 32 | go | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `imul` gpr_gpr 32 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |
| `sar` cl_gpr 32 | c | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `sar` cl_gpr 32 | rust | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `sar` cl_gpr 32 | go | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `sar` cl_gpr 32 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |
| `shr` cl_gpr 64 | c | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `shr` cl_gpr 64 | rust | primitive | PROVED_ON_SHIP | primitive | PROVED_ON_SHIP | no |
| `shr` cl_gpr 64 | go | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `shr` cl_gpr 64 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |
| `idiv` gpr_one 32 | c | term | UNDECIDED, UNDECIDED at 300000 ms | term | UNDECIDED, UNDECIDED at 300000 ms | no |
| `idiv` gpr_one 32 | rust | term | UNDECIDED, UNDECIDED at 300000 ms | term | UNDECIDED, UNDECIDED at 300000 ms | no |
| `idiv` gpr_one 32 | go | term | UNDECIDED, UNDECIDED at 300000 ms | term | UNDECIDED, UNDECIDED at 300000 ms | no |
| `idiv` gpr_one 32 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | UNDECIDED, UNDECIDED at 300000 ms | **yes** |
| `cmovne` gpr_gpr 32 | c | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `cmovne` gpr_gpr 32 | rust | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `cmovne` gpr_gpr 32 | go | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `cmovne` gpr_gpr 32 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |
| `setne` gpr_one 8 | c | term | DISPROVED, PROVED_ON_SHIP under caller extension | term | DISPROVED, PROVED_ON_SHIP under caller extension | no |
| `setne` gpr_one 8 | rust | term | DISPROVED, PROVED_ON_SHIP under caller extension | term | DISPROVED, PROVED_ON_SHIP under caller extension | no |
| `setne` gpr_one 8 | go | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `setne` gpr_one 8 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | DISPROVED, PROVED_ON_SHIP under caller extension | **yes** |
| `addss` xmm_xmm 32 | c | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `addss` xmm_xmm 32 | rust | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `addss` xmm_xmm 32 | go | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `addss` xmm_xmm 32 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |
| `cvtsi2sd` gpr_xmm 64 | c | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `cvtsi2sd` gpr_xmm 64 | rust | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `cvtsi2sd` gpr_xmm 64 | go | term | PROVED_ON_SHIP | term | PROVED_ON_SHIP | no |
| `cvtsi2sd` gpr_xmm 64 | swift | term | the compiler refused: /persist/swift/usr/bin/swiftc: No such file or directory | term | PROVED_ON_SHIP | **yes** |

## 5. Which route ran, and why

Table 3 -- the primitive lookup, per (cell, target): how many of that language's single-opcode rows classify to the cell, which row was chosen and on what ground, and -- where none did -- the cause the term route ran instead.

| cell | lang | route | single-opcode rows at this cell | chosen row's body, LITERAL | the setup cells the row carries | the operator and operand types the manifest records | cause if no primitive |
|---|---|---|---|---|---|---|---|
| `add` gpr_gpr 32 | c | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `add` gpr_gpr 32 | rust | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `add` gpr_gpr 32 | go | primitive | 1 | `add %ebx,%eax; ret` |  | `a + b on int32 and int32` (probe go/op_312 of go) |  |
| `add` gpr_gpr 32 | swift | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `sub` imm_gpr 64 | c | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `sub` imm_gpr 64 | rust | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `sub` imm_gpr 64 | go | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `sub` imm_gpr 64 | swift | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `imul` gpr_gpr 32 | c | primitive | 1 | `mov %edi,%eax; imul %esi,%eax; ret` |  | `a * b on int32_t and int32_t` (probe c/op_174 of c) |  |
| `imul` gpr_gpr 32 | rust | primitive | 1 | `mov %edi,%eax; imul %esi,%eax; ret` |  | `a * b on i32 and i32` (probe rust/op_606 of rust) |  |
| `imul` gpr_gpr 32 | go | primitive | 1 | `imul %ebx,%eax; ret` |  | `a * b on int32 and int32` (probe go/op_60 of go) |  |
| `imul` gpr_gpr 32 | swift | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `sar` cl_gpr 32 | c | primitive | 2 | `mov %esi,%ecx; mov %edi,%eax; sar %cl,%eax; ret` |  | `a >> b on int32_t and int32_t` (probe c/op_714 of c) |  |
| `sar` cl_gpr 32 | rust | primitive | 2 | `mov %rsi,%rcx; mov %edi,%eax; sar %cl,%eax; ret` |  | `a >> b on i32 and i64` (probe rust/op_499 of rust) |  |
| `sar` cl_gpr 32 | go | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `sar` cl_gpr 32 | swift | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `shr` cl_gpr 64 | c | primitive | 2 | `mov %esi,%ecx; mov %rdi,%rax; shr %cl,%rax; ret` |  | `a >> b on uint64_t and int32_t` (probe c/op_726 of c) |  |
| `shr` cl_gpr 64 | rust | primitive | 2 | `mov %rsi,%rcx; mov %rdi,%rax; shr %cl,%rax; ret` |  | `a >> b on u64 and i64` (probe rust/op_511 of rust) |  |
| `shr` cl_gpr 64 | go | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `shr` cl_gpr 64 | swift | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `idiv` gpr_one 32 | c | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell -- though under task o2's WIDE chaff rule there is one, `mov %edi,%eax; cltd; idiv %esi; mov %edx,%eax; ret` (c/op_246), which is evidence about the cell and not a second route |
| `idiv` gpr_one 32 | rust | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `idiv` gpr_one 32 | go | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `idiv` gpr_one 32 | swift | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cmovne` gpr_gpr 32 | c | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cmovne` gpr_gpr 32 | rust | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cmovne` gpr_gpr 32 | go | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cmovne` gpr_gpr 32 | swift | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `setne` gpr_one 8 | c | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `setne` gpr_one 8 | rust | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `setne` gpr_one 8 | go | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `setne` gpr_one 8 | swift | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `addss` xmm_xmm 32 | c | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `addss` xmm_xmm 32 | rust | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `addss` xmm_xmm 32 | go | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `addss` xmm_xmm 32 | swift | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cvtsi2sd` gpr_xmm 64 | c | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cvtsi2sd` gpr_xmm 64 | rust | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cvtsi2sd` gpr_xmm 64 | go | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |
| `cvtsi2sd` gpr_xmm 64 | swift | term | 0 |  |  |  | no single-opcode row of this language's own corpus classifies to this cell |

