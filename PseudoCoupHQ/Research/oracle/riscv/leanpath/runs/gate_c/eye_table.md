# the eye table: D beside E beside U beside L

Rendered: 2. Refused at render: 73. Lowered and read back: 2.

| definition | D: Sail's text over the reads | E: the composition | E: built from (subterm -> corpus unit) | U: instructions | L: the meaning read back | walk | proof |
|---|---|---|---|---|---|---|---|
| ZIMOP_MOP_RR one | (zeros (n := 64)) | REFUSED: no key of operator_for matches: (zeros (n := 64)) | | | | | |
| ZIMOP_MOP_R one | (zeros (n := 64)) | REFUSED: no key of operator_for matches: (zeros (n := 64)) | | | | | |
| ZBS_RTYPE BCLR | (rs1_val &&& (Complement.complement (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb rs2_val 5 0)))) | REFUSED: no key of operator_for matches: (rs1_val &&& (Complement.complement (shift_bits_left (zero_extend (m | | | | | |
| ZBS_RTYPE BEXT | (zero_extend (m := 64) (bool_to_bit ((rs1_val &&& (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb rs2_val 5 0))) != (ze | REFUSED: no key of operator_for matches: (zero_extend (m := 64) (bool_to_bit ((rs1_val &&& (shift_bits_left ( | | | | | |
| ZBS_RTYPE BINV | (rs1_val ^^^ (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb rs2_val 5 0))) | REFUSED: no key of operator_for matches: (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb | | | | | |
| ZBS_RTYPE BSET | (rs1_val \|\|\| (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.BitVec.extractLsb rs2_val 5 0))) | REFUSED: no key of operator_for matches: (rs1_val \|\|\| (shift_bits_left (zero_extend (m := 64) 1#1) (Sail.B | | | | | |
| ZBS_IOP BCLRI | (rs1_val &&& (Complement.complement (shift_bits_left (zero_extend (m := 64) 1#1) shamt))) | REFUSED: no key of operator_for matches: (rs1_val &&& (Complement.complement (shift_bits_left (zero_extend (m | | | | | |
| ZBS_IOP BEXTI | (zero_extend (m := 64) (bool_to_bit ((rs1_val &&& (shift_bits_left (zero_extend (m := 64) 1#1) shamt)) != (zeros (n := 64))))) | REFUSED: no key of operator_for matches: (zero_extend (m := 64) (bool_to_bit ((rs1_val &&& (shift_bits_left ( | | | | | |
| ZBS_IOP BINVI | (rs1_val ^^^ (shift_bits_left (zero_extend (m := 64) 1#1) shamt)) | REFUSED: no key of operator_for matches: (shift_bits_left (zero_extend (m := 64) 1#1) shamt) | | | | | |
| ZBS_IOP BSETI | (rs1_val \|\|\| (shift_bits_left (zero_extend (m := 64) 1#1) shamt)) | REFUSED: no key of operator_for matches: (rs1_val \|\|\| (shift_bits_left (zero_extend (m := 64) 1#1) shamt)) | | | | | |
| ZBKB_RTYPE PACK | ((Sail.BitVec.extractLsb rs2_val ((xlen_bytes *i 4) -i 1) 0) +++ (Sail.BitVec.extractLsb rs1_val ((xlen_bytes *i 4) -i 1) 0)) | REFUSED: no key of operator_for matches: ((Sail.BitVec.extractLsb rs2_val ((xlen_bytes *i 4) -i 1) 0) +++ (Sa | | | | | |
| ZBKB_RTYPE PACKH | (zero_extend (m := 64) ((Sail.BitVec.extractLsb rs2_val 7 0) +++ (Sail.BitVec.extractLsb rs1_val 7 0))) | REFUSED: no key of operator_for matches: (zero_extend (m := 64) ((Sail.BitVec.extractLsb rs2_val 7 0) +++ (Sa | | | | | |
| ZBB_RTYPEW one | (sign_extend (m := 64) (match op with \| .ROLW => (rotate_bits_left (Sail.BitVec.extractLsb v_rs1 31 0) (Sail.BitVec.extractLsb v_rs2 4 0))  | REFUSED: no key of operator_for matches: (sign_extend (m := 64) (match op with \| .ROLW => (rotate_bits_left  | | | | | |
| ZBB_RTYPE ANDN | (rs1_val &&& (Complement.complement rs2_val)) | REFUSED: no key of operator_for matches: (rs1_val &&& (Complement.complement rs2_val)) | | | | | |
| ZBB_RTYPE ORN | (rs1_val \|\|\| (Complement.complement rs2_val)) | REFUSED: no key of operator_for matches: (rs1_val \|\|\| (Complement.complement rs2_val)) | | | | | |
| ZBB_RTYPE XNOR | (Complement.complement (rs1_val ^^^ rs2_val)) | REFUSED: no key of operator_for matches: (Complement.complement (rs1_val ^^^ rs2_val)) | | | | | |
| ZBB_RTYPE MAX | (if ((zopz0zK_s rs1_val rs2_val) : Bool) then rs1_val else rs2_val) | REFUSED: no key of operator_for matches: (if ((zopz0zK_s rs1_val rs2_val) : Bool) then rs1_val else rs2_val) | | | | | |
| ZBB_RTYPE MAXU | (if ((zopz0zK_u rs1_val rs2_val) : Bool) then rs1_val else rs2_val) | REFUSED: no key of operator_for matches: (if ((zopz0zK_u rs1_val rs2_val) : Bool) then rs1_val else rs2_val) | | | | | |
| ZBB_RTYPE MIN | (if ((zopz0zI_s rs1_val rs2_val) : Bool) then rs1_val else rs2_val) | REFUSED: no key of operator_for matches: (if ((zopz0zI_s rs1_val rs2_val) : Bool) then rs1_val else rs2_val) | | | | | |
| ZBB_RTYPE MINU | (if ((zopz0zI_u rs1_val rs2_val) : Bool) then rs1_val else rs2_val) | REFUSED: no key of operator_for matches: (if ((zopz0zI_u rs1_val rs2_val) : Bool) then rs1_val else rs2_val) | | | | | |
| ZBB_RTYPE ROL | (rotate_bits_left rs1_val (Sail.BitVec.extractLsb rs2_val (log2_xlen -i 1) 0)) | REFUSED: no key of operator_for matches: (rotate_bits_left rs1_val (Sail.BitVec.extractLsb rs2_val (log2_xlen | | | | | |
| ZBB_RTYPE ROR | (rotate_bits_right rs1_val (Sail.BitVec.extractLsb rs2_val (log2_xlen -i 1) 0)) | REFUSED: no key of operator_for matches: (rotate_bits_right rs1_val (Sail.BitVec.extractLsb rs2_val (log2_xle | | | | | |
| ZBB_EXTOP SEXTB | (sign_extend (m := 64) (Sail.BitVec.extractLsb rs1_val 7 0)) | REFUSED: no key of operator_for matches: (sign_extend (m := 64) (Sail.BitVec.extractLsb rs1_val 7 0)) | | | | | |
| ZBB_EXTOP SEXTH | (sign_extend (m := 64) (Sail.BitVec.extractLsb rs1_val 15 0)) | REFUSED: no key of operator_for matches: (sign_extend (m := 64) (Sail.BitVec.extractLsb rs1_val 15 0)) | | | | | |
| ZBB_EXTOP ZEXTH | (zero_extend (m := 64) (Sail.BitVec.extractLsb rs1_val 15 0)) | REFUSED: no key of operator_for matches: (zero_extend (m := 64) (Sail.BitVec.extractLsb rs1_val 15 0)) | | | | | |
| ZBA_RTYPEUW one | ((shift_bits_left (zero_extend (m := 64) (Sail.BitVec.extractLsb v_rs1 31 0)) shamt) + v_rs2) | REFUSED: no key of operator_for matches: ((shift_bits_left (zero_extend (m := 64) (Sail.BitVec.extractLsb v_r | | | | | |
| ZBA_RTYPE one | ((shift_bits_left v_rs1 shamt) + v_rs2) | REFUSED: no key of operator_for matches: ((shift_bits_left v_rs1 shamt) + v_rs2) | | | | | |
| SLLIUW one | (shift_bits_left (zero_extend (m := 64) (Sail.BitVec.extractLsb v_rs1 31 0)) shamt) | REFUSED: no key of operator_for matches: (shift_bits_left (zero_extend (m := 64) (Sail.BitVec.extractLsb v_rs | | | | | |
| SHIFTIWOP one | (sign_extend (m := 64) (match op with \| .SLLIW => (shift_bits_left (Sail.BitVec.extractLsb v_rs1 31 0) shamt) \| .SRLIW => (shift_bits_righ | REFUSED: no key of operator_for matches: (sign_extend (m := 64) (match op with \| .SLLIW => (shift_bits_left  | | | | | |
| SHIFTIOP SLLI | (shift_bits_left v_rs1 (Sail.BitVec.extractLsb shamt (log2_xlen -i 1) 0)) | REFUSED: no key of operator_for matches: (shift_bits_left v_rs1 (Sail.BitVec.extractLsb shamt (log2_xlen -i 1 | | | | | |
| SHIFTIOP SRLI | (shift_bits_right v_rs1 (Sail.BitVec.extractLsb shamt (log2_xlen -i 1) 0)) | REFUSED: no key of operator_for matches: (shift_bits_right v_rs1 (Sail.BitVec.extractLsb shamt (log2_xlen -i  | | | | | |
| SHIFTIOP SRAI | (shift_bits_right_arith v_rs1 (Sail.BitVec.extractLsb shamt (log2_xlen -i 1) 0)) | REFUSED: no key of operator_for matches: (shift_bits_right_arith v_rs1 (Sail.BitVec.extractLsb shamt (log2_xl | | | | | |
| SHA512SUM1R one | (sign_extend (m := 64) ((v_rs1 <<< 23) ^^^ ((v_rs1_2 >>> 14) ^^^ ((v_rs1_3 >>> 18) ^^^ ((v_rs2 >>> 9) ^^^ ((v_rs2_2 <<< 18) ^^^ (v_rs2_3 <<< | REFUSED: no key of operator_for matches: (sign_extend (m := 64) ((v_rs1 <<< 23) ^^^ ((v_rs1_2 >>> 14) ^^^ ((v | | | | | |
| SHA512SUM0R one | (sign_extend (m := 64) ((v_rs1 <<< 25) ^^^ ((v_rs1_2 <<< 30) ^^^ ((v_rs1_3 >>> 28) ^^^ ((v_rs2 >>> 7) ^^^ ((v_rs2_2 >>> 2) ^^^ (v_rs2_3 <<<  | REFUSED: no key of operator_for matches: (sign_extend (m := 64) ((v_rs1 <<< 25) ^^^ ((v_rs1_2 <<< 30) ^^^ ((v | | | | | |
| SHA512SIG1L one | (sign_extend (m := 64) ((v_rs1 <<< 3) ^^^ ((v_rs1_2 >>> 6) ^^^ ((v_rs1_3 >>> 19) ^^^ ((v_rs2 >>> 29) ^^^ ((v_rs2_2 <<< 26) ^^^ (v_rs2_3 <<<  | REFUSED: no key of operator_for matches: (sign_extend (m := 64) ((v_rs1 <<< 3) ^^^ ((v_rs1_2 >>> 6) ^^^ ((v_r | | | | | |
| SHA512SIG1H one | (sign_extend (m := 64) ((v_rs1 <<< 3) ^^^ ((v_rs1_2 >>> 6) ^^^ ((v_rs1_3 >>> 19) ^^^ ((v_rs2 >>> 29) ^^^ (v_rs2_2 <<< 13)))))) | REFUSED: no key of operator_for matches: (sign_extend (m := 64) ((v_rs1 <<< 3) ^^^ ((v_rs1_2 >>> 6) ^^^ ((v_r | | | | | |
| SHA512SIG0L one | (sign_extend (m := 64) ((v_rs1 >>> 1) ^^^ ((v_rs1_2 >>> 7) ^^^ ((v_rs1_3 >>> 8) ^^^ ((v_rs2 <<< 31) ^^^ ((v_rs2_2 <<< 25) ^^^ (v_rs2_3 <<< 2 | REFUSED: no key of operator_for matches: (sign_extend (m := 64) ((v_rs1 >>> 1) ^^^ ((v_rs1_2 >>> 7) ^^^ ((v_r | | | | | |
| SHA512SIG0H one | (sign_extend (m := 64) ((v_rs1 >>> 1) ^^^ ((v_rs1_2 >>> 7) ^^^ ((v_rs1_3 >>> 8) ^^^ ((v_rs2 <<< 31) ^^^ (v_rs2_2 <<< 24)))))) | REFUSED: no key of operator_for matches: (sign_extend (m := 64) ((v_rs1 >>> 1) ^^^ ((v_rs1_2 >>> 7) ^^^ ((v_r | | | | | |
| RTYPEW one | (sign_extend (m := 64) (match op with \| .ADDW => ((Sail.BitVec.extractLsb v_rs1 31 0) + (Sail.BitVec.extractLsb v_rs2 31 0)) \| .SUBW => (( | REFUSED: no key of operator_for matches: (sign_extend (m := 64) (match op with \| .ADDW => ((Sail.BitVec.extr | | | | | |
| RTYPE ADD | (v_rs1 + v_rs2) | REFUSED: no key of operator_for matches: (v_rs1 + v_rs2) | | | | | |
| RTYPE SLT | (zero_extend (m := 64) (bool_to_bit (zopz0zI_s v_rs1 v_rs2))) | REFUSED: no key of operator_for matches: (zero_extend (m := 64) (bool_to_bit (zopz0zI_s v_rs1 v_rs2))) | | | | | |
| RTYPE SLTU | (zero_extend (m := 64) (bool_to_bit (zopz0zI_u v_rs1 v_rs2))) | op_656(a, b) | (zero_extend (m := 64) (bool_to_bit (zop -> c__op_656 | sltu a0, a0, a1; c.jr ra | (pure_RTYPE (a) (b) (LeanIM.rop.SLTU)) | CERTIFIED | PROVED equal to RTYPE rop.SLTU (same_text) |
| RTYPE AND | (v_rs1 &&& v_rs2) | REFUSED: no key of operator_for matches: (v_rs1 &&& v_rs2) | | | | | |
| RTYPE OR | (v_rs1 \|\|\| v_rs2) | REFUSED: no key of operator_for matches: (v_rs1 \|\|\| v_rs2) | | | | | |
| RTYPE XOR | (v_rs1 ^^^ v_rs2) | op_404(a, b) | (a ^^^ b) -> c__op_404 | c.xor a0, a1; c.jr ra | (pure_RTYPE (a) (b) (XOR)) | CERTIFIED | PROVED equal to RTYPE rop.XOR (same_text) |
| RTYPE SLL | (shift_bits_left v_rs1 (Sail.BitVec.extractLsb v_rs2 (log2_xlen -i 1) 0)) | REFUSED: no key of operator_for matches: (shift_bits_left v_rs1 (Sail.BitVec.extractLsb v_rs2 (log2_xlen -i 1 | | | | | |
| RTYPE SRL | (shift_bits_right v_rs1 (Sail.BitVec.extractLsb v_rs2 (log2_xlen -i 1) 0)) | REFUSED: no key of operator_for matches: (shift_bits_right v_rs1 (Sail.BitVec.extractLsb v_rs2 (log2_xlen -i  | | | | | |
| RTYPE SUB | (v_rs1 - v_rs2) | REFUSED: (a - b) is held only at (64, 32), not at 64 | | | | | |
| RTYPE SRA | (shift_bits_right_arith v_rs1 (Sail.BitVec.extractLsb v_rs2 (log2_xlen -i 1) 0)) | REFUSED: no key of operator_for matches: (shift_bits_right_arith v_rs1 (Sail.BitVec.extractLsb v_rs2 (log2_xl | | | | | |
| RORIW one | (sign_extend (m := 64) (rotate_bits_right (Sail.BitVec.extractLsb v_rs1 31 0) shamt)) | REFUSED: no key of operator_for matches: (sign_extend (m := 64) (rotate_bits_right (Sail.BitVec.extractLsb v_ | | | | | |
| RORI one | (rotate_bits_right v_rs1 (Sail.BitVec.extractLsb shamt (log2_xlen -i 1) 0)) | REFUSED: no key of operator_for matches: (rotate_bits_right v_rs1 (Sail.BitVec.extractLsb shamt (log2_xlen -i | | | | | |
| REV8 one | (rev8 v_rs1) | REFUSED: no key of operator_for matches: (rev8 v_rs1) | | | | | |
| REMW one | (sign_extend (m := 64) (to_bits_truncate (l := 32) (if (((if (is_unsigned : Bool) then (BitVec.toNatInt (Sail.BitVec.extractLsb v_rs2 31 0)) | REFUSED: no key of operator_for matches: (sign_extend (m := 64) (to_bits_truncate (l := 32) (if (((if (is_uns | | | | | |
| REM one | (to_bits_truncate (l := 64) (if (((if (is_unsigned : Bool) then (BitVec.toNatInt rs2_bits) else (BitVec.toInt rs2_bits)) == 0) : Bool) then  | REFUSED: no key of operator_for matches: (to_bits_truncate (l := 64) (if (((if (is_unsigned : Bool) then (Bit | | | | | |
| MULW one | (sign_extend (m := 64) (to_bits_truncate (l := 32) ((BitVec.toInt (Sail.BitVec.extractLsb v_rs1 31 0)) *i (BitVec.toInt (Sail.BitVec.extract | REFUSED: no key of operator_for matches: (sign_extend (m := 64) (to_bits_truncate (l := 32) ((BitVec.toInt (S | | | | | |
| MUL one | (mult_to_bits_half (l := xlen) mul_op.signed_rs1 mul_op.signed_rs2 rs1_bits rs2_bits mul_op.result_part) | REFUSED: no key of operator_for matches: (mult_to_bits_half (l := xlen) mul_op.signed_rs1 mul_op.signed_rs2 r | | | | | |
| ITYPE ADDI | (v_rs1 + (sign_extend (m := 64) imm)) | REFUSED: no key of operator_for matches: (v_rs1 + (sign_extend (m := 64) imm)) | | | | | |
| ITYPE SLTI | (zero_extend (m := 64) (bool_to_bit (zopz0zI_s v_rs1 (sign_extend (m := 64) imm)))) | REFUSED: no key of operator_for matches: (zero_extend (m := 64) (bool_to_bit (zopz0zI_s v_rs1 (sign_extend (m | | | | | |
| ITYPE SLTIU | (zero_extend (m := 64) (bool_to_bit (zopz0zI_u v_rs1 (sign_extend (m := 64) imm)))) | REFUSED: no key of operator_for matches: (sign_extend (m := 64) imm) | | | | | |
| ITYPE ANDI | (v_rs1 &&& (sign_extend (m := 64) imm)) | REFUSED: no key of operator_for matches: (v_rs1 &&& (sign_extend (m := 64) imm)) | | | | | |
| ITYPE ORI | (v_rs1 \|\|\| (sign_extend (m := 64) imm)) | REFUSED: no key of operator_for matches: (v_rs1 \|\|\| (sign_extend (m := 64) imm)) | | | | | |
| ITYPE XORI | (v_rs1 ^^^ (sign_extend (m := 64) imm)) | REFUSED: no key of operator_for matches: (sign_extend (m := 64) imm) | | | | | |
| DIVW one | (sign_extend (m := 64) (to_bits_truncate (l := 32) (if (((not is_unsigned) && ((if (((if (is_unsigned : Bool) then (BitVec.toNatInt (Sail.Bi | REFUSED: no key of operator_for matches: (sign_extend (m := 64) (to_bits_truncate (l := 32) (if (((not is_uns | | | | | |
| DIV one | (to_bits_truncate (l := 64) (if (((not is_unsigned) && ((if (((if (is_unsigned : Bool) then (BitVec.toNatInt rs2_bits) else (BitVec.toInt rs | REFUSED: no key of operator_for matches: (to_bits_truncate (l := 64) (if (((not is_unsigned) && ((if (((if (i | | | | | |
| C_ZEXT_B one | (zero_extend (m := 64) (Sail.BitVec.extractLsb v_rsd 7 0)) | REFUSED: no key of operator_for matches: (zero_extend (m := 64) (Sail.BitVec.extractLsb v_rsd 7 0)) | | | | | |
| C_NOT one | (Complement.complement v_r) | REFUSED: no key of operator_for matches: (Complement.complement v_r) | | | | | |
| CTZW one | (to_bits (l := 64) (BitVec.countTrailingZeros (Sail.BitVec.extractLsb v_rs1 31 0))) | REFUSED: no key of operator_for matches: (to_bits (l := 64) (BitVec.countTrailingZeros (Sail.BitVec.extractLs | | | | | |
| CTZ one | (to_bits (l := 64) (BitVec.countTrailingZeros v_rs1)) | REFUSED: no key of operator_for matches: (to_bits (l := 64) (BitVec.countTrailingZeros v_rs1)) | | | | | |
| CLZW one | (to_bits (l := 64) (BitVec.countLeadingZeros (Sail.BitVec.extractLsb v_rs1 31 0))) | REFUSED: no key of operator_for matches: (to_bits (l := 64) (BitVec.countLeadingZeros (Sail.BitVec.extractLsb | | | | | |
| CLZ one | (to_bits (l := 64) (BitVec.countLeadingZeros v_rs1)) | REFUSED: no key of operator_for matches: (to_bits (l := 64) (BitVec.countLeadingZeros v_rs1)) | | | | | |
| CLMULR one | (carryless_mulr v_rs1 v_rs2) | REFUSED: no key of operator_for matches: (carryless_mulr v_rs1 v_rs2) | | | | | |
| CLMULH one | (Sail.BitVec.extractLsb (carryless_mul v_rs1 v_rs2) ((2 *i xlen) -i 1) xlen) | REFUSED: no key of operator_for matches: (Sail.BitVec.extractLsb (carryless_mul v_rs1 v_rs2) ((2 *i xlen) -i  | | | | | |
| CLMUL one | (Sail.BitVec.extractLsb (carryless_mul v_rs1 v_rs2) (xlen -i 1) 0) | REFUSED: no key of operator_for matches: (Sail.BitVec.extractLsb (carryless_mul v_rs1 v_rs2) (xlen -i 1) 0) | | | | | |
| BREV8 one | (brev8 v_rs1) | REFUSED: no key of operator_for matches: (brev8 v_rs1) | | | | | |
| ADDIW one | (sign_extend (m := 64) (Sail.BitVec.extractLsb (v_rs1 + (sign_extend (m := 64) imm)) 31 0)) | REFUSED: no key of operator_for matches: (sign_extend (m := 64) (Sail.BitVec.extractLsb (v_rs1 + (sign_extend | | | | | |
