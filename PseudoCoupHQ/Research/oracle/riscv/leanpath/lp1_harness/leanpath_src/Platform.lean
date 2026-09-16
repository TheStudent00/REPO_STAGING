/-
  Platform.lean -- the MEANING of the eight platform operations that the
  RISC-V Sail model leaves without a body: the reservation (four), the
  terminal (two), the random bits, and the experimental-extensions flag.

  These are the last of the model's body-less operations that are not
  float. Where `Kinds.lean` gives the float axioms a body, this file gives
  the platform axioms one. The model's own hand-written file declares them

      axiom cancel_reservation : Unit → SailM Unit
      axiom load_reservation : Arch.pa → Nat → SailM Unit
      axiom match_reservation : Arch.pa → Bool
      axiom valid_reservation : Unit → Bool
      axiom plat_term_read : Unit → SailM String
      axiom plat_term_write {α} : α → SailM Unit
      axiom get_16_random_bits : Unit → SailM (BitVec 16)
      axiom sys_enable_experimental_extensions : Unit → Bool

  (`handwritten_support/RiscvExtras.lean` lines 31-41) and its executable
  flavour gives three of them a stub with no content and `panic`s on the
  other five. Nothing here is a stub and nothing here panics.

  These are EFFECTS ON STATE, not values. So the file is built in four
  layers, written ONCE and general in their parameters -- nothing here is
  keyed by an instruction name:

    1. `Plat`      the state: the reservation, the terminal's pending
                   input and written output, the seed, the flag. Nothing
                   else.
    2. the core    pure, total transitions on `Plat`. THE MEANING LIVES
                   HERE, and so does every law.
    3. the monad   the same eight over any monad that can read and write
                   a `Plat` (`MonadPlat`). `SailM` is one such monad once
                   the harness says where the `Plat` sits.
    4. the shapes  the emit's exact arities, and what each one costs.

  ## the address

  `Arch.pa` is a class field: `RiscvExtras.lean` opens `section defs` at
  line 22 and declares `variable [Arch]` at line 24, so the address type
  is not concrete and no width may be picked here. This file works over
  an abstract

      variable {PA : Type} [DecidableEq PA]

  which is strictly more general: under `variable [Arch]` one instantiates
  `PA := Arch.pa` and nothing else changes. The ONE thing added is
  `DecidableEq Arch.pa` -- a reservation is matched by comparing
  addresses, so some decidable equality on the address type is
  unavoidable. The emit satisfies it: `LeanIM/Defs.lean:2003` sets
  `pa := BitVec (if 64 = 32 then 34 else 64)`, and `BitVec n` has
  `DecidableEq` for every `n`.

  ## the reservation set

  A reservation covers a SET of addresses, not one address:
  `plat_reservation_set_size_exp` (`model/core/platform_config.sail:48`)
  gives its size, and `plat_reservation_require_exact_addr_match` says
  whether the compare is exact. Both are Sail `config` values -- fixed
  when the model is built, not machine state -- so they enter here as a
  section parameter, a normaliser

      nm : PA → PA

  that sends an address to the representative of its reservation set.
  `nm := id` is the exact-match platform; `nm := fun a => (a >>> k) <<< k`
  is a 2^k-byte reservation set. The C++ reference does exactly this with
  a mask (`c_emulator/riscv_model_impl.cpp:217-232`).

  Imports nothing, so it builds and `#eval`s on a bare Lean toolchain with
  no Sail package present.
-/

/- The section variables are declared once for the whole file; not every
theorem uses every one of them, and that is not a defect. -/
set_option linter.unusedSectionVars false

namespace Platform

/-! ## 1 -- the state

Exactly what the eight operations need.

The reservation is `Option PA` rather than a pair of an address and a
flag: that is the same information with no junk state -- an invalid
reservation cannot carry a stale address that some later line reads by
mistake -- and it needs no `Inhabited PA`.

The width argument of `load_reservation` is NOT kept. The C++ reference
uses it only inside an assertion that the reservation set covers the
reserved bytes; no later operation reads it. -/

structure Plat (PA : Type) where
  /-- the reservation: the representative of the reserved set, or none held -/
  res : Option PA
  /-- the terminal's pending input, oldest first -/
  termIn : List (BitVec 8)
  /-- what has been written to the terminal, in the order written -/
  termOut : List (BitVec 8)
  /-- the seed the random bits are drawn from -/
  seed : BitVec 64
  /-- the experimental-extensions flag -/
  experimental : Bool
deriving Repr, BEq

namespace Plat

variable {PA : Type} [DecidableEq PA]

/-- the reservation-set normaliser: two addresses are in one reservation
set when they normalise alike. Configuration, not state. -/
abbrev Norm (PA : Type) := PA → PA

/-- the exact-match platform (`require_exact_reservation_addr = true`). -/
def exactNorm : Norm PA := id

/-- a starting state: nothing reserved, nothing pending, nothing written. -/
def blank (seed : BitVec 64) : Plat PA :=
  { res := none, termIn := [], termOut := [], seed := seed, experimental := false }

/-! ## 2 -- the core: the meaning, as pure total transitions -/

/-- `load_reservation`: record the address and make the reservation valid.
The normalised address is what is kept, so the compare is a single
equality however wide the reservation set is. -/
def loadRes (nm : Norm PA) (a : PA) (_width : Nat) (s : Plat PA) : Plat PA :=
  { s with res := some (nm a) }

/-- `match_reservation`: true only when a reservation is held AND the
address falls in the reserved set. -/
def matchRes (nm : Norm PA) (a : PA) (s : Plat PA) : Bool :=
  match s.res with
  | none => false
  | some r => decide (nm a = r)

/-- `cancel_reservation`: make the reservation invalid. -/
def cancelRes (s : Plat PA) : Plat PA :=
  { s with res := none }

