/-
  Containers.lean -- the universal type's CONTAINER form, and its bridge
  to the containers Sail's RISC-V model actually holds many values in.
  Written once, general in its parameters; nothing in this file is keyed
  by an instruction name, an operator token or a container kind.

  the owner's decision, verbatim:

    "universal container could be a dict-list"

  So a container is a LIST OF (KEY, VALUE) PAIRS, the key a universal
  value. ONE shape serves all three of the model's containers:

      Sail's container     the key                     the value
      ------------------   -------------------------   -----------------
      Vector α n           0 … n-1                     the element
      memory               the address                 the byte
      a record or a text   the field's position, or    the field
                           its name read as bits

  and the register file is the vector case at n = 32.

  `Universal.lean` holds the one element; this file holds the one
  container over it. It imports `Universal` and nothing else -- in
  particular it does NOT import the Sail emit, so it builds whether or
  not the model is built, and churn in the model cannot break it. The
  three Sail primitives it bridges to (`vectorUpdate`, `vectorInit`,
  `Vector.length`) are TRANSCRIBED here, exactly as `Universal.lean`
  transcribes `to_bits_truncate` as `sailToBitsTruncate`.

  ## what is honest about this file

  Five things are compromises or open questions, and none of them is
  papered over in the code below. Each is marked again where it bites.

  1. THE LENGTH LIVES IN SAIL'S TYPE, NOT IN THE CONTAINER.
     Sail's container is `Vector α n`: `n` is part of the type, so a
     Sail vector can never be the wrong length, and `Vector.length` is
     a projection out of the type rather than a measurement of the
     value. A dict-list has no length in its type. Consequences, all
     of them forced:
       - `ofVector` loses nothing, and `length_ofVector` recovers `n`
         as a THEOREM about the value instead of reading it off a type;
       - `toVector` must be TOLD the length -- it cannot be read off a
         dict-list, because a dict-list may hold any keys at all;
       - only ONE of the two round trips is an identity. Vector to
         dict-list and back is proved. Dict-list to vector and back is
         FALSE in general (a dict-list with a key outside 0 … n-1, or
         with a repeated key, is not the image of any `Vector α n`),
         so it is not stated.
       - `set` at a key outside 0 … n-1 GROWS the dict-list, where
         Sail's `vectorUpdate` at an index outside the type cannot be
         written at all. The two agree only in bounds, and every
         bridge theorem below carries the in-bounds hypothesis.

  2. KEYS COMPARE STRUCTURALLY, NOT BY VALUE.
     `Uni` already derives `DecidableEq`, so key equality is decided;
     but the universal type does not have unique spellings -- `4` is
     `(mant 4, expo 0)` and also `(mant 1, expo 2)`, one value and two
     objects, and those are two DIFFERENT keys here. All three of the
     containers above key by an INTEGER, and `key : Nat → Uni` gives
     one spelling per integer -- `key_inj` proves distinct integers
     give distinct keys -- so the containers this file is for are
     sound. A container keyed by an arbitrary universal value would
     need a value-equality test on `Uni` (a canonical form, or
     `Uni.cmp _ _ = .eq` shown to be an equivalence). That is NOT
     written here. See the question in the report.

  3. THE VALUE TYPE IS A PARAMETER; THE DECIDED FORM IS `UDict`.
     `Dict α` is the one implementation, and `UDict := Dict Uni` is the
     decided dict-list: key universal, value universal. The parameter
     is not a second design -- it is what "written once" costs, because
     two of Sail's own vectors cannot be `Dict Uni`:
       - `Vector (Option TLB_Entry) 64` (`LeanIM/VmemTlb.lean`): the
         element is not a number at all;
       - `vectorInit (vectorInit (zeros (n := SEW)))`
         (`LeanIM/VextUtilsInsts.lean:686`): a vector OF VECTORS, and
         `Uni` is flat -- it cannot hold a container.
     With the parameter, those are `Dict (Option TLB_Entry)` and
     `Dict (Dict Uni)` with the same code and the same proofs. Without
     it they have no container form at all. Question for the owner.

  4. THE SAIL SIDE IS A TRANSCRIPTION, NOT THE PACKAGE.
     The lean-sail package is not on this host -- the emit's build
     fetches it (`[[require]] name = "Sail" … rev = "v5"`) and the
     built copy lives in the sandbox at
     `/work/proof/.lake/packages/Sail/`. So `vectorUpdate`,
     `vectorInit` and `Vector.length` are transcribed below from their
     USES in the emit, against Lean core's `Vector α n` (which is the
     type the emit's own spelling `Vector (BitVec 32) 4` denotes).
     The bridge theorems are proved against the transcription. The
     lane `lanes_lp1/lp1_l23_containers_against_the_real_lean_sail.sh`
     prints the package's own definitions, proves the transcription
     equals them by `rfl`, and restates every bridge theorem over the
     package's own names -- that is the step this file cannot take on
     a host the package is not on. Until that lane has run green, the
     five bridge theorems hold OF THE TRANSCRIPTION, which is a weaker
     thing than holding of Sail.

  5. MEMORY HAS NO BRIDGE STATEMENT HERE, DELIBERATELY.
     The read-back law IS proved -- on the container (`load_store_same`
     and `load_store_other`). What is NOT stated is the bridge to the
     model's own memory, because the model's `vmem_read` / `vmem_write`
     bottom out in the package's `readReg` / `writeReg` / `writeByte`
     in `Sail/ConcurrencyInterfaceV1.lean`, a monadic machine that is
     not on this host and whose read-after-write lemma we have never
     seen. Assuming it would be assuming the thing the section is
     supposed to prove, so the statement is left out and said instead.
