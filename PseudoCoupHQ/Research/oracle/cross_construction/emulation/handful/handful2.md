# handful2.md -- task h2: the same twenty `find_emulation` runs after two printing fixes

The same ten cells of the arch-opcode model table and the same two targets (c and rust) task h1 ran, re-run with the cell's term put through the pipeline's own normaliser before the renderer sees it (fix 1) and a vector cell's lane projected in the driver (fix 2). Neither renderer was changed. Written by `handful.py report2`; never hand-edited. Task h1's own `handful.json` and `handful.md` are untouched.

**What a run is, one sentence.** `find_emulation(cell, lang)` takes the z3 term the reference simulator's own builder writes into each place one table cell's opcode writes, has the existing renderer write that term in the target language's own operators, compiles it at the corpus's own ship flags, carves the body back out, and asks z3 whether the body answers as the cell's term says for every input.

| what | value |
|---|---|
| runs | 20 |
| c ship flags | lane_gen.py compile_probe: `[CLANG, "-std=c17"] + ["-O1"] + ["-c", src, "-o", obj]` -- the ship build of every c unit in the corpus |
| rust ship flags | lane_gen.py compile_probe, rust branch: `opt = ["-C", "opt-level=1", "-C", "debug-assertions=off"]` then `["rustc", "--crate-type=lib", "--emit=obj"] + opt + ["-o", obj, src]` -- the ship build of every rust unit in the corpus |
| solver ceiling | 3000 ms |
| memory bound | 4194304 kB, named abort ABORT_MEMORY_H2 |
| peak resident | 448016 kB |

## 1. The twenty runs, one section each

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

The source, LITERAL (`src2/add_gpr_gpr_32__reg_rdi__c.c`):

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

The source, LITERAL (`src2/add_gpr_gpr_32__flags__c.c`):

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

The source, LITERAL (`src2/add_gpr_gpr_32__reg_rdi__rust.rs`):

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

The source, LITERAL (`src2/add_gpr_gpr_32__flags__rust.rs`):

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

### 1.3 `sub` imm_gpr 64 -> c

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

The source, LITERAL (`src2/sub_imm_gpr_64__reg_rdi__c.c`):

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

The source, LITERAL (`src2/sub_imm_gpr_64__flags__c.c`):

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

### 1.4 `sub` imm_gpr 64 -> rust

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

The source, LITERAL (`src2/sub_imm_gpr_64__reg_rdi__rust.rs`):

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

The source, LITERAL (`src2/sub_imm_gpr_64__flags__rust.rs`):

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

### 1.5 `imul` gpr_gpr 32 -> c

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

The source, LITERAL (`src2/imul_gpr_gpr_32__reg_rdi__c.c`):

```
/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of imul_gpr_gpr_32__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 0, v0)*Extract(31, 0, v1)) */
#include <stdint.h>

uint64_t
emu_imul_gpr_gpr_32__reg_rdi__c(uint32_t a, uint32_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)((uint32_t)((uint32_t)a) * (uint32_t)((uint32_t)b)))));
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

The source, LITERAL (`src2/imul_gpr_gpr_32__flags__c.c`):

```
/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of imul_gpr_gpr_32__flags__c.  The term's layer-5 text, LITERAL:
   Concat(Extract(31, 0, v0), Extract(31, 0, v1)) */
#include <stdint.h>

uint64_t
emu_imul_gpr_gpr_32__flags__c(uint32_t a, uint32_t b)
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

### 1.6 `imul` gpr_gpr 32 -> rust

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

The source, LITERAL (`src2/imul_gpr_gpr_32__reg_rdi__rust.rs`):