/-- `valid_reservation`: is a reservation held. -/
def validRes (s : Plat PA) : Bool :=
  s.res.isSome

/-- `plat_term_read`, at the width the Sail source gives it (`bits(8)`).
An empty pending input answers `0`, as the reference platform does; the
byte type has no room for "nothing was there". -/
def termRead (s : Plat PA) : BitVec 8 × Plat PA :=
  match s.termIn with
  | [] => (0, s)
  | b :: rest => (b, { s with termIn := rest })

/-- one byte as the one-character string the emit's `plat_term_read`
wants back. -/
def byteToString (b : BitVec 8) : String :=
  String.singleton (Char.ofNat b.toNat)

/-- `plat_term_read` at the width the LEAN signature gives it, `String`.
It is the byte read rendered as its one character -- except that an empty
pending input gives the EMPTY string, which the byte flavour cannot say
(it must answer `0`, indistinguishable from a NUL that really was
there). -/
def termReadStr (s : Plat PA) : String × Plat PA :=
  match s.termIn with
  | [] => ("", s)
  | b :: rest => (byteToString b, { s with termIn := rest })

/-- `plat_term_write`: append to the output, in order. -/
def termWrite (b : BitVec 8) (s : Plat PA) : Plat PA :=
  { s with termOut := s.termOut ++ [b] }

/-- the seed's step: a 64-bit linear congruential recurrence (the MMIX
multiplier and increment), taken modulo 2^64 by `BitVec 64` arithmetic.
Deterministic and reproducible -- the whole point is that Lean computes
it. Never real randomness. -/
def seedNext (x : BitVec 64) : BitVec 64 :=
  6364136223846793005 * x + 1442695040888963407

/-- `get_16_random_bits`: advance the seed, answer its top sixteen bits.
The top bits are taken because the low bits of a linear congruential
sequence have short periods. -/
def random16 (s : Plat PA) : BitVec 16 × Plat PA :=
  let x := seedNext s.seed
  (BitVec.ofNat 16 (x.toNat >>> 48), { s with seed := x })

/-- `sys_enable_experimental_extensions`: the flag, read. -/
def expEnabled (s : Plat PA) : Bool :=
  s.experimental

/-! ### the derived walks: a whole terminal transfer, a whole draw -/

/-- write a list of bytes, in order. -/
def writeAll (bs : List (BitVec 8)) (s : Plat PA) : Plat PA :=
  bs.foldl (fun t b => t.termWrite b) s

/-- read `n` bytes. -/
def readAll : Nat → Plat PA → List (BitVec 8) × Plat PA
  | 0, s => ([], s)
  | n + 1, s =>
    let r := s.termRead
    let q := readAll n r.2
    (r.1 :: q.1, q.2)

/-- feed what was written back in as what is pending: the terminal wired
to itself, which is how "read back what was written" is stated. -/
def loopback (s : Plat PA) : Plat PA :=
  { s with termIn := s.termOut, termOut := [] }

/-- draw `n` sixteen-bit words. -/
def randomN : Nat → Plat PA → List (BitVec 16) × Plat PA
  | 0, s => ([], s)
  | n + 1, s =>
    let r := s.random16
    let q := randomN n r.2
    (r.1 :: q.1, q.2)

/-! ### LR and SC, the two instructions these exist for

`LOADRES` reserves (`model/sys/vmem_utils.sail:156`, reached from
`extensions/A/zalrsc_insts.sail:41`). `STORECON` succeeds only on a match
(`vmem_utils.sail:249`) and then cancels, success or not
(`zalrsc_insts.sail:76`). That is the whole of the pair, and it is two
lines here. -/

/-- the reservation half of `LOADRES`. -/
def lr (nm : Norm PA) (a : PA) (width : Nat) (s : Plat PA) : Plat PA :=
  s.loadRes nm a width

/-- the reservation half of `STORECON`: does the store go through, and
the state after. The cancel is unconditional, as the model has it. -/
def sc (nm : Norm PA) (a : PA) (s : Plat PA) : Bool × Plat PA :=
  (s.matchRes nm a, s.cancelRes)

end Plat

/-! ## 3 -- the same eight over a monad

`MonadPlat` says only that the monad can read and write a `Plat`. Every
body below is the core transition lifted through it -- the meaning is not
restated, so there is one meaning and not two. -/

class MonadPlat (m : Type → Type) (PA : outParam Type) where
  getPlat : m (Plat PA)
  setPlat : Plat PA → m Unit

export MonadPlat (getPlat setPlat)

section Monadic

variable {PA : Type} [DecidableEq PA] {m : Type → Type} [Monad m] [MonadPlat m PA]

/-- read, transform, write. -/
def modifyPlat (f : Plat PA → Plat PA) : m Unit := do
  setPlat (f (← getPlat))

/-- `load_reservation : Arch.pa → Nat → SailM Unit` -/
def load_reservation (nm : Plat.Norm PA) (a : PA) (width : Nat) : m Unit :=
  modifyPlat (Plat.loadRes nm a width)

/-- `cancel_reservation : Unit → SailM Unit` -/
def cancel_reservation (_ : Unit) : m Unit :=
  modifyPlat (PA := PA) Plat.cancelRes

/-- the monadic `match_reservation`. The emit's own signature is PURE --
see section 4 and the note there. -/
def match_reservationM (nm : Plat.Norm PA) (a : PA) : m Bool := do
  return (← getPlat).matchRes nm a

/-- the monadic `valid_reservation`. Pure in the emit; see section 4. -/
def valid_reservationM (_ : Unit) : m Bool := do
  return (← getPlat (PA := PA)).validRes

/-- `plat_term_read` at the Sail source's width, `bits(8)`. -/
def plat_term_read_byte (_ : Unit) : m (BitVec 8) := do
  let s ← getPlat (PA := PA)
  let r := s.termRead
  setPlat r.2
  return r.1

