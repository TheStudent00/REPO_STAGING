| key: a subterm of Sail's definitions | c | cpp | rust | go |
|---|---|---|---|---|
| `(a &&& b)` | 18 (4 at 64) | 35 (8 at 64) | 5 (2 at 64) |  |
| `(a ^^^ b)` | 17 (4 at 64) | 34 (8 at 64) | 5 (2 at 64) |  |
| `(a \|\|\| b)` | 17 (4 at 64) | 34 (8 at 64) | 5 (2 at 64) |  |
| `(a + b)` | 13 (4 at 64) | 13 (4 at 64) | 2 (2 at 64) |  |
| `(a - b)` | 13 (4 at 64) | 13 (4 at 64) | 2 (2 at 64) |  |
| `(shift_bits_left a (Sail.BitVec.extractLsb b (log2_xlen -i 1) 0))` | 8 (4 at 64) | 8 (4 at 64) | 6 (4 at 64) |  |
| `(mult_to_bits_half (l := xlen) Signedness.Signed Signedness.Signed a b VectorHalf.Low)` | 8 (4 at 64) | 8 (4 at 64) | 2 (2 at 64) | 2 (2 at 64) |
| `(sign_extend (m := 64) (shift_bits_left (Sail.BitVec.extractLsb a 31 0) (Sail.BitVec.extractLsb (Sail.BitVec.extractLsb b 31 0) 4 0)))` | 8 (0 at 64) | 8 (0 at 64) | 3 (0 at 64) |  |
| `(zero_extend (m := 64) (bool_to_bit (zopz0zI_s a b)))` | 8 (1 at 64) | 8 (1 at 64) | 2 (1 at 64) | 1 (1 at 64) |
| `(zero_extend (m := 64) (bool_to_bit (zopz0zI_u a b)))` | 6 (3 at 64) | 6 (3 at 64) | 1 (1 at 64) | 1 (1 at 64) |
| `(to_bits_truncate (l := 64) (if (((BitVec.toNatInt b) == 0) : Bool) then (BitVec.toNatInt a) else (Int.tmod (BitVec.toNatInt a) (BitVec.toNatInt b))))` | 6 (3 at 64) | 6 (3 at 64) |  |  |
| `(to_bits_truncate (l := 64) (if (((BitVec.toNatInt b) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toNatInt a) (BitVec.toNatInt b))))` | 6 (3 at 64) | 6 (3 at 64) |  |  |
| `(shift_bits_right a (Sail.BitVec.extractLsb b (log2_xlen -i 1) 0))` | 4 (2 at 64) | 4 (2 at 64) | 3 (2 at 64) |  |
| `(shift_bits_right_arith a (Sail.BitVec.extractLsb b (log2_xlen -i 1) 0))` | 4 (2 at 64) | 4 (2 at 64) | 3 (2 at 64) |  |
| `(sign_extend (m := 64) (shift_bits_right_arith (Sail.BitVec.extractLsb a 31 0) (Sail.BitVec.extractLsb (Sail.BitVec.extractLsb b 31 0) 4 0)))` | 4 (0 at 64) | 4 (0 at 64) | 3 (0 at 64) |  |
| `(sign_extend (m := 64) (shift_bits_right (Sail.BitVec.extractLsb a 31 0) (Sail.BitVec.extractLsb (Sail.BitVec.extractLsb b 31 0) 4 0)))` | 4 (0 at 64) | 4 (0 at 64) |  |  |
| `(to_bits_truncate (l := 64) (if (((BitVec.toInt b) == 0) : Bool) then (BitVec.toInt a) else (Int.tmod (BitVec.toInt a) (BitVec.toInt b))))` | 4 (1 at 64) | 4 (1 at 64) |  |  |
| `(to_bits_truncate (l := 64) (if (((if (((BitVec.toInt b) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt a) (BitVec.toInt b))) ≥b (2 ^i (xlen -i 1))) : Bool) then (Neg.neg (2 ^i (xlen -i 1))) else (if (((BitVec.toInt b) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt a) (BitVec.toInt b)))))` | 4 (1 at 64) | 4 (1 at 64) |  |  |
| `(sign_extend (m := 64) ((Sail.BitVec.extractLsb a 31 0) + (Sail.BitVec.extractLsb b 31 0)))` | 3 (0 at 64) | 3 (0 at 64) | 1 (0 at 64) |  |
| `(sign_extend (m := 64) ((Sail.BitVec.extractLsb a 31 0) - (Sail.BitVec.extractLsb b 31 0)))` | 3 (0 at 64) | 3 (0 at 64) | 1 (0 at 64) |  |
| `(Complement.complement a)` |  |  | 3 (2 at 64) | 3 (2 at 64) |
| `(sign_extend (m := 64) (to_bits_truncate (l := 32) ((BitVec.toInt (Sail.BitVec.extractLsb a 31 0)) *i (BitVec.toInt (Sail.BitVec.extractLsb b 31 0)))))` | 1 (0 at 64) | 1 (0 at 64) | 1 (0 at 64) | 1 (0 at 64) |
| `(sign_extend (m := 64) (to_bits_truncate (l := 32) (if (((BitVec.toInt (Sail.BitVec.extractLsb b 31 0)) == 0) : Bool) then (BitVec.toInt (Sail.BitVec.extractLsb a 31 0)) else (Int.tmod (BitVec.toInt (Sail.BitVec.extractLsb a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb b 31 0))))))` | 2 (0 at 64) | 2 (0 at 64) |  |  |
| `(sign_extend (m := 64) (to_bits_truncate (l := 32) (if (((if (((BitVec.toInt (Sail.BitVec.extractLsb b 31 0)) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt (Sail.BitVec.extractLsb a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb b 31 0)))) ≥b (2 ^i 31)) : Bool) then (Neg.neg (2 ^i 31)) else (if (((BitVec.toInt (Sail.BitVec.extractLsb b 31 0)) == 0) : Bool) then (Neg.neg 1) else (Int.tdiv (BitVec.toInt (Sail.BitVec.extractLsb a 31 0)) (BitVec.toInt (Sail.BitVec.extractLsb b 31 0)))))))` | 2 (0 at 64) | 2 (0 at 64) |  |  |