```
#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of imul_gpr_gpr_32__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0)*Extract(31, 0, v1))
#[no_mangle]
pub extern "C" fn emu_imul_gpr_gpr_32__reg_rdi__rust(a: u32, b: u32) -> u64
{
    (((((((0x0u32) as u64) << 32) | ((((((((a as u32)) as u32)).wrapping_mul((((b as u32)) as u32))) as u32)) as u64)) as u64)) as u64)
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

The source, LITERAL (`src2/imul_gpr_gpr_32__flags__rust.rs`):

```
#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of imul_gpr_gpr_32__flags__rust.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(31, 0, v0), Extract(31, 0, v1))
#[no_mangle]
pub extern "C" fn emu_imul_gpr_gpr_32__flags__rust(a: u32, b: u32) -> u64
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

### 1.7 `sar` cl_gpr 32 -> c

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

The source, LITERAL (`src2/sar_cl_gpr_32__reg_rdi__c.c`):

```
/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of sar_cl_gpr_32__reg_rdi__c.  The term's layer-5 text, LITERAL:
   Concat(0, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1))) */
#include <stdint.h>

uint64_t
emu_sar_cl_gpr_32__reg_rdi__c(uint32_t a, uint8_t b)
{
    return (uint64_t)((uint64_t)(((uint64_t)(UINT32_C(0x0)) << 32) | (uint64_t)((uint32_t)((int32_t)((uint32_t)a) >> (unsigned)(uint32_t)((uint32_t)(((uint32_t)(UINT32_C(0x0)) << 5) | (uint32_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x1f)))))))));
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

### 1.8 `sar` cl_gpr 32 -> rust

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

The source, LITERAL (`src2/sar_cl_gpr_32__reg_rdi__rust.rs`):

```
#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of sar_cl_gpr_32__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0) >> Concat(0, Extract(4, 0, v1)))
#[no_mangle]
pub extern "C" fn emu_sar_cl_gpr_32__reg_rdi__rust(a: u32, b: u8) -> u64
{
    (((((((0x0u32) as u64) << 32) | ((((((((a as u32)) as i32)).wrapping_shr(((((((((0x0u32) as u32) << 5) | (((((((b as u32)) >> 0) as u32) & 0x1fu32)) as u32)) as u32)) as u32) as u32))) as u32)) as u64)) as u64)) as u64)
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

### 1.9 `shr` cl_gpr 64 -> c

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

The source, LITERAL (`src2/shr_cl_gpr_64__reg_rdi__c.c`):

```
/* task o7 emulation -- rendered by emulate.py Renderer from the layer-4 term of shr_cl_gpr_64__reg_rdi__c.  The term's layer-5 text, LITERAL:
   LShR(v0, Concat(0, Extract(5, 0, v1))) */
#include <stdint.h>

uint64_t
emu_shr_cl_gpr_64__reg_rdi__c(uint64_t a, uint8_t b)
{
    return (uint64_t)((uint64_t)((uint64_t)((uint64_t)a) >> (unsigned)(uint64_t)((uint64_t)(((uint64_t)(UINT64_C(0x0)) << 6) | (uint64_t)(((uint32_t)((uint32_t)b >> 0) & UINT32_C(0x3f)))))));
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

### 1.10 `shr` cl_gpr 64 -> rust

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

The source, LITERAL (`src2/shr_cl_gpr_64__reg_rdi__rust.rs`):

```
#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of shr_cl_gpr_64__reg_rdi__rust.
// The term's layer-5 text, LITERAL:
//   LShR(v0, Concat(0, Extract(5, 0, v1)))
#[no_mangle]
pub extern "C" fn emu_shr_cl_gpr_64__reg_rdi__rust(a: u64, b: u8) -> u64
{
    (((((((a as u64)) as u64).wrapping_shr(((((((((0x0u64) as u64) << 6) | (((((((b as u32)) >> 0) as u32) & 0x3fu32)) as u64)) as u64)) as u64) as u32))) as u64)) as u64)
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

### 1.11 `idiv` gpr_one 32 -> c

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

The source, LITERAL (`src2/idiv_gpr_one_32__reg_rax__c.c`):

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

The source, LITERAL (`src2/idiv_gpr_one_32__reg_rdx__c.c`):

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

### 1.12 `idiv` gpr_one 32 -> rust

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

The source, LITERAL (`src2/idiv_gpr_one_32__reg_rax__rust.rs`):

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

The source, LITERAL (`src2/idiv_gpr_one_32__reg_rdx__rust.rs`):

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

### 1.13 `cmovne` gpr_gpr 32 -> c

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

The source, LITERAL (`src2/cmovne_gpr_gpr_32__reg_rdi__c.c`):

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

### 1.14 `cmovne` gpr_gpr 32 -> rust

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

The source, LITERAL (`src2/cmovne_gpr_gpr_32__reg_rdi__rust.rs`):

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

### 1.15 `setne` gpr_one 8 -> c

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

The source, LITERAL (`src2/setne_gpr_one_8__reg_rdi__c.c`):

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

### 1.16 `setne` gpr_one 8 -> rust

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

The source, LITERAL (`src2/setne_gpr_one_8__reg_rdi__rust.rs`):

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

### 1.17 `addss` xmm_xmm 32 -> c

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

The source, LITERAL (`src2/addss_xmm_xmm_32__reg_xmm0__c.c`):

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
    return bits_to_f32((uint32_t)((uint32_t)f32_to_bits(((float)((a) + (b))))));
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
| IN-0 | xmm0 | xmm0 |
| IN-1 | xmm1 | xmm1 |

### 1.18 `addss` xmm_xmm 32 -> rust

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

The source, LITERAL (`src2/addss_xmm_xmm_32__reg_xmm0__rust.rs`):

```
#![allow(dead_code, unused_parens, unused_unsafe, unconditional_panic, non_snake_case, overflowing_literals)]

// task o11 emulation -- rendered by rust_render.py
// RustRenderer from the layer-4 term of addss_xmm_xmm_32__reg_xmm0__rust.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1)))
#[no_mangle]
pub extern "C" fn emu_addss_xmm_xmm_32__reg_xmm0__rust(a: f32, b: f32) -> f32
{
    f32::from_bits((((((a) + (b))).to_bits() as u32)) as u32)
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
| IN-0 | xmm0 | xmm0 |
| IN-1 | xmm1 | xmm1 |

### 1.19 `cvtsi2sd` gpr_xmm 64 -> c

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

The source, LITERAL (`src2/cvtsi2sd_gpr_xmm_64__reg_xmm0__c.c`):

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

### 1.20 `cvtsi2sd` gpr_xmm 64 -> rust

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

The source, LITERAL (`src2/cvtsi2sd_gpr_xmm_64__reg_xmm0__rust.rs`):

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


## 2. The twenty runs, one row each: task h1's verdict beside task h2's

Table 1 -- one row per run, the same ten cells and the same two targets as task h1. `h1 verdict` is the gate verdict of that run's destination place as task h1 recorded it (`handful.json`), and `h2 verdict` is the same place's verdict after the two printing fixes; where a run was refused before any gate call the column carries the refusal's own cause word. `composition (h2)` is a GLOSS, task h1b's own column over this task's own carved bodies: each table-cell instruction by its mnemonic, `ret` and calling-convention moves counted as chaff rather than listed, an instruction that maps to no table cell starred. The LITERAL objects of every run -- the cell's term, the rendered source, the carved body and the gate's own words -- are in that run's own section above.

| cell | lang | h1 verdict | h2 verdict | landed (h2) | composition (h2) | cause if refused |
|---|---|---|---|---|---|---|
| `add` gpr_gpr 32 | c | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) |  |
| `add` gpr_gpr 32 | rust | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) |  |
| `sub` imm_gpr 64 | c | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) |  |
| `sub` imm_gpr 64 | rust | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED_ELSEWHERE on `lea` | `lea` (+1 chaff) |  |
| `imul` gpr_gpr 32 | c | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED | `imul` (+2 chaff) |  |
| `imul` gpr_gpr 32 | rust | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED | `imul` (+2 chaff) |  |
| `sar` cl_gpr 32 | c | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED | `sar` (+3 chaff) |  |
| `sar` cl_gpr 32 | rust | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED | `sar` (+3 chaff) |  |
| `shr` cl_gpr 64 | c | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED | `shr` (+3 chaff) |  |
| `shr` cl_gpr 64 | rust | PROVED_ON_SHIP | PROVED_ON_SHIP | LANDED | `shr` (+3 chaff) |  |
| `idiv` gpr_one 32 | c | UNDECIDED, UNDECIDED at 300000 ms | UNDECIDED, UNDECIDED at 300000 ms | NOT_COLLAPSED (51) | `shl` `or` `shr` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `or` `shl` `shl` `or` `s... (+25 chaff) |  |
| `idiv` gpr_one 32 | rust | UNDECIDED, UNDECIDED at 300000 ms | UNDECIDED, UNDECIDED at 300000 ms | NOT_COLLAPSED (51) | `shl` `or` `shr` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `shl` `or` `or` `shl` `shl` `or` `s... (+25 chaff) |  |
| `cmovne` gpr_gpr 32 | c | PROVED_ON_SHIP | PROVED_ON_SHIP | NOT_COLLAPSED (2) | `test` `cmove` (+2 chaff) |  |
| `cmovne` gpr_gpr 32 | rust | PROVED_ON_SHIP | PROVED_ON_SHIP | NOT_COLLAPSED (2) | `test` `cmove` (+2 chaff) |  |
| `setne` gpr_one 8 | c | DISPROVED, PROVED_ON_SHIP under caller extension | DISPROVED, PROVED_ON_SHIP under caller extension | NOT_COLLAPSED (3) | `xor` `test` `setne` (+1 chaff) |  |
| `setne` gpr_one 8 | rust | DISPROVED, PROVED_ON_SHIP under caller extension | DISPROVED, PROVED_ON_SHIP under caller extension | NOT_COLLAPSED (3) | `xor` `test` `setne` (+1 chaff) |  |
| `addss` xmm_xmm 32 | c | vector arrival used beyond its low lane: xmm0 read above bit 63 | PROVED_ON_SHIP | LANDED |  -- maps to no cell: `addss`\* (+1 chaff) |  |
| `addss` xmm_xmm 32 | rust | vector arrival used beyond its low lane: xmm0 read above bit 63 | PROVED_ON_SHIP | LANDED |  -- maps to no cell: `addss`\* (+1 chaff) |  |
| `cvtsi2sd` gpr_xmm 64 | c | vector arrival used beyond its low lane: xmm0 read above bit 63 | PROVED_ON_SHIP | LANDED | `cvtsi2sd` (+1 chaff) |  |
| `cvtsi2sd` gpr_xmm 64 | rust | vector arrival used beyond its low lane: xmm0 read above bit 63 | PROVED_ON_SHIP | LANDED | `cvtsi2sd` (+1 chaff) |  |

## 3. What did not work, by cause

### 3.1 Refusals and gate calls that did not prove

- `the flags place of a preseeded row is the flag state that ARRIVED, not a place this opcode writes`: 4 -- cmovne gpr_gpr 32/c [flags], cmovne gpr_gpr 32/rust [flags], setne gpr_one 8/c [flags], setne gpr_one 8/rust [flags]
- `the gate answered UNDECIDED at 3,000 ms and again at 300000 ms`: 4 -- idiv gpr_one 32/c [reg_rax], idiv gpr_one 32/c [reg_rdx], idiv gpr_one 32/rust [reg_rax], idiv gpr_one 32/rust [reg_rdx]

### 3.2 The landings that were not LANDED, by cause

- the cell's own arch opcode IS among the ones that remain; what sits beside it is what the term carries beyond the operation (51 remain): 4 -- idiv gpr_one 32/c [reg_rax], idiv gpr_one 32/c [reg_rdx], idiv gpr_one 32/rust [reg_rax], idiv gpr_one 32/rust [reg_rdx]
- the compiler chose another arch opcode for the same computation (`lea`): 4 -- add gpr_gpr 32/c [reg_rdi], add gpr_gpr 32/rust [reg_rdi], sub imm_gpr 64/c [reg_rdi], sub imm_gpr 64/rust [reg_rdi]
- the compiler chose another arch opcode for the same computation (`mov`): 2 -- sub imm_gpr 64/c [flags], sub imm_gpr 64/rust [flags]
- the emulation is a PAIR by construction (the setter's comparison, then the select), so more than one arch opcode was never possible (2 remain): 2 -- cmovne gpr_gpr 32/c [reg_rdi], cmovne gpr_gpr 32/rust [reg_rdi]
- the emulation is a PAIR by construction (the setter's comparison, then the select), so more than one arch opcode was never possible (3 remain): 2 -- setne gpr_one 8/c [reg_rdi], setne gpr_one 8/rust [reg_rdi]
- the flags place is the reference's flag model -- the two values the setter compared, repacked -- so it is not one operation and no single arch opcode is its landing (2 remain): 4 -- add gpr_gpr 32/c [flags], add gpr_gpr 32/rust [flags], imul gpr_gpr 32/c [flags], imul gpr_gpr 32/rust [flags]

## 4. What the two fixes changed, run by run

### 4.1 Fix 1: the term the renderer is handed

| cell | lang | place | instructions (h1) | instructions (h2) | gate (h1) | gate (h2) |
|---|---|---|---|---|---|---|
| `add` gpr_gpr 32 | c | `reg_rdi` | 2 | 2 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `add` gpr_gpr 32 | c | `flags` | 4 | 4 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `add` gpr_gpr 32 | rust | `reg_rdi` | 2 | 2 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `add` gpr_gpr 32 | rust | `flags` | 4 | 4 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `sub` imm_gpr 64 | c | `reg_rdi` | 2 | 2 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `sub` imm_gpr 64 | c | `flags` | 3 | 3 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `sub` imm_gpr 64 | rust | `reg_rdi` | 2 | 2 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `sub` imm_gpr 64 | rust | `flags` | 3 | 3 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `imul` gpr_gpr 32 | c | `reg_rdi` | 3 | 3 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `imul` gpr_gpr 32 | c | `flags` | 4 | 4 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `imul` gpr_gpr 32 | rust | `reg_rdi` | 3 | 3 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `imul` gpr_gpr 32 | rust | `flags` | 4 | 4 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `sar` cl_gpr 32 | c | `reg_rdi` | 4 | 4 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `sar` cl_gpr 32 | rust | `reg_rdi` | 4 | 4 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `shr` cl_gpr 64 | c | `reg_rdi` | 4 | 4 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `shr` cl_gpr 64 | rust | `reg_rdi` | 4 | 4 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `idiv` gpr_one 32 | c | `reg_rax` | 76 | 76 | UNDECIDED, UNDECIDED at 300000 ms | UNDECIDED, UNDECIDED at 300000 ms |
| `idiv` gpr_one 32 | c | `reg_rdx` | 76 | 76 | UNDECIDED, UNDECIDED at 300000 ms | UNDECIDED, UNDECIDED at 300000 ms |
| `idiv` gpr_one 32 | rust | `reg_rax` | 76 | 76 | UNDECIDED, UNDECIDED at 300000 ms | UNDECIDED, UNDECIDED at 300000 ms |
| `idiv` gpr_one 32 | rust | `reg_rdx` | 76 | 76 | UNDECIDED, UNDECIDED at 300000 ms | UNDECIDED, UNDECIDED at 300000 ms |
| `cmovne` gpr_gpr 32 | c | `reg_rdi` | 4 | 4 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `cmovne` gpr_gpr 32 | c | `flags` | refused | refused |  |  |
| `cmovne` gpr_gpr 32 | rust | `reg_rdi` | 4 | 4 | PROVED_ON_SHIP | PROVED_ON_SHIP |
| `cmovne` gpr_gpr 32 | rust | `flags` | refused | refused |  |  |
| `setne` gpr_one 8 | c | `reg_rdi` | 4 | 4 | DISPROVED, PROVED_ON_SHIP under caller extension | DISPROVED, PROVED_ON_SHIP under caller extension |
| `setne` gpr_one 8 | c | `flags` | refused | refused |  |  |
| `setne` gpr_one 8 | rust | `reg_rdi` | 4 | 4 | DISPROVED, PROVED_ON_SHIP under caller extension | DISPROVED, PROVED_ON_SHIP under caller extension |
| `setne` gpr_one 8 | rust | `flags` | refused | refused |  |  |
| `addss` xmm_xmm 32 | c | `reg_xmm0` | refused | 2 |  | PROVED_ON_SHIP |
| `addss` xmm_xmm 32 | rust | `reg_xmm0` | refused | 2 |  | PROVED_ON_SHIP |
| `cvtsi2sd` gpr_xmm 64 | c | `reg_xmm0` | refused | 2 |  | PROVED_ON_SHIP |
| `cvtsi2sd` gpr_xmm 64 | rust | `reg_xmm0` | refused | 2 |  | PROVED_ON_SHIP |

### 4.2 Fix 2: the lane of a vector place

**`addss` xmm_xmm 32 -> c, place `reg_xmm0`.** The place is 128 bits and the cell's own `key_width` is 32, so the driver projected `Extract(31, 0, the cell's own term for this place)`.

The projected lane, LITERAL:

```
fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1)))
```

The bits above the lane, LITERAL:

```
Extract(127, 32, v0)
```

Put to the gate against `Extract(127, 32, seed_xmm0)`: **PROVED_ON_SHIP** -- z3 proved the bits above the lane are the arrival's own bits, passed through

**`addss` xmm_xmm 32 -> rust, place `reg_xmm0`.** The place is 128 bits and the cell's own `key_width` is 32, so the driver projected `Extract(31, 0, the cell's own term for this place)`.

The projected lane, LITERAL:

```
fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) + fpToFP(Extract(31, 0, v1)))
```

The bits above the lane, LITERAL:

```
Extract(127, 32, v0)
```

Put to the gate against `Extract(127, 32, seed_xmm0)`: **PROVED_ON_SHIP** -- z3 proved the bits above the lane are the arrival's own bits, passed through

**`cvtsi2sd` gpr_xmm 64 -> c, place `reg_xmm0`.** The place is 128 bits and the cell's own `key_width` is 64, so the driver projected `Extract(63, 0, the cell's own term for this place)`.

The projected lane, LITERAL:

```
fp.to_ieee_bv(fpToFP(RNE(), v0))
```

The bits above the lane, LITERAL:

```
Extract(127, 64, v0)
```

Put to the gate against `Extract(127, 64, seed_xmm0)`: **PROVED_ON_SHIP** -- z3 proved the bits above the lane are the arrival's own bits, passed through

**`cvtsi2sd` gpr_xmm 64 -> rust, place `reg_xmm0`.** The place is 128 bits and the cell's own `key_width` is 64, so the driver projected `Extract(63, 0, the cell's own term for this place)`.

The projected lane, LITERAL:

```
fp.to_ieee_bv(fpToFP(RNE(), v0))
```

The bits above the lane, LITERAL:

```
Extract(127, 64, v0)
```

Put to the gate against `Extract(127, 64, seed_xmm0)`: **PROVED_ON_SHIP** -- z3 proved the bits above the lane are the arrival's own bits, passed through