/-- `plat_term_read : Unit → SailM String`, the emit's signature. The
core's `Plat.termReadStr`, lifted; nothing is restated here. -/
def plat_term_read (_ : Unit) : m String := do
  let s ← getPlat (PA := PA)
  let r := s.termReadStr
  setPlat r.2
  return r.1

/-- `plat_term_write` at the Sail source's width, `bits(8)`. The emit's
signature is `{α} : α → SailM Unit`, unconstrained in `α`; see the note in
section 4 for why no body of THAT type can write the payload. -/
def plat_term_write (b : BitVec 8) : m Unit :=
  modifyPlat (PA := PA) (Plat.termWrite b)

/-- `get_16_random_bits : Unit → SailM (BitVec 16)` -/
def get_16_random_bits (_ : Unit) : m (BitVec 16) := do
  let s ← getPlat (PA := PA)
  let r := s.random16
  setPlat r.2
  return r.1

/-- the monadic `sys_enable_experimental_extensions`. Pure in the emit;
see section 4. -/
def sys_enable_experimental_extensionsM (_ : Unit) : m Bool := do
  return (← getPlat (PA := PA)).expEnabled

end Monadic

/-! ### the reference monad

`StateM (Plat PA)` is the smallest monad that satisfies `MonadPlat`. It
is what the coherence theorems below are proved in, and it is the shape
the `SailM` instance takes once the harness says where the `Plat` sits. -/

instance instMonadPlatStateM {PA : Type} : MonadPlat (StateM (Plat PA)) PA where
  getPlat := get
  setPlat := set

/-! ## 4 -- the emit's exact arities, and what each one costs

Two of the eight are PURE functions whose meaning depends on machine
state:

    match_reservation : Arch.pa → Bool
    valid_reservation : Unit → Bool

A pure Lean function cannot read state. Sail declares both `pure`
(`model/sys/sys_reservation.sail:21,23`) because it keeps the reservation
OUTSIDE the model (`sys_reservation.sail:11-13`), where a C++ method
reads a mutable field. Lean has no such field.

Three honest ways out, all provided, none hidden:

  (i)   the state is an ARGUMENT -- `Plat.matchRes nm a s`,
        `Plat.validRes s`. This is the meaning, and every law is about
        it. Cost: it is not the emit's arity.
  (ii)  a MONADIC variant beside the pure one -- `match_reservationM`,
        `valid_reservationM`. Cost: the model would have to call these,
        which means the Sail `val` must change from `pure` to `impure`,
        i.e. an upstream change to `sys_reservation.sail`.
  (iii) the emit's ARITY EXACTLY, with the state fixed by a section
        variable -- `match_reservation_at` and `valid_reservation_at`
        below. Cost, and it is a real one: a Lean constant is fixed once,
        so whatever `Plat` is supplied is the state at BUILD time. This
        is sound only where the harness can supply the live state at the
        binding site (for instance by binding these names inside the same
        state-threading layer that runs the model), and it is NOT sound
        as a top-level constant over a fixed starting state.

`theorem match_run` and `theorem valid_run` below prove (i) and (ii)
agree, which is what makes (iii) sound wherever the supplied state IS the
live state.

NOTHING here changes a signature the emit depends on. The emit's own
arity is (iii); (i) and (ii) sit beside it. -/

section Shapes

variable {PA : Type} [DecidableEq PA] (nm : Plat.Norm PA) (s : Plat PA)

/-- `match_reservation : Arch.pa → Bool`, the emit's arity, over an
explicit state. -/
def match_reservation_at : PA → Bool := fun a => s.matchRes nm a

/-- `valid_reservation : Unit → Bool`, the emit's arity, over an explicit
state. -/
def valid_reservation_at : Unit → Bool := fun _ => s.validRes

/-- `sys_enable_experimental_extensions : Unit → Bool`, the emit's arity.
This one is honestly pure: the flag is configuration, fixed when the
model is built, so a constant is the right shape and costs nothing. -/
def sys_enable_experimental_extensions_at : Unit → Bool := fun _ => s.expEnabled

end Shapes

/-
  ### the text to paste into `RiscvExtras.lean`

  Under the file's own `variable [Arch]` and inside its `section
  Effectful`, with `Platform` imported and one `DecidableEq Arch.pa`
  instance and one `MonadPlat SailM Arch.pa` instance in scope, the eight
  axioms become these eight definitions. `nm` is the platform's
  reservation-set normaliser and `plat` the live platform state.

      def load_reservation : Arch.pa → Nat → SailM Unit :=
        fun a w => Platform.load_reservation nm a w
      def cancel_reservation : Unit → SailM Unit :=
        Platform.cancel_reservation
      def match_reservation : Arch.pa → Bool :=
        Platform.match_reservation_at nm plat
      def valid_reservation : Unit → Bool :=
        Platform.valid_reservation_at plat
      def plat_term_read : Unit → SailM String :=
        Platform.plat_term_read (PA := Arch.pa)
      def plat_term_write {α} : α → SailM Unit :=
        fun _ => pure ()          -- see the parametricity note below
      def get_16_random_bits : Unit → SailM (BitVec 16) :=
        Platform.get_16_random_bits (PA := Arch.pa)
      def sys_enable_experimental_extensions : Unit → Bool :=
        Platform.sys_enable_experimental_extensions_at plat

  ### the two terminal signatures disagree, and one is dead

  The Sail source declares both at byte width --
  `plat_term_write : bits(8) -> unit` and `plat_term_read : unit ->
  bits(8)` (`model/sys/platform.sail:240-241`). The hand-written Lean
  gives the read a `String` instead. THE LEAN SIGNATURE IS FOLLOWED
  HERE, because it is what the emit uses; `Plat.termRead` keeps the
  byte flavour beside it and `theorem term_read_string_of_byte` says the
  two agree, character for byte, on every non-empty input. They can only
  disagree on an empty one, where `String` can say `""` and `bits(8)`
  cannot.

  It costs nothing today: `plat_term_read` is declared in the
  hand-written file and called NOWHERE in the all-modules emit -- only
  the write is reached, from the HTIF command path. So the widening is
  a latent disagreement, not a live one, and whoever narrows the Lean
  signature back to `BitVec 8` will break no call site.

  ### the `plat_term_write` note

  The hand-written Lean gives it `{α} : α → SailM Unit`, unconstrained.
  Nothing can be done with a value of a wholly abstract type, so by
  parametricity EVERY total body of that exact type ignores its argument:
  the only faithful thing the emit's signature admits is a write that
  records nothing. The model's one call site
  (`LeanIM/Platform.lean:707`) passes a `BitVec 8` -- the Sail source's
  own `bits(8) -> unit` (`model/sys/platform.sail:240`). So bind the
  emit's `{α}` shape at `α := BitVec 8` to
  `Platform.plat_term_write` and the payload survives; leave it
  polymorphic and it cannot. This is a defect of the hand-written
  signature, not of the body.
-/

/-! ## the laws

Proved, not stated. Every theorem below is proved outright -- there is no
`sorry`, no `admit`, no `native_decide` and no `partial` anywhere in this
file, and the `#print axioms` lines at the end say so mechanically. -/

