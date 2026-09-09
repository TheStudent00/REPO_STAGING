-- The smallest possible check that this toolchain proves anything:
-- one arithmetic identity over 32-bit words, discharged by bv_decide,
-- which bit-blasts the goal to a SAT solver and checks the solver's
-- certificate inside Lean's kernel.
import Std.Tactic.BVDecide

theorem smoke_add_comm (v0 v1 : BitVec 32) : v0 + v1 = v1 + v0 := by
  bv_decide
