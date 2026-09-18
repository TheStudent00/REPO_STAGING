import Std.Tactic.BVDecide
-- one #check per line: an unknown one errors on its own line and the rest still run
#check @BitVec.zero
#check @BitVec.zero_eq
#check @BitVec.ofNat_eq_ofNat
#check @BitVec.sshiftRight
#check @BitVec.sshiftRight'
#check @BitVec.sshiftRight_eq
#check @BitVec.lt_def
#check @BitVec.ult
#check @BitVec.ult_iff_lt
#check @Int.ofNat_lt
#check @Int.toNat_natCast