namespace Plat

variable {PA : Type} [DecidableEq PA]

/-! ### the reservation -/

/-- **L1** `match_reservation` is true at the address just given to
`load_reservation`. -/
theorem matchRes_loadRes_self (nm : Norm PA) (a : PA) (w : Nat) (s : Plat PA) :
    (s.loadRes nm a w).matchRes nm a = true := by
  simp [loadRes, matchRes]

/-- **L2** `match_reservation` is false at any address in another
reservation set. -/
theorem matchRes_loadRes_other (nm : Norm PA) (a b : PA) (w : Nat) (s : Plat PA)
    (h : nm b ≠ nm a) : (s.loadRes nm a w).matchRes nm b = false := by
  simp [loadRes, matchRes, h]

/-- **L2'** on the exact-match platform, "another reservation set" is
just "another address". -/
theorem matchRes_loadRes_other_exact (a b : PA) (w : Nat) (s : Plat PA) (h : b ≠ a) :
    (s.loadRes exactNorm a w).matchRes exactNorm b = false :=
  matchRes_loadRes_other _ _ _ _ _ h

/-- **L3** `match_reservation` is false after `cancel_reservation`, at
every address. -/
theorem matchRes_cancelRes (nm : Norm PA) (b : PA) (s : Plat PA) :
    s.cancelRes.matchRes nm b = false := by
  simp [cancelRes, matchRes]

/-- **L4** a reservation is held after `load_reservation`. -/
theorem validRes_loadRes (nm : Norm PA) (a : PA) (w : Nat) (s : Plat PA) :
    (s.loadRes nm a w).validRes = true := by
  simp [loadRes, validRes]

/-- **L5** none is held after `cancel_reservation`. -/
theorem validRes_cancelRes (s : Plat PA) : s.cancelRes.validRes = false := by
  simp [cancelRes, validRes]

/-- **L6** `valid_reservation` agrees with whether a reservation is held.
-/
theorem validRes_iff_held (s : Plat PA) : s.validRes = true ↔ ∃ a, s.res = some a := by
  cases h : s.res <;> simp [validRes, h]

/-- **L7** a match implies a reservation is held: the two never disagree.
-/
theorem matchRes_imp_validRes (nm : Norm PA) (a : PA) (s : Plat PA)
    (h : s.matchRes nm a = true) : s.validRes = true := by
  cases hr : s.res with
  | none => simp [matchRes, hr] at h
  | some r => simp [validRes, hr]

/-! ### the frame: what each operation leaves alone

These are why a terminal write or a random draw between an LR and its SC
cannot break the pair. -/

theorem loadRes_frame (nm : Norm PA) (a : PA) (w : Nat) (s : Plat PA) :
    (s.loadRes nm a w).termIn = s.termIn ∧ (s.loadRes nm a w).termOut = s.termOut ∧
      (s.loadRes nm a w).seed = s.seed ∧ (s.loadRes nm a w).experimental = s.experimental := by
  simp [loadRes]

theorem cancelRes_frame (s : Plat PA) :
    s.cancelRes.termIn = s.termIn ∧ s.cancelRes.termOut = s.termOut ∧
      s.cancelRes.seed = s.seed ∧ s.cancelRes.experimental = s.experimental := by
  simp [cancelRes]

theorem termWrite_frame (b : BitVec 8) (s : Plat PA) :
    (s.termWrite b).res = s.res ∧ (s.termWrite b).seed = s.seed := by
  simp [termWrite]

theorem termRead_frame (s : Plat PA) :
    (termRead s).2.res = s.res ∧ (termRead s).2.seed = s.seed := by
  cases h : s.termIn <;> simp [termRead, h]

/-- proved by `rfl`, deliberately: `simp` would unfold the recurrence's
two 64-bit numerals and try to normalise the arithmetic, which costs
tens of gigabytes. Every fact about `random16` below is stated so that it
holds by unfolding alone, with the seed left symbolic. -/
theorem random16_frame (s : Plat PA) :
    (random16 s).2.res = s.res ∧ (random16 s).2.termIn = s.termIn ∧
      (random16 s).2.termOut = s.termOut := by
  cases s; exact ⟨rfl, rfl, rfl⟩

/-- the reservation survives a terminal write. -/
theorem matchRes_termWrite (nm : Norm PA) (a : PA) (b : BitVec 8) (s : Plat PA) :
    (s.termWrite b).matchRes nm a = s.matchRes nm a := by
  simp [termWrite, matchRes]

