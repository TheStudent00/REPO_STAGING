# log 141 — the virtual-memory canonical form, explained (saved
# understanding)

Date: 2026-09-02. the owner: "please save that understanding of it."
This is the teaching-form explanation accepted in conversation,
plus §8, which answers the owner's follow-up about contiguity and how
the arch-unit coordinates with the virtual memory. AgentMemory
points here under "THE VIRTUAL-MEMORY FORM — SEE LOG 135".

# 1. The idea in one paragraph

Every arch-unit is rewritten as if it ran on one imaginary machine
that has no favourite registers and unlimited, pre-labelled
memory. Every value the unit ever touches — each input, each
constant, each intermediate, the answer, even an address the unit
computes — gets its own labelled BLOCK in that memory, labelled by
what the value IS (its lineage), not by where the compiler put it.
Registers still exist, but only as scratch vehicles: a value is
loaded from its block, operated on, and stored back to its block,
by one fixed loading rule that is the same for every unit in every
language. Two units are then compared as what they do to the
labelled memory; everything the compiler chose — which register,
which stack offset, spill or no spill — has been erased.

# 2. Why registers were the wrong foundation

- Scarcity: 16 registers; more live values than that forces
  spills, and a register-home form can only refuse (36 units did).
- Compiler idiosyncrasy: c puts a in %rdi, go in %rax, a
  struct-returning rust unit puts a result ADDRESS in %rdi and
  shifts a over; every convention became a special case (5 units).
- Memory-resident answers are invisible to register comparison:
  an address-of unit's answer is a stack address (6 units
  disproved when a memory patch moved the slot).
- Common cause: treating WHERE the compiler put a value as part of
  the unit's identity. Identity is what it computes from its
  inputs; where things sit is bookkeeping.

# 3. The layout — typed blocks, labelled rows

| block | row | holds | who fills it |
|---|---|---|---|
| IN | 0,1,… | each input as it arrived | the caller (arrival contract) |
| CONST | 0,1,… | each literal the unit uses | the unit's text |
| TEMP | 0,1,… | each intermediate value | the computation |
| OWN | 0,… | a slot the unit owns, if it takes its address | the unit |
| GUARD | 0,… | outcome of a check | a guard |
| OUT | 0 | the answer | the computation |

- A block per LINEAGE, not per role: a transformed input stays in
  its input's lineage (TEMP rows attributed to IN-k).
- Empty blocks are information ("this unit has no guards").
- The loading rule: scratch registers by order of need (%r10,
  %r11, %r9, %r8, …), never by role. load block -> scratch; op;
  store scratch -> block. Fixed rule => same computation gives the
  same text.

# 4. Worked example — three languages, one entry

c `lea (%rdi,%rsi,1),%rax`; go `mov %rax,%rcx ; add %rbx,%rcx`;
cpython `mov 0x10(%rdi),%rax ; mov 0x10(%rsi),%rdx ; shr $3 … ;
lea (%rax,%rdx,1),%rdi` — three conventions, three instruction
choices, one arrival difference. In the virtual form all three
compute:

    load IN-0 -> %r10 ; load IN-1 -> %r11 ; add %r11,%r10 ;
    store %r10 -> OUT-0 ; ret

with a = 5, b = 9 moving: IN-0=5, IN-1=9 -> %r10=5, %r11=9 ->
%r10=14 -> OUT-0=14. c and go match because the simplifier already
renders one fixed instruction for a two-operand sum. CPython
matches on its COMPUTATION; its unpacking (load field +0x10, shift
right 3) is ARRIVAL, recorded as an annotation on IN-0/IN-1
("typed-pointer(PyLongObject*)"), never in the text. The merged
pool entry: one text, members c/cpp/go/rust/cpython with language
and arrival as columns.

# 5. The address-of unit

`&a`: the answer is the ADDRESS where a is stored. Round 8's patch
put its slots at -0x8(%rsp) etc. — the very slot the answer names
— so the rewrite moved a and the answer changed: disproved. In the
virtual form: store a to OWN-0; the answer is OWN-0's address, a
standardized virtual address, identical for every address-of unit
in every language. Nothing collides: the unit's own slot has its
own block.

