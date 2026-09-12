// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sw_gpr_gpr_imm_32__mem_MEM_a1__go__bit_blast.
//   Concat(Extract(63, 32, v0), Extract(31, 0, v1))
package main

//go:noinline
func emu_sw_gpr_gpr_imm_32__mem_MEM_a1__go__bit_blast(a uint64, b uint32) uint64 {
	var x1_0 uint64 = (uint64(b) >> 0) & 1
	var x1_1 uint64 = (uint64(b) >> 1) & 1
	var x1_2 uint64 = (uint64(b) >> 2) & 1
	var x1_3 uint64 = (uint64(b) >> 3) & 1
	var x1_4 uint64 = (uint64(b) >> 4) & 1
	var x1_5 uint64 = (uint64(b) >> 5) & 1
	var x1_6 uint64 = (uint64(b) >> 6) & 1
	var x1_7 uint64 = (uint64(b) >> 7) & 1
	var x1_8 uint64 = (uint64(b) >> 8) & 1
	var x1_9 uint64 = (uint64(b) >> 9) & 1
	var x1_10 uint64 = (uint64(b) >> 10) & 1
	var x1_11 uint64 = (uint64(b) >> 11) & 1
	var x1_12 uint64 = (uint64(b) >> 12) & 1
	var x1_13 uint64 = (uint64(b) >> 13) & 1
	var x1_14 uint64 = (uint64(b) >> 14) & 1
	var x1_15 uint64 = (uint64(b) >> 15) & 1
	var x1_16 uint64 = (uint64(b) >> 16) & 1
	var x1_17 uint64 = (uint64(b) >> 17) & 1
	var x1_18 uint64 = (uint64(b) >> 18) & 1
	var x1_19 uint64 = (uint64(b) >> 19) & 1
	var x1_20 uint64 = (uint64(b) >> 20) & 1
	var x1_21 uint64 = (uint64(b) >> 21) & 1
	var x1_22 uint64 = (uint64(b) >> 22) & 1
	var x1_23 uint64 = (uint64(b) >> 23) & 1
	var x1_24 uint64 = (uint64(b) >> 24) & 1
	var x1_25 uint64 = (uint64(b) >> 25) & 1
	var x1_26 uint64 = (uint64(b) >> 26) & 1
	var x1_27 uint64 = (uint64(b) >> 27) & 1
	var x1_28 uint64 = (uint64(b) >> 28) & 1
	var x1_29 uint64 = (uint64(b) >> 29) & 1
	var x1_30 uint64 = (uint64(b) >> 30) & 1
	var x1_31 uint64 = (uint64(b) >> 31) & 1
	var x0_32 uint64 = (uint64(a) >> 32) & 1
	var x0_33 uint64 = (uint64(a) >> 33) & 1
	var x0_34 uint64 = (uint64(a) >> 34) & 1
	var x0_35 uint64 = (uint64(a) >> 35) & 1
	var x0_36 uint64 = (uint64(a) >> 36) & 1
	var x0_37 uint64 = (uint64(a) >> 37) & 1
	var x0_38 uint64 = (uint64(a) >> 38) & 1
	var x0_39 uint64 = (uint64(a) >> 39) & 1
	var x0_40 uint64 = (uint64(a) >> 40) & 1
	var x0_41 uint64 = (uint64(a) >> 41) & 1
	var x0_42 uint64 = (uint64(a) >> 42) & 1
	var x0_43 uint64 = (uint64(a) >> 43) & 1
	var x0_44 uint64 = (uint64(a) >> 44) & 1
	var x0_45 uint64 = (uint64(a) >> 45) & 1
	var x0_46 uint64 = (uint64(a) >> 46) & 1
	var x0_47 uint64 = (uint64(a) >> 47) & 1
	var x0_48 uint64 = (uint64(a) >> 48) & 1
	var x0_49 uint64 = (uint64(a) >> 49) & 1
	var x0_50 uint64 = (uint64(a) >> 50) & 1
	var x0_51 uint64 = (uint64(a) >> 51) & 1
	var x0_52 uint64 = (uint64(a) >> 52) & 1
	var x0_53 uint64 = (uint64(a) >> 53) & 1
	var x0_54 uint64 = (uint64(a) >> 54) & 1
	var x0_55 uint64 = (uint64(a) >> 55) & 1
	var x0_56 uint64 = (uint64(a) >> 56) & 1
	var x0_57 uint64 = (uint64(a) >> 57) & 1
	var x0_58 uint64 = (uint64(a) >> 58) & 1
	var x0_59 uint64 = (uint64(a) >> 59) & 1
	var x0_60 uint64 = (uint64(a) >> 60) & 1
	var x0_61 uint64 = (uint64(a) >> 61) & 1
	var x0_62 uint64 = (uint64(a) >> 62) & 1
	var x0_63 uint64 = (uint64(a) >> 63) & 1
	var w0 uint64 = (x1_0 << 0)
	var w1 uint64 = w0 | (x1_1 << 1)
	var w2 uint64 = w1 | (x1_2 << 2)
	var w3 uint64 = w2 | (x1_3 << 3)
	var w4 uint64 = w3 | (x1_4 << 4)
	var w5 uint64 = w4 | (x1_5 << 5)
	var w6 uint64 = w5 | (x1_6 << 6)
	var w7 uint64 = w6 | (x1_7 << 7)
	var w8 uint64 = w7 | (x1_8 << 8)
	var w9 uint64 = w8 | (x1_9 << 9)
	var w10 uint64 = w9 | (x1_10 << 10)
	var w11 uint64 = w10 | (x1_11 << 11)
	var w12 uint64 = w11 | (x1_12 << 12)
	var w13 uint64 = w12 | (x1_13 << 13)
	var w14 uint64 = w13 | (x1_14 << 14)
	var w15 uint64 = w14 | (x1_15 << 15)
	var w16 uint64 = w15 | (x1_16 << 16)
	var w17 uint64 = w16 | (x1_17 << 17)
	var w18 uint64 = w17 | (x1_18 << 18)
	var w19 uint64 = w18 | (x1_19 << 19)
	var w20 uint64 = w19 | (x1_20 << 20)
	var w21 uint64 = w20 | (x1_21 << 21)
	var w22 uint64 = w21 | (x1_22 << 22)
	var w23 uint64 = w22 | (x1_23 << 23)
	var w24 uint64 = w23 | (x1_24 << 24)
	var w25 uint64 = w24 | (x1_25 << 25)
	var w26 uint64 = w25 | (x1_26 << 26)
	var w27 uint64 = w26 | (x1_27 << 27)
	var w28 uint64 = w27 | (x1_28 << 28)
	var w29 uint64 = w28 | (x1_29 << 29)
	var w30 uint64 = w29 | (x1_30 << 30)
	var w31 uint64 = w30 | (x1_31 << 31)
	var w32 uint64 = w31 | (x0_32 << 32)
	var w33 uint64 = w32 | (x0_33 << 33)
	var w34 uint64 = w33 | (x0_34 << 34)
	var w35 uint64 = w34 | (x0_35 << 35)
	var w36 uint64 = w35 | (x0_36 << 36)
	var w37 uint64 = w36 | (x0_37 << 37)
	var w38 uint64 = w37 | (x0_38 << 38)
	var w39 uint64 = w38 | (x0_39 << 39)
	var w40 uint64 = w39 | (x0_40 << 40)
	var w41 uint64 = w40 | (x0_41 << 41)
	var w42 uint64 = w41 | (x0_42 << 42)
	var w43 uint64 = w42 | (x0_43 << 43)
	var w44 uint64 = w43 | (x0_44 << 44)
	var w45 uint64 = w44 | (x0_45 << 45)
	var w46 uint64 = w45 | (x0_46 << 46)
	var w47 uint64 = w46 | (x0_47 << 47)
	var w48 uint64 = w47 | (x0_48 << 48)
	var w49 uint64 = w48 | (x0_49 << 49)
	var w50 uint64 = w49 | (x0_50 << 50)
	var w51 uint64 = w50 | (x0_51 << 51)
	var w52 uint64 = w51 | (x0_52 << 52)
	var w53 uint64 = w52 | (x0_53 << 53)
	var w54 uint64 = w53 | (x0_54 << 54)
	var w55 uint64 = w54 | (x0_55 << 55)
	var w56 uint64 = w55 | (x0_56 << 56)
	var w57 uint64 = w56 | (x0_57 << 57)
	var w58 uint64 = w57 | (x0_58 << 58)
	var w59 uint64 = w58 | (x0_59 << 59)
	var w60 uint64 = w59 | (x0_60 << 60)
	var w61 uint64 = w60 | (x0_61 << 61)
	var w62 uint64 = w61 | (x0_62 << 62)
	var w63 uint64 = w62 | (x0_63 << 63)
	return uint64(w63)
}

var g0 uint64
var g1 uint32
var sink interface{}

func main() {
	sink = emu_sw_gpr_gpr_imm_32__mem_MEM_a1__go__bit_blast(g0, g1)
	_ = sink
}