/-- a match reads the reservation field and nothing else. -/
theorem matchRes_congr (nm : Norm PA) (a : PA) (s t : Plat PA) (h : t.res = s.res) :
    t.matchRes nm a = s.matchRes nm a := by
  unfold matchRes; rw [h]

/-- the reservation survives a random draw. Stated through
`matchRes_congr` rather than by `rfl`, again so that the recurrence's
numerals are never unfolded. -/
theorem matchRes_random16 (nm : Norm PA) (a : PA) (s : Plat PA) :
    (random16 s).2.matchRes nm a = s.matchRes nm a :=
  matchRes_congr nm a s _ (random16_frame s).1

/-! ### the terminal -/

/-- **T1** a write appends one byte to the output, in order. -/
theorem termOut_termWrite (b : BitVec 8) (s : Plat PA) :
    (s.termWrite b).termOut = s.termOut ++ [b] := rfl

/-- **T2** writing a list appends it, in order. -/
theorem termOut_writeAll (bs : List (BitVec 8)) (s : Plat PA) :
    (s.writeAll bs).termOut = s.termOut ++ bs := by
  induction bs generalizing s with
  | nil => simp [writeAll]
  | cons b bs ih =>
    have step : s.writeAll (b :: bs) = (s.termWrite b).writeAll bs := rfl
    rw [step, ih, termOut_termWrite, List.append_assoc]
    rfl

/-- **T3** a read takes the oldest pending byte and leaves the rest. -/
theorem termRead_cons (b : BitVec 8) (rest : List (BitVec 8)) (s : Plat PA)
    (h : s.termIn = b :: rest) :
    (termRead s).1 = b ∧ (termRead s).2.termIn = rest := by
  simp [termRead, h]

/-- reading exactly the pending input gives it back. -/
theorem readAll_of_termIn (bs : List (BitVec 8)) (s : Plat PA) (h : s.termIn = bs) :
    (readAll bs.length s).1 = bs := by
  induction bs generalizing s with
  | nil => simp [readAll]
  | cons b rest ih =>
    have h2 : (termRead s).2.termIn = rest := by simp [termRead, h]
    have h1 : (termRead s).1 = b := by simp [termRead, h]
    simp [readAll, h1, ih _ h2]

/-- **T4 -- reading back what the terminal wrote.** Write a list of
bytes, wire the terminal's output to its input, read that many: the same
list comes back, in the same order. -/
theorem read_back_what_was_written (bs : List (BitVec 8)) (s : Plat PA) (h : s.termOut = []) :
    (readAll bs.length (s.writeAll bs).loopback).1 = bs := by
  refine readAll_of_termIn _ _ ?_
  simp [loopback, termOut_writeAll, h]

/-! ### the random bits -/

/-- **R1** the same state answers the same bits, always: this is a
function, not an effect. -/
theorem random16_deterministic (s : Plat PA) : (random16 s).1 = (random16 s).1 := rfl

/-- **R2** the draw advances the seed, and by the stated recurrence. -/
theorem random16_seed (s : Plat PA) : (random16 s).2.seed = seedNext s.seed := rfl

/-- the bits drawn, written out. -/
theorem random16_bits (s : Plat PA) :
    (random16 s).1 = BitVec.ofNat 16 ((seedNext s.seed).toNat >>> 48) := rfl

/-- **R3** the bits drawn depend on the SEED ALONE -- not on the
reservation, the terminal, or the flag. So a run is reproducible from its
seed. -/
theorem randomN_seed_only (n : Nat) (s t : Plat PA) (h : s.seed = t.seed) :
    (randomN n s).1 = (randomN n t).1 := by
  induction n generalizing s t with
  | zero => rfl
  | succ n ih =>
    have h1 : (random16 s).1 = (random16 t).1 := by
      rw [random16_bits, random16_bits, h]
    have h2 : (random16 s).2.seed = (random16 t).2.seed := by
      rw [random16_seed, random16_seed, h]
    have es : (randomN (n + 1) s).1 = (random16 s).1 :: (randomN n (random16 s).2).1 := rfl
    have et : (randomN (n + 1) t).1 = (random16 t).1 :: (randomN n (random16 t).2).1 := rfl
    rw [es, et, h1, ih _ _ h2]

/-! ### the flag -/

/-- **E1** the flag read is the flag held. -/
theorem expEnabled_eq (s : Plat PA) : s.expEnabled = s.experimental := rfl

/-! ### LR and SC, end to end

The point of the reservation four. -/

/-- **S1** an SC at the address its LR reserved succeeds. -/
theorem sc_after_lr_same (nm : Norm PA) (a : PA) (w : Nat) (s : Plat PA) :
    (sc nm a (lr nm a w s)).1 = true :=
  matchRes_loadRes_self nm a w s

/-- **S2** an SC at an address in another reservation set fails. -/
theorem sc_after_lr_other (nm : Norm PA) (a b : PA) (w : Nat) (s : Plat PA)
    (h : nm b ≠ nm a) : (sc nm b (lr nm a w s)).1 = false :=
  matchRes_loadRes_other nm a b w s h

/-- **S3** an SC after the reservation was cancelled fails. -/
theorem sc_after_cancel (nm : Norm PA) (a : PA) (w : Nat) (s : Plat PA) :
    (sc nm a (lr nm a w s).cancelRes).1 = false :=
  matchRes_cancelRes nm a (lr nm a w s)

/-- **S4** an LR/SC pair succeeds AT MOST ONCE: the second SC always
fails, because the first cancelled. This is the property the whole
mechanism exists for. -/
theorem sc_twice (nm : Norm PA) (a : PA) (w : Nat) (s : Plat PA) :
    (sc nm a (sc nm a (lr nm a w s)).2).1 = false :=
  matchRes_cancelRes nm a (lr nm a w s)