# 6. Why it runs on real hardware

The virtual region is mapped to real memory at run time; every
block address becomes a real address; every load/store is a real
instruction. The text is assembler-valid throughout. (§8 says HOW
the mapping works without requiring contiguity.)

# 7. Questions answered in advance

- Loads don't change the computation: the proof obligation is
  relative to the arrival contract, checked by the gate against
  the unit's own machine code.
- More temps than scratch registers: more TEMP rows, same fixed
  order; no cap, no refusal.
- Third or hidden argument: IN-2, IN-3, …; a struct-return pointer
  is an IN row annotated "result destination". No special case.
- Pointer arrival is not hidden: it is the arrival column. Same
  instructions + different modes = information, never discarded.
- Why not designated registers + memory overflow: that was round
  8; it broke on the first address-valued answer.

# 8. the owner's contiguity concern, and the ledger

the owner: "i have some issues with the dependency on contiguous-ness
and the way that the arch-unit coordinates with the virtual
memory … im not sure if we are able to place a ledger of
allocated memory in ram. i feel like there surely must be a
solution to this."

## 8.1 The concern, stated

- §3's picture used one region with fixed offsets (V+0x00,
  V+0x08, …). That makes the form depend on CONTIGUITY: it
  assumes all blocks sit in one run of addresses at fixed
  distances. Real memory need not offer that, and a layout that
  bakes offsets into the text is another kind of "where" leaking
  into identity.

## 8.2 The solution: a ledger, and two-step addressing

- Replace fixed offsets with a LEDGER: a small table in RAM, one
  entry per block, holding that block's real base address. The
  ledger itself has ONE known base (a register or a single known
  address), and its entries are in fixed order (IN, CONST, TEMP,
  OWN, GUARD, OUT), so "block k" is always "ledger entry k".
- A unit addresses memory in two steps: read the block's base
  from the ledger, then read the row within the block:

    load  LEDGER[IN]   -> %r10      the base of the IN block
    load  (%r10 + 0)   -> %r10      IN-0's value
    load  LEDGER[IN]   -> %r11
    load  (%r11 + 8)   -> %r11      IN-1's value
    add   %r11, %r10
    load  LEDGER[OUT]  -> %r11
    store %r10 -> (%r11 + 0)        OUT-0

- Blocks may now live ANYWHERE. Contiguous, scattered, on the
  stack, on the heap, in separate pages — the text is identical
  because it names blocks by ledger entry, never by absolute or
  relative address. The runner allocates the blocks however it
  likes and fills the ledger before the unit runs.
- Yes, a ledger can be placed in RAM: it is an ordinary array of
  pointers. The only fixed thing in the whole scheme is the
  ledger's own base, which the runner passes in one register (or
  at one known address) — the same way any calling convention
  passes one thing.

## 8.3 What this buys, in the owner's terms

- Universality: the text references nothing about the machine's
  layout. Two units are equal when their ledger-relative texts are
  equal — equivalence is evaluated on the text alone, which is
  the point of standardizing.
- Runnable: every instruction is real; the runner is a few lines
  that allocate blocks and fill the ledger. Speed is not a goal
  (the owner: "im not concerned with arch-unit canon form running
  fast"), and the extra load per access is the whole price.
- The address-of case is cleaner still: the unit's answer is
  "the address of OWN-0", computed as LEDGER[OWN] + 0 — the
  runner decides what real address that is, and two address-of
  units still produce identical text.

## 8.4 The coordination between arch-unit and virtual memory

- The unit never knows real addresses. It knows: the ledger base,
  the fixed order of blocks, and row offsets within a block. That
  is the entire contract.
- The runner knows: how big each block must be (read from the
  unit's row counts), where it chose to put them, and it writes
  the ledger. Arrival = the runner filling IN rows; return = the
  runner reading OUT-0.
- Equivalence checking never involves the runner at all; it
  compares texts (and, when texts differ, proves them equal over
  the ledger-relative model).