-/

import Universal

namespace Containers

open Universal

/-! ## the keys

A key is a universal value. The three containers all key by an integer,
and `key` is the one spelling of an integer used as a key: `ofInt`, so
`mant` carries the integer and `expo` is zero. `key_inj` is what makes
structural key equality sound for them. -/

/-- the key of an index, an address, or a field's position. -/
def key (i : Nat) : Uni := Uni.ofInt (i : Int)

/-- the key of a signed integer, for the containers whose keys may run
below zero. -/
def keyI (i : Int) : Uni := Uni.ofInt i

/-- the key of a NAME, read the way the project's text canon reads a
text: the utf-8 bytes as one unbounded bit_vec, with a leading 1 so a
leading zero byte is not lost. A record keyed by field names needs no
second container form -- a name IS a universal value. -/
def keyOfName (s : String) : Uni :=
  Uni.ofInt ((s.toUTF8.toList.foldl (fun acc b => acc * 256 + b.toNat) 1 : Nat) : Int)

/-- an integer key reads back as itself: `ofInt` is the one spelling. -/
theorem toInt_ofInt (n : Int) : (Uni.ofInt n).toInt = n := by
  by_cases h : n < 0 <;>
    simp [Uni.ofInt, Uni.ofSignedAt, Uni.mk', Uni.toInt, Uni.smant, Uni.isNeg, Uni.e,
          Expo.ofInt, Expo.val, h] <;> omega

theorem keyI_inj {i j : Int} : keyI i = keyI j ↔ i = j := by
  constructor
  · intro h
    have := congrArg Uni.toInt h
    simpa [keyI, toInt_ofInt] using this
  · intro h; rw [h]

theorem key_inj {i j : Nat} : key i = key j ↔ i = j := by
  constructor
  · intro h
    have : ((i : Int)) = ((j : Int)) := keyI_inj.mp h
    omega
  · intro h; rw [h]

theorem key_ne {i j : Nat} (h : i ≠ j) : key i ≠ key j := fun he => h (key_inj.mp he)

/-! ## the type

The dict-list: a list of (key, value) pairs. The key is always a
universal value; `UDict` is the decided form, where the value is one
too. The value type is a parameter so that ONE implementation and ONE
set of proofs serve the model's vectors of non-numbers and its vectors
of vectors -- see note 3 in the header. -/

/-- **the universal container**: a dict-list, a list of (key, value)
pairs whose key is a universal value. -/
structure Dict (α : Type) where
  cells : List (Uni × α)
deriving Repr, Inhabited, BEq, DecidableEq

/-- the decided form: key universal, value universal. -/
abbrev UDict := Dict Uni

namespace Dict

variable {α β : Type}

/-! ## the operations

Each is written on the cells and lifted, so the laws below are list
inductions and nothing else. `get` reads the FIRST cell with the key,
`set` rewrites that cell in place and appends only when the key is new
-- which is what makes `set` at a key already present leave the length
alone, and what makes a repeated key harmless. -/