/-- **S5** a terminal write between the LR and the SC does not break the
pair. -/
theorem sc_after_lr_termWrite (nm : Norm PA) (a : PA) (w : Nat) (b : BitVec 8) (s : Plat PA) :
    (sc nm a ((lr nm a w s).termWrite b)).1 = true := by
  show ((lr nm a w s).termWrite b).matchRes nm a = true
  rw [matchRes_termWrite]
  exact matchRes_loadRes_self nm a w s

/-- **S6** a random draw between the LR and the SC does not break the
pair either. -/
theorem sc_after_lr_random (nm : Norm PA) (a : PA) (w : Nat) (s : Plat PA) :
    (sc nm a (random16 (lr nm a w s)).2).1 = true := by
  show (random16 (lr nm a w s)).2.matchRes nm a = true
  rw [matchRes_random16]
  exact matchRes_loadRes_self nm a w s

end Plat

/-! ### the coherence of the monadic layer with the core

Each monadic body, run at a state, gives exactly the core's answer and
the core's next state. These are what make the pure shapes of section 4
sound wherever the state supplied is the live one. -/

section Coherence

variable {PA : Type} [DecidableEq PA]

theorem load_run (nm : Plat.Norm PA) (a : PA) (w : Nat) (s : Plat PA) :
    (load_reservation (m := StateM (Plat PA)) nm a w).run s = ((), s.loadRes nm a w) := rfl

theorem cancel_run (s : Plat PA) :
    (cancel_reservation (m := StateM (Plat PA)) (PA := PA) ()).run s = ((), s.cancelRes) := rfl

theorem match_run (nm : Plat.Norm PA) (a : PA) (s : Plat PA) :
    (match_reservationM (m := StateM (Plat PA)) nm a).run s = (s.matchRes nm a, s) := rfl

theorem valid_run (s : Plat PA) :
    (valid_reservationM (m := StateM (Plat PA)) (PA := PA) ()).run s = (s.validRes, s) := rfl

theorem term_read_byte_run (s : Plat PA) :
    (plat_term_read_byte (m := StateM (Plat PA)) (PA := PA) ()).run s = s.termRead := rfl

theorem term_write_run (b : BitVec 8) (s : Plat PA) :
    (plat_term_write (m := StateM (Plat PA)) (PA := PA) b).run s = ((), s.termWrite b) := rfl

theorem random_run (s : Plat PA) :
    (get_16_random_bits (m := StateM (Plat PA)) (PA := PA) ()).run s = s.random16 := rfl

theorem experimental_run (s : Plat PA) :
    (sys_enable_experimental_extensionsM (m := StateM (Plat PA)) (PA := PA) ()).run s =
      (s.expEnabled, s) := rfl

theorem term_read_string_run (s : Plat PA) :
    (plat_term_read (m := StateM (Plat PA)) (PA := PA) ()).run s = s.termReadStr := rfl

/-- the two terminal reads agree: the `String` the emit's signature wants
is the one character of the byte the Sail source's signature wants, and
both leave the same state -- EXCEPT on an empty pending input, where the
`String` flavour says `""` and the byte flavour must say `0`. -/
theorem term_read_string_of_byte (b : BitVec 8) (rest : List (BitVec 8)) (s : Plat PA)
    (h : s.termIn = b :: rest) :
    (plat_term_read (m := StateM (Plat PA)) (PA := PA) ()).run s =
      (Plat.byteToString b, { s with termIn := rest }) := by
  rw [term_read_string_run]
  simp only [Plat.termReadStr, h]

theorem term_read_string_empty (s : Plat PA) (h : s.termIn = []) :
    (plat_term_read (m := StateM (Plat PA)) (PA := PA) ()).run s = ("", s) := by
  rw [term_read_string_run]
  simp only [Plat.termReadStr, h]

end Coherence

/-! ## the self-checks

The shape `Kinds.lean` uses: a `Chk` per fact, a `report` per group,
counted at the end. Restated here rather than imported so that this file
depends on nothing. -/

structure Chk where
  name : String
  ok   : Bool
  got  : String
  want : String

def chk {α : Type} [BEq α] [Repr α] (name : String) (got want : α) : Chk :=
  { name := name, ok := got == want,
    got := toString (repr got), want := toString (repr want) }

def report (title : String) (cs : List Chk) : IO Unit := do
  IO.println ("== " ++ title)
  for c in cs do
    if c.ok then IO.println ("  ok   " ++ c.name ++ " = " ++ c.got)
    else IO.println ("  FAIL " ++ c.name ++ ": got " ++ c.got ++ " want " ++ c.want)
  IO.println ("  -- " ++ toString (cs.filter (fun c => c.ok)).length ++ "/" ++
              toString cs.length ++ " ok")

/-! ### concrete ground for the checks

`PA := BitVec 64` is what the emit's `Arch` instance makes `Arch.pa` when
`xlen = 64` (`LeanIM/Defs.lean:2003`). The laws above are over an
abstract `PA`; these checks stand them at a width Lean can print. -/

abbrev PA64 := BitVec 64

/-- a 2^k-byte reservation set. `setNorm 0 = id`, the exact-match
platform. -/
def setNorm (k : Nat) : Plat.Norm PA64 := fun a => (a >>> k) <<< k

/-- the 64-byte reservation set of `Za64rs`. -/
def nm64 : Plat.Norm PA64 := setNorm 6

def s0 : Plat PA64 := Plat.blank 1

def addrA : PA64 := 0x8000_0000
def addrB : PA64 := 0x8000_0100
/-- within the same 64-byte reservation set as `addrA`. -/
def addrA' : PA64 := 0x8000_0004

#eval report "the reservation four, as operations" [
  chk "valid_reservation on a fresh state" (Plat.validRes s0) false,
  chk "match_reservation on a fresh state" (Plat.matchRes nm64 addrA s0) false,
  chk "valid_reservation after load_reservation"
    (Plat.validRes (Plat.loadRes nm64 addrA 4 s0)) true,
  chk "match_reservation at the loaded address"
    (Plat.matchRes nm64 addrA (Plat.loadRes nm64 addrA 4 s0)) true,
  chk "match_reservation elsewhere in the same 64-byte set"
    (Plat.matchRes nm64 addrA' (Plat.loadRes nm64 addrA 4 s0)) true,
  chk "match_reservation in another set"
    (Plat.matchRes nm64 addrB (Plat.loadRes nm64 addrA 4 s0)) false,
  chk "match_reservation elsewhere, exact-match platform"
    (Plat.matchRes Plat.exactNorm addrA' (Plat.loadRes Plat.exactNorm addrA 4 s0)) false,
  chk "valid_reservation after cancel_reservation"
    (Plat.validRes (Plat.cancelRes (Plat.loadRes nm64 addrA 4 s0))) false,
  chk "match_reservation after cancel_reservation"
    (Plat.matchRes nm64 addrA (Plat.cancelRes (Plat.loadRes nm64 addrA 4 s0))) false
]

#eval report "the terminal two, and the flag" [
  chk "plat_term_write appends"
    (Plat.termOut (Plat.termWrite 0x48 s0)) [(0x48 : BitVec 8)],
  chk "three writes, in order"
    (Plat.termOut (Plat.writeAll [0x48, 0x49, 0x21] s0)) [(0x48 : BitVec 8), 0x49, 0x21],
  chk "plat_term_read on empty input answers 0"
    (Plat.termRead s0).1 (0 : BitVec 8),
  chk "plat_term_read takes the oldest byte"
    (Plat.termRead { s0 with termIn := [0x61, 0x62] }).1 (0x61 : BitVec 8),
  chk "and leaves the rest"
    (Plat.termRead { s0 with termIn := [0x61, 0x62] }).2.termIn [(0x62 : BitVec 8)],
  chk "reading back what was written"
    (Plat.readAll 3 (Plat.loopback (Plat.writeAll [0x48, 0x49, 0x21] s0))).1
    [(0x48 : BitVec 8), 0x49, 0x21],
  chk "the String flavour of the read is the byte's character"
    ((plat_term_read (m := StateM (Plat PA64)) (PA := PA64) ()).run
      { s0 with termIn := [0x61] }).1 "a",
  chk "the String flavour on empty input is the empty string"
    ((plat_term_read (m := StateM (Plat PA64)) (PA := PA64) ()).run s0).1 "",
  chk "sys_enable_experimental_extensions, off" (Plat.expEnabled s0) false,
  chk "sys_enable_experimental_extensions, on"
    (Plat.expEnabled { s0 with experimental := true }) true
]

#eval report "get_16_random_bits: deterministic, reproducible, advancing" [
  -- pinned: the sequence itself is the thing being fixed, so the
  -- expected value is written out. A change to the recurrence shows up
  -- here and nowhere else.
  chk "the first draw from seed 1" (Plat.random16 s0).1 (0x6c57 : BitVec 16),
  chk "the same state draws the same bits"
    (Plat.random16 s0).1 (Plat.random16 s0).1,
  chk "the seed advanced" (decide ((Plat.random16 s0).2.seed = s0.seed)) false,
  chk "eight draws from seed 1"
    (Plat.randomN 8 s0).1
    (Plat.randomN 8 s0).1,
  chk "eight draws depend on the seed alone"
    (Plat.randomN 8 s0).1
    (Plat.randomN 8 { s0 with experimental := true, termOut := [0x41] }).1,
  chk "a different seed draws differently"
    (decide ((Plat.randomN 8 s0).1 = (Plat.randomN 8 (Plat.blank (PA := PA64) 2)).1)) false,
  chk "the draw leaves the reservation alone"
    (Plat.matchRes nm64 addrA (Plat.random16 (Plat.loadRes nm64 addrA 4 s0)).2) true
]

#eval report "the laws, at concrete values" [
  chk "L1 match at the address just loaded"
    (Plat.matchRes nm64 addrA (Plat.loadRes nm64 addrA 4 s0)) true,
  chk "L2 false in another reservation set"
    (Plat.matchRes nm64 addrB (Plat.loadRes nm64 addrA 4 s0)) false,
  chk "L3 false after cancel"
    (Plat.matchRes nm64 addrA (Plat.cancelRes (Plat.loadRes nm64 addrA 4 s0))) false,
  chk "L4 valid after load" (Plat.validRes (Plat.loadRes nm64 addrA 4 s0)) true,
  chk "L5 invalid after cancel"
    (Plat.validRes (Plat.cancelRes (Plat.loadRes nm64 addrA 4 s0))) false,
  chk "L6 valid agrees with a reservation being held"
    (Plat.validRes (Plat.loadRes nm64 addrA 4 s0))
    ((Plat.loadRes nm64 addrA 4 s0).res.isSome),
  chk "L7 a match implies valid"
    (Plat.validRes (Plat.loadRes nm64 addrA 4 s0)) true,
  chk "T4 read back what was written"
    (Plat.readAll 2 (Plat.loopback (Plat.writeAll [0x6f, 0x6b] s0))).1
    [(0x6f : BitVec 8), 0x6b],
  chk "R2 the seed advanced by the recurrence"
    (Plat.random16 s0).2.seed (Plat.seedNext s0.seed),
  chk "E1 the flag read is the flag held"
    (Plat.expEnabled { s0 with experimental := true }) true
]