def getCells (dflt : α) (k : Uni) : List (Uni × α) → α
  | [] => dflt
  | (k', v') :: t => if k' = k then v' else getCells dflt k t

def setCells (k : Uni) (v : α) : List (Uni × α) → List (Uni × α)
  | [] => [(k, v)]
  | (k', v') :: t => if k' = k then (k, v) :: t else (k', v') :: setCells k v t

def hasCells (k : Uni) : List (Uni × α) → Bool
  | [] => false
  | (k', _) :: t => if k' = k then true else hasCells k t

/-- the container with no cells. -/
def empty : Dict α := ⟨[]⟩

/-- the value at a key, or `dflt` when the key is not there. -/
def get (d : Dict α) (k : Uni) (dflt : α) : α := getCells dflt k d.cells

/-- the container with `k` carrying `v`. -/
def set (d : Dict α) (k : Uni) (v : α) : Dict α := ⟨setCells k v d.cells⟩

/-- is the key there at all. -/
def has (d : Dict α) (k : Uni) : Bool := hasCells k d.cells

/-- how many cells. NOT how many keys -- they are the same for every
container built by the constructors here, which never repeat a key. -/
def length (d : Dict α) : Nat := d.cells.length

def keys (d : Dict α) : List Uni := d.cells.map Prod.fst
def vals (d : Dict α) : List α := d.cells.map Prod.snd

/-- the same keys, each value carried through `f`: a vector of vectors
is `mapVals ofVector (ofVector v)`, with no second container form. -/
def mapVals (f : α → β) (d : Dict α) : Dict β := ⟨d.cells.map (fun c => (c.1, f c.2))⟩

/-- keys `b`, `b+1`, … over a Lean list. -/
def ofValuesFrom (b : Nat) : List α → Dict α
  | [] => ⟨[]⟩
  | x :: t => ⟨(key b, x) :: (ofValuesFrom (b + 1) t).cells⟩

/-- **a container from a Lean list**: keys `0 … n-1`, in order. -/
def ofValues (xs : List α) : Dict α := ofValuesFrom 0 xs

/-- the decided form of the same: a `List Uni` becomes a `UDict`. -/
def ofList (xs : List Uni) : UDict := ofValues xs

/-- `n` cells, every value the same -- what `vectorInit` builds. -/
def repeatVal (n : Nat) (a : α) : Dict α := ofValues (List.replicate n a)

/-! ## the laws

The four the container has to obey, proved. -/

theorem getCells_setCells_same (l : List (Uni × α)) (k : Uni) (v dflt : α) :
    getCells dflt k (setCells k v l) = v := by
  induction l with
  | nil => simp [setCells, getCells]
  | cons c t ih =>
    obtain ⟨k', v'⟩ := c
    by_cases h : k' = k
    · simp [setCells, getCells, h]
    · simp [setCells, getCells, h, ih]

/-- **get after set at the same key returns what was set.** -/
theorem get_set_same (d : Dict α) (k : Uni) (v dflt : α) :
    (d.set k v).get k dflt = v := getCells_setCells_same d.cells k v dflt

theorem getCells_setCells_other (l : List (Uni × α)) (k k' : Uni) (v dflt : α) (h : k' ≠ k) :
    getCells dflt k' (setCells k v l) = getCells dflt k' l := by
  induction l with
  | nil => simp [setCells, getCells, Ne.symm h]
  | cons c t ih =>
    obtain ⟨k₀, v₀⟩ := c
    by_cases h₀ : k₀ = k
    · subst h₀; simp [setCells, getCells, Ne.symm h]
    · simp [setCells, getCells, h₀, ih]

/-- **get after set at a different key is unchanged.** -/
theorem get_set_other (d : Dict α) (k k' : Uni) (v dflt : α) (h : k' ≠ k) :
    (d.set k v).get k' dflt = d.get k' dflt :=
  getCells_setCells_other d.cells k k' v dflt h

theorem setCells_setCells_same (l : List (Uni × α)) (k : Uni) (v w : α) :
    setCells k w (setCells k v l) = setCells k w l := by
  induction l with
  | nil => simp [setCells]
  | cons c t ih =>
    obtain ⟨k', v'⟩ := c
    by_cases h : k' = k
    · subst h; simp [setCells]
    · simp [setCells, h, ih]

/-- **set after set at the same key keeps only the later one.** -/
theorem set_set_same (d : Dict α) (k : Uni) (v w : α) :
    (d.set k v).set k w = d.set k w := by
  simp [set, setCells_setCells_same]

theorem length_setCells (l : List (Uni × α)) (k : Uni) (v : α) :
    (setCells k v l).length = if hasCells k l then l.length else l.length + 1 := by
  induction l with
  | nil => simp [setCells, hasCells]
  | cons c t ih =>
    obtain ⟨k', v'⟩ := c
    by_cases h : k' = k
    · simp [setCells, hasCells, h]
    · cases hh : hasCells k t <;> simp [setCells, hasCells, h, ih, hh]

/-- **length under set**: a key already there keeps the length, a new
key grows it by one. (Sail's `vectorUpdate` can only be the first case
-- see note 1 in the header.) -/
theorem length_set (d : Dict α) (k : Uni) (v : α) :
    (d.set k v).length = if d.has k then d.length else d.length + 1 :=
  length_setCells d.cells k v

theorem length_set_of_has (d : Dict α) (k : Uni) (v : α) (h : d.has k = true) :
    (d.set k v).length = d.length := by simp [length_set, h]

theorem length_set_of_not_has (d : Dict α) (k : Uni) (v : α) (h : d.has k = false) :
    (d.set k v).length = d.length + 1 := by simp [length_set, h]

/-! ## the edges, and the rest of the small laws -/

theorem get_empty (k : Uni) (dflt : α) : (empty : Dict α).get k dflt = dflt := rfl

theorem length_empty : (empty : Dict α).length = 0 := rfl

theorem has_empty (k : Uni) : (empty : Dict α).has k = false := rfl

theorem hasCells_setCells_same (l : List (Uni × α)) (k : Uni) (v : α) :
    hasCells k (setCells k v l) = true := by
  induction l with
  | nil => simp [setCells, hasCells]
  | cons c t ih =>
    obtain ⟨k', v'⟩ := c
    by_cases h : k' = k
    · simp [setCells, hasCells, h]
    · simp [setCells, hasCells, h, ih]

theorem has_set_same (d : Dict α) (k : Uni) (v : α) : (d.set k v).has k = true :=
  hasCells_setCells_same d.cells k v

theorem length_mapVals (f : α → β) (d : Dict α) : (mapVals f d).length = d.length := by
  simp [mapVals, length]

theorem get_mapVals (f : α → β) (d : Dict α) (k : Uni) (dflt : α) :
    (mapVals f d).get k (f dflt) = f (d.get k dflt) := by
  obtain ⟨l⟩ := d
  simp only [mapVals, get]
  induction l with
  | nil => simp [getCells]
  | cons c t ih =>
    obtain ⟨k', v'⟩ := c
    by_cases h : k' = k
    · simp [getCells, h]
    · simp [getCells, h, ih]

/-! ## a container from a Lean list, and what it reads back -/

theorem length_ofValuesFrom (b : Nat) (xs : List α) :
    (ofValuesFrom b xs).length = xs.length := by
  induction xs generalizing b with
  | nil => simp [ofValuesFrom, length]
  | cons x t ih => simpa [ofValuesFrom, length] using ih (b + 1)

theorem length_ofValues (xs : List α) : (ofValues xs).length = xs.length :=
  length_ofValuesFrom 0 xs

theorem get_ofValuesFrom (b : Nat) (xs : List α) (i : Nat) (dflt : α) :
    (ofValuesFrom b xs).get (key (b + i)) dflt = (xs[i]?).getD dflt := by
  induction xs generalizing b i with
  | nil => simp [ofValuesFrom, get, getCells]
  | cons x t ih =>
    cases i with
    | zero => simp [ofValuesFrom, get, getCells]
    | succ j =>
      have hne : key b ≠ key (b + (j + 1)) := key_ne (by omega)
      have hb : b + (j + 1) = (b + 1) + j := by omega
      simp only [ofValuesFrom, get, getCells, hne, if_false, List.getElem?_cons_succ]
      rw [hb]
      exact ih (b + 1) j

/-- the container from a list answers the list, position by position --
and answers the default off the end, which is the container's honest
reply where Sail's type would simply have refused the index. -/
theorem get_ofValues (xs : List α) (i : Nat) (dflt : α) :
    (ofValues xs).get (key i) dflt = (xs[i]?).getD dflt := by
  have := get_ofValuesFrom 0 xs i dflt
  simpa using this

theorem get_repeatVal (n i : Nat) (a dflt : α) (h : i < n) :
    (repeatVal n a).get (key i) dflt = a := by
  simp [repeatVal, get_ofValues, h]

theorem length_repeatVal (n : Nat) (a : α) : (repeatVal n a).length = n := by
  simp [repeatVal, length_ofValues]

theorem setCells_ofValuesFrom (b : Nat) (xs : List α) (i : Nat) (x : α) (h : i < xs.length) :
    ofValuesFrom b (xs.set i x) = (ofValuesFrom b xs).set (key (b + i)) x := by
  induction xs generalizing b i with
  | nil => simp at h
  | cons y t ih =>
    cases i with
    | zero => simp [ofValuesFrom, set, setCells]
    | succ j =>
      have hb : b + (j + 1) = (b + 1) + j := by omega
      have hne : key b ≠ key ((b + 1) + j) := key_ne (by omega)
      have hj : j < t.length := by simpa using h
      have ihj := ih (b + 1) j hj
      simp only [List.set_cons_succ, ofValuesFrom, set, setCells, hb, hne, if_false]
      rw [ihj]
      simp [set]

/-- writing one position of the list IS `set` at that position's key. -/
theorem ofValues_set (xs : List α) (i : Nat) (x : α) (h : i < xs.length) :
    ofValues (xs.set i x) = (ofValues xs).set (key i) x := by
  have := setCells_ofValuesFrom 0 xs i x h
  simpa using this

end Dict

/-! ## Sail's own container, transcribed

The emit spells its container `Vector (BitVec 32) 4` -- the element type
first, the LENGTH SECOND AND IN THE TYPE, which is Lean core's
`Vector α n`. The three primitives the emit uses on it (log 289 §2.3:
`vectorUpdate` 99 uses, `vectorInit` 15, `Vector.length` 4) and the
read (`GetElem?.getElem!`, 792 uses in the emit, the vector reads among
them) are transcribed here so that this module can be checked against
them without importing the emit, exactly as `Universal.lean`
transcribes `to_bits_truncate`.

The package itself is not on this host (note 4 in the header). Two
things about it are inferred from the emit's uses rather than read:

  - the INDEX TYPE. `write_TLB` passes a `Nat` (`LeanIM/VmemTlb.lean`)
    and `to_bytes_le` passes the counter of a `[lo:hi:1]i` loop, which
    is an `Int` (`LeanIM/Vector.lean`). Both are transcribed, and
    `sailVectorUpdate_natCast` proves they are the same function on a
    non-negative index, so which one the package chose does not change
    a single bridge theorem below.
  - `vectorUpdate` OUT OF BOUNDS. Transcribed as core's `set!`, which
    is `setIfInBounds`: it answers the container unchanged. Every
    bridge theorem carries the in-bounds hypothesis, so a package that
    instead refuses out of bounds agrees with all of them. -/

/-- Sail's `vectorUpdate`, at a `Nat` index. -/
def sailVectorUpdate {α : Type} {n : Nat} (v : Vector α n) (i : Nat) (x : α) : Vector α n :=
  v.set! i x

/-- Sail's `vectorUpdate`, at the `Int` index a Sail loop counter is. -/
def sailVectorUpdateI {α : Type} {n : Nat} (v : Vector α n) (i : Int) (x : α) : Vector α n :=
  v.set! i.toNat x

/-- the two readings of the index are one function on a non-negative
index, so the bridge does not depend on which one the package chose. -/
theorem sailVectorUpdate_natCast {α : Type} {n : Nat} (v : Vector α n) (i : Nat) (x : α) :
    sailVectorUpdateI v (i : Int) x = sailVectorUpdate v i x := by
  simp [sailVectorUpdateI, sailVectorUpdate]

/-- Sail's `vectorInit`: every element the same. `n` is implicit exactly
as in the emit (`vectorInit none`, the length read off the type). -/
def sailVectorInit {α : Type} {n : Nat} (a : α) : Vector α n := Vector.replicate n a

/-- Sail's `Vector.length`: a projection out of the TYPE, not a
measurement of the value. This is the length living in the type, in one
line. -/
def sailVectorLength {α : Type} {n : Nat} (_ : Vector α n) : Nat := n

/-- the emit's read, `GetElem?.getElem! v i`. -/
def sailVectorRead {α : Type} [Inhabited α] {n : Nat} (v : Vector α n) (i : Nat) : α := v[i]!

namespace Dict

variable {α : Type}

/-- Sail's vector as a dict-list: keys `0 … n-1`. -/
def ofVector {n : Nat} (v : Vector α n) : Dict α := ofValues v.toList

/-- a dict-list as a Sail vector. The length CANNOT be recovered from
the dict-list -- it has to be given, and a key that is missing answers
`dflt`. This is note 1 in the header, in one definition. -/
def toVector (n : Nat) (d : Dict α) (dflt : α) : Vector α n :=
  Vector.ofFn (fun i : Fin n => d.get (key i.val) dflt)

/-! ## the bridges, proved -/

/-- `Vector.length` equals `length`: the number in Sail's TYPE is the
number of cells in the value. -/
theorem length_ofVector {n : Nat} (v : Vector α n) : (ofVector v).length = n := by
  simp [ofVector, length_ofValues]

theorem sailVectorLength_eq_length {n : Nat} (v : Vector α n) :
    sailVectorLength v = (ofVector v).length := by
  simp [sailVectorLength, length_ofVector]

/-- reading an element is `get` at that index's key. -/
theorem get_ofVector {n : Nat} (v : Vector α n) (i : Nat) (dflt : α) (h : i < n) :
    (ofVector v).get (key i) dflt = v[i] := by
  have hl : i < v.toList.length := by simpa using h
  simp [ofVector, get_ofValues, List.getElem?_eq_getElem hl]

/-- and so the emit's own read, `GetElem?.getElem!`, is that `get`. -/
theorem get_ofVector_eq_sailVectorRead {n : Nat} [Inhabited α] (v : Vector α n) (i : Nat)
    (dflt : α) (h : i < n) : (ofVector v).get (key i) dflt = sailVectorRead v i := by
  rw [get_ofVector v i dflt h, sailVectorRead, getElem!_pos v i h]

/-- **the round trip**: Sail's vector to a dict-list and back is the
vector. (The other direction is false in general -- header note 1.) -/
theorem toVector_ofVector {n : Nat} (v : Vector α n) (dflt : α) :
    toVector n (ofVector v) dflt = v := by
  apply Vector.ext
  intro i h
  rw [toVector, Vector.getElem_ofFn h]
  exact get_ofVector v i dflt h

/-- what `set!` does to the list under a core `Vector`, which is what
makes the `vectorUpdate` bridge a list induction. -/
theorem toList_set! {n : Nat} (v : Vector α n) (i : Nat) (x : α) :
    (v.set! i x).toList = v.toList.set i x := by
  simp [Vector.toList]

/-- **`vectorUpdate` equals `set`**, in bounds. -/
theorem ofVector_sailVectorUpdate {n : Nat} (v : Vector α n) (i : Nat) (x : α) (h : i < n) :
    ofVector (sailVectorUpdate v i x) = (ofVector v).set (key i) x := by
  have hl : i < v.toList.length := by simpa using h
  simp only [ofVector, sailVectorUpdate, toList_set!]
  exact ofValues_set v.toList i x hl

/-- the same for the `Int`-index reading of `vectorUpdate`. -/
theorem ofVector_sailVectorUpdateI {n : Nat} (v : Vector α n) (i : Nat) (x : α) (h : i < n) :
    ofVector (sailVectorUpdateI v (i : Int) x) = (ofVector v).set (key i) x := by
  rw [sailVectorUpdate_natCast]
  exact ofVector_sailVectorUpdate v i x h

/-- **`vectorInit` equals a dict-list of one repeated value.** -/
theorem ofVector_sailVectorInit {n : Nat} (a : α) :
    ofVector (sailVectorInit (n := n) a) = repeatVal n a := by
  simp [ofVector, sailVectorInit, repeatVal, Vector.toList_replicate]

end Dict

/-! ## the three containers, each an instantiation

Nothing below adds an implementation. Memory, the register file and a
record are the SAME dict-list at different keys and different values --
that is the whole claim of this file, written out so it can be read. -/

/-- **memory**: keys are addresses, values are bytes. -/
abbrev Mem := UDict

/-- one byte written. -/
def store (m : Mem) (addr : Nat) (b : BitVec 8) : Mem := m.set (key addr) (Uni.ofBitsU b)

/-- one byte read; an address never written answers zero, which is the
container's choice and NOT a claim about the model's memory. -/
def load (m : Mem) (addr : Nat) : Uni := m.get (key addr) (Uni.ofInt 0)

/-- **the byte read back is the byte written.** This is the read-back
law ON THE CONTAINER. The bridge to the model's `vmem_read` /
`vmem_write` is NOT stated -- header note 5. -/
theorem load_store_same (m : Mem) (addr : Nat) (b : BitVec 8) :
    load (store m addr b) addr = Uni.ofBitsU b :=
  Dict.get_set_same m (key addr) (Uni.ofBitsU b) (Uni.ofInt 0)

/-- a write at one address leaves every other address alone. -/
theorem load_store_other (m : Mem) (a a' : Nat) (b : BitVec 8) (h : a' ≠ a) :
    load (store m a b) a' = load m a' :=
  Dict.get_set_other m (key a) (key a') (Uni.ofBitsU b) (Uni.ofInt 0) (key_ne h)

/-- **the register file**: the vector case at n = 32, no new code. -/
abbrev Regs := UDict

def regsInit : Regs := Dict.repeatVal 32 (Uni.ofInt 0)

def rX (r : Regs) (i : Nat) : Uni := r.get (key i) (Uni.ofInt 0)
def wX (r : Regs) (i : Nat) (v : Uni) : Regs := r.set (key i) v

theorem rX_wX_same (r : Regs) (i : Nat) (v : Uni) : rX (wX r i v) i = v :=
  Dict.get_set_same r (key i) v (Uni.ofInt 0)

theorem rX_wX_other (r : Regs) (i j : Nat) (v : Uni) (h : j ≠ i) :
    rX (wX r i v) j = rX r j :=
  Dict.get_set_other r (key i) (key j) v (Uni.ofInt 0) (key_ne h)

theorem length_regsInit : regsInit.length = 32 := Dict.length_repeatVal 32 (Uni.ofInt 0)

/-- **a record**: the same container keyed by a field's name. -/
def field (d : UDict) (name : String) : Uni := d.get (keyOfName name) (Uni.ofInt 0)
def setField (d : UDict) (name : String) (v : Uni) : UDict := d.set (keyOfName name) v

theorem field_setField_same (d : UDict) (name : String) (v : Uni) :
    field (setField d name v) name = v :=
  Dict.get_set_same d (keyOfName name) v (Uni.ofInt 0)

/-! ## the checks

Known values, read off the object itself. Nothing below is part of the
definition. The style is `Kinds.lean`'s. -/

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

private def z : Uni := Uni.ofInt 0
private def d1 : UDict := Dict.empty.set (key 0) (Uni.ofInt 7)
private def d2 : UDict := d1.set (key 3) (Uni.ofInt 9)
private def v4 : Vector (BitVec 8) 4 := Vector.ofFn (fun i => BitVec.ofNat 8 (10 + i.val))

#eval report "the four laws at concrete values" [
  chk "get after set at the same key returns what was set"
    ((d1.get (key 0) z).toInt) (7 : Int),
  chk "get after set at a different key is unchanged"
    ((d2.get (key 0) z).toInt) (7 : Int),
  chk "set after set at the same key keeps only the later one"
    (d1.set (key 0) (Uni.ofInt 8)) (Dict.empty.set (key 0) (Uni.ofInt 8)),
  chk "a key already there keeps the length"
    ((d1.set (key 0) (Uni.ofInt 8)).length) 1,
  chk "a new key grows the length by one"
    ((d1.set (key 1) (Uni.ofInt 8)).length) 2
]

#eval report "the edges: empty, and one cell" [
  chk "the empty container answers the default"
    (((Dict.empty : UDict).get (key 0) (Uni.ofInt 5)).toInt) (5 : Int),
  chk "the empty container has length zero and holds no key"
    (((Dict.empty : UDict).length), ((Dict.empty : UDict).has (key 0))) ((0, false) : Nat × Bool),
  chk "one cell: its length, its value, and the default off the end"
    ((Dict.ofList [Uni.ofInt 3]).length,
     ((Dict.ofList [Uni.ofInt 3]).get (key 0) z).toInt,
     ((Dict.ofList [Uni.ofInt 3]).get (key 1) (Uni.ofInt (-1))).toInt)
    ((1, 3, -1) : Nat × Int × Int),
  chk "a container from a Lean list of universal values"
    ((Dict.ofList [Uni.ofInt 4, Uni.ofInt 5, Uni.ofInt 6]).vals.map Uni.toInt)
    ([4, 5, 6] : List Int),
  chk "distinct integers are distinct keys"
    (key 4 == key 5) false,
  chk "one value, two spellings, TWO KEYS (header note 2)"
    (Uni.ofInt 4 == Uni.ofSignedAt 1 2) false
]