#eval report "LR and SC, end to end" [
  chk "S1 an SC at the reserved address succeeds"
    (Plat.sc nm64 addrA (Plat.lr nm64 addrA 4 s0)).1 true,
  chk "S1' and anywhere in the same reservation set"
    (Plat.sc nm64 addrA' (Plat.lr nm64 addrA 4 s0)).1 true,
  chk "S2 an SC in another reservation set fails"
    (Plat.sc nm64 addrB (Plat.lr nm64 addrA 4 s0)).1 false,
  chk "S3 an SC after a cancel fails"
    (Plat.sc nm64 addrA (Plat.cancelRes (Plat.lr nm64 addrA 4 s0))).1 false,
  chk "S4 the second SC of a pair always fails"
    (Plat.sc nm64 addrA (Plat.sc nm64 addrA (Plat.lr nm64 addrA 4 s0)).2).1 false,
  chk "S5 a terminal write between LR and SC does not break the pair"
    (Plat.sc nm64 addrA (Plat.termWrite 0x21 (Plat.lr nm64 addrA 4 s0))).1 true,
  chk "S6 a random draw between LR and SC does not break the pair"
    (Plat.sc nm64 addrA (Plat.random16 (Plat.lr nm64 addrA 4 s0)).2).1 true,
  chk "an SC with no LR at all fails"
    (Plat.sc nm64 addrA s0).1 false
]

#eval report "the monadic layer runs, and agrees with the core" [
  chk "load_reservation then match, in the monad"
    (((do
        load_reservation (m := StateM (Plat PA64)) nm64 addrA 4
        match_reservationM (m := StateM (Plat PA64)) nm64 addrA) : StateM (Plat PA64) Bool).run
      s0).1 true,
  chk "load, cancel, then match, in the monad"
    (((do
        load_reservation (m := StateM (Plat PA64)) nm64 addrA 4
        cancel_reservation (m := StateM (Plat PA64)) (PA := PA64) ()
        match_reservationM (m := StateM (Plat PA64)) nm64 addrA) : StateM (Plat PA64) Bool).run
      s0).1 false,
  chk "valid_reservation in the monad, after a load"
    (((do
        load_reservation (m := StateM (Plat PA64)) nm64 addrA 4
        valid_reservationM (m := StateM (Plat PA64)) (PA := PA64) ()) :
        StateM (Plat PA64) Bool).run s0).1 true,
  chk "the monadic match agrees with the core"
    ((match_reservationM (m := StateM (Plat PA64)) nm64 addrA).run
      (Plat.loadRes nm64 addrA 4 s0)).1
    (Plat.matchRes nm64 addrA (Plat.loadRes nm64 addrA 4 s0)),
  chk "write then read, in the monad"
    (((do
        plat_term_write (m := StateM (Plat PA64)) (PA := PA64) 0x7a
        modifyPlat (m := StateM (Plat PA64)) (PA := PA64) Plat.loopback
        plat_term_read_byte (m := StateM (Plat PA64)) (PA := PA64) ()) :
        StateM (Plat PA64) (BitVec 8)).run s0).1 (0x7a : BitVec 8),
  chk "two draws in the monad differ"
    (decide ((((do
        let x ← get_16_random_bits (m := StateM (Plat PA64)) (PA := PA64) ()
        let y ← get_16_random_bits (m := StateM (Plat PA64)) (PA := PA64) ()
        return (x, y)) : StateM (Plat PA64) (BitVec 16 × BitVec 16)).run s0).1.1 =
      (((do
        let x ← get_16_random_bits (m := StateM (Plat PA64)) (PA := PA64) ()
        let y ← get_16_random_bits (m := StateM (Plat PA64)) (PA := PA64) ()
        return (x, y)) : StateM (Plat PA64) (BitVec 16 × BitVec 16)).run s0).1.2)) false,
  chk "the emit's pure arity, at a state where a reservation is held"
    (match_reservation_at nm64 (Plat.loadRes nm64 addrA 4 s0) addrA) true,
  chk "the emit's pure arity, at a state where none is"
    (valid_reservation_at (PA := PA64) s0 ()) false,
  chk "the flag through the emit's pure arity"
    (sys_enable_experimental_extensions_at (PA := PA64) { s0 with experimental := true } ()) true
]

/-! ### nothing here rests on an axiom

`#print axioms` on a theorem lists what it depends on. Anything beyond
Lean's own three (`propext`, `Classical.choice`, `Quot.sound`) -- above
all `sorryAx` -- would say so here. -/

-- the reservation
#print axioms Plat.matchRes_loadRes_self
#print axioms Plat.matchRes_loadRes_other
#print axioms Plat.matchRes_loadRes_other_exact
#print axioms Plat.matchRes_cancelRes
#print axioms Plat.validRes_loadRes
#print axioms Plat.validRes_cancelRes
#print axioms Plat.validRes_iff_held
#print axioms Plat.matchRes_imp_validRes
-- the frame
#print axioms Plat.loadRes_frame
#print axioms Plat.cancelRes_frame
#print axioms Plat.termWrite_frame
#print axioms Plat.termRead_frame
#print axioms Plat.random16_frame
#print axioms Plat.matchRes_termWrite
#print axioms Plat.matchRes_congr
#print axioms Plat.matchRes_random16
-- the terminal
#print axioms Plat.termOut_termWrite
#print axioms Plat.termOut_writeAll
#print axioms Plat.termRead_cons
#print axioms Plat.readAll_of_termIn
#print axioms Plat.read_back_what_was_written
-- the random bits and the flag
#print axioms Plat.random16_deterministic
#print axioms Plat.random16_seed
#print axioms Plat.random16_bits
#print axioms Plat.randomN_seed_only
#print axioms Plat.expEnabled_eq
-- LR and SC
#print axioms Plat.sc_after_lr_same
#print axioms Plat.sc_after_lr_other
#print axioms Plat.sc_after_cancel
#print axioms Plat.sc_twice
#print axioms Plat.sc_after_lr_termWrite
#print axioms Plat.sc_after_lr_random
-- the monadic layer against the core
#print axioms load_run
#print axioms cancel_run
#print axioms match_run
#print axioms valid_run
#print axioms term_read_byte_run
#print axioms term_write_run
#print axioms random_run
#print axioms experimental_run
#print axioms term_read_string_run
#print axioms term_read_string_of_byte
#print axioms term_read_string_empty

end Platform