#eval report "the bridges to Sail's Vector, at concrete values" [
  chk "the round trip: vector to dict-list and back"
    ((Dict.toVector 4 (Dict.ofVector v4) 0#8).toList) (v4.toList),
  chk "Vector.length equals length"
    ((sailVectorLength v4), ((Dict.ofVector v4).length)) ((4, 4) : Nat × Nat),
  chk "reading an element is get at that index's key"
    ((Dict.ofVector v4).get (key 2) 0#8) (12#8 : BitVec 8),
  chk "vectorUpdate equals set"
    (Dict.ofVector (sailVectorUpdate v4 2 0xff#8))
    ((Dict.ofVector v4).set (key 2) 0xff#8),
  chk "vectorUpdate at an Int index is the same function"
    (Dict.ofVector (sailVectorUpdateI v4 (2 : Int) 0xff#8))
    (Dict.ofVector (sailVectorUpdate v4 2 0xff#8)),
  chk "vectorInit equals a dict-list of one repeated value"
    (Dict.ofVector (sailVectorInit (n := 3) (0#8))) (Dict.repeatVal 3 (0#8)),
  chk "a vector of vectors needs no second form (header note 3)"
    ((Dict.mapVals (fun w => Dict.ofVector w)
        (Dict.ofVector (sailVectorInit (n := 2) (sailVectorInit (n := 3) (0#8)))))
       |>.get (key 1) Dict.empty |>.length)
    3
]

#eval report "the three containers, one form" [
  chk "memory: the byte read back is the byte written"
    ((load (store (Dict.empty : Mem) 0x1000 0xab#8) 0x1000).toInt) (171 : Int),
  chk "memory: another address is untouched"
    ((load (store (Dict.empty : Mem) 0x1000 0xab#8) 0x1004).toInt) (0 : Int),
  chk "the register file: 32 cells, one written and read back"
    ((rX (wX regsInit 5 (Uni.ofInt 42)) 5).toInt, regsInit.length, (rX regsInit 5).toInt)
    ((42, 32, 0) : Int × Nat × Int),
  chk "a record keyed by a field's name"
    ((field (setField (Dict.empty : UDict) "asid" (Uni.ofInt 9)) "asid").toInt) (9 : Int),
  chk "two field names are two keys"
    (keyOfName "asid" == keyOfName "vpn") false,
  chk "a text keyed by position"
    ((Dict.ofList (("hi".toList).map (fun c => Uni.ofInt c.toNat))).vals.map Uni.toInt)
    ([104, 105] : List Int)
]

/-! ## the audit

What every theorem in this file rests on. Lean's three standard axioms
(`propext`, `Classical.choice`, `Quot.sound`) are the whole list, and
`sorryAx` is in none of them -- which is the machine-checked form of the
claim that nothing here is left looking proved. Anything this file does
NOT prove is in the header, in words, and is not below. -/

#print axioms Dict.get_set_same
#print axioms Dict.get_set_other
#print axioms Dict.set_set_same
#print axioms Dict.length_set
#print axioms Dict.get_ofValues
#print axioms Dict.length_ofValues
#print axioms Dict.length_ofVector
#print axioms Dict.get_ofVector
#print axioms Dict.get_ofVector_eq_sailVectorRead
#print axioms Dict.toVector_ofVector
#print axioms Dict.ofVector_sailVectorUpdate
#print axioms Dict.ofVector_sailVectorUpdateI
#print axioms Dict.ofVector_sailVectorInit
#print axioms Dict.sailVectorLength_eq_length
#print axioms key_inj
#print axioms load_store_same
#print axioms load_store_other
#print axioms rX_wX_same
#print axioms field_setField_same

end Containers
