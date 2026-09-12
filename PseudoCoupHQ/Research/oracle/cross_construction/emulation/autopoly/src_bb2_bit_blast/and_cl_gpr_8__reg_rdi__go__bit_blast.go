// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of and_cl_gpr_8__reg_rdi__go__bit_blast.
//   Concat(Extract(63, 8, v1), ~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)))
package main

//go:noinline
func emu_and_cl_gpr_8__reg_rdi__go__bit_blast(a uint64, b uint8) uint64 {
	var x1_0 uint64 = (uint64(a) >> 0) & 1
	var x0_0 uint64 = (uint64(b) >> 0) & 1
	var x1_1 uint64 = (uint64(a) >> 1) & 1
	var x0_1 uint64 = (uint64(b) >> 1) & 1
	var x1_2 uint64 = (uint64(a) >> 2) & 1
	var x0_2 uint64 = (uint64(b) >> 2) & 1
	var x1_3 uint64 = (uint64(a) >> 3) & 1
	var x0_3 uint64 = (uint64(b) >> 3) & 1
	var x1_4 uint64 = (uint64(a) >> 4) & 1
	var x0_4 uint64 = (uint64(b) >> 4) & 1
	var x1_5 uint64 = (uint64(a) >> 5) & 1
	var x0_5 uint64 = (uint64(b) >> 5) & 1
	var x1_6 uint64 = (uint64(a) >> 6) & 1
	var x0_6 uint64 = (uint64(b) >> 6) & 1
	var x1_7 uint64 = (uint64(a) >> 7) & 1
	var x0_7 uint64 = (uint64(b) >> 7) & 1
	var x1_8 uint64 = (uint64(a) >> 8) & 1
	var x1_9 uint64 = (uint64(a) >> 9) & 1
	var x1_10 uint64 = (uint64(a) >> 10) & 1
	var x1_11 uint64 = (uint64(a) >> 11) & 1
	var x1_12 uint64 = (uint64(a) >> 12) & 1
	var x1_13 uint64 = (uint64(a) >> 13) & 1
	var x1_14 uint64 = (uint64(a) >> 14) & 1
	var x1_15 uint64 = (uint64(a) >> 15) & 1
	var x1_16 uint64 = (uint64(a) >> 16) & 1
	var x1_17 uint64 = (uint64(a) >> 17) & 1
	var x1_18 uint64 = (uint64(a) >> 18) & 1
	var x1_19 uint64 = (uint64(a) >> 19) & 1
	var x1_20 uint64 = (uint64(a) >> 20) & 1
	var x1_21 uint64 = (uint64(a) >> 21) & 1
	var x1_22 uint64 = (uint64(a) >> 22) & 1
	var x1_23 uint64 = (uint64(a) >> 23) & 1
	var x1_24 uint64 = (uint64(a) >> 24) & 1
	var x1_25 uint64 = (uint64(a) >> 25) & 1
	var x1_26 uint64 = (uint64(a) >> 26) & 1
	var x1_27 uint64 = (uint64(a) >> 27) & 1
	var x1_28 uint64 = (uint64(a) >> 28) & 1
	var x1_29 uint64 = (uint64(a) >> 29) & 1
	var x1_30 uint64 = (uint64(a) >> 30) & 1
	var x1_31 uint64 = (uint64(a) >> 31) & 1
	var x1_32 uint64 = (uint64(a) >> 32) & 1
	var x1_33 uint64 = (uint64(a) >> 33) & 1
	var x1_34 uint64 = (uint64(a) >> 34) & 1
	var x1_35 uint64 = (uint64(a) >> 35) & 1
	var x1_36 uint64 = (uint64(a) >> 36) & 1
	var x1_37 uint64 = (uint64(a) >> 37) & 1
	var x1_38 uint64 = (uint64(a) >> 38) & 1
	var x1_39 uint64 = (uint64(a) >> 39) & 1
	var x1_40 uint64 = (uint64(a) >> 40) & 1
	var x1_41 uint64 = (uint64(a) >> 41) & 1
	var x1_42 uint64 = (uint64(a) >> 42) & 1
	var x1_43 uint64 = (uint64(a) >> 43) & 1
	var x1_44 uint64 = (uint64(a) >> 44) & 1
	var x1_45 uint64 = (uint64(a) >> 45) & 1
	var x1_46 uint64 = (uint64(a) >> 46) & 1
	var x1_47 uint64 = (uint64(a) >> 47) & 1
	var x1_48 uint64 = (uint64(a) >> 48) & 1
	var x1_49 uint64 = (uint64(a) >> 49) & 1
	var x1_50 uint64 = (uint64(a) >> 50) & 1
	var x1_51 uint64 = (uint64(a) >> 51) & 1
	var x1_52 uint64 = (uint64(a) >> 52) & 1
	var x1_53 uint64 = (uint64(a) >> 53) & 1
	var x1_54 uint64 = (uint64(a) >> 54) & 1
	var x1_55 uint64 = (uint64(a) >> 55) & 1
	var x1_56 uint64 = (uint64(a) >> 56) & 1
	var x1_57 uint64 = (uint64(a) >> 57) & 1
	var x1_58 uint64 = (uint64(a) >> 58) & 1
	var x1_59 uint64 = (uint64(a) >> 59) & 1
	var x1_60 uint64 = (uint64(a) >> 60) & 1
	var x1_61 uint64 = (uint64(a) >> 61) & 1
	var x1_62 uint64 = (uint64(a) >> 62) & 1
	var x1_63 uint64 = (uint64(a) >> 63) & 1
	var g0 uint64 = (x0_0 & x1_0)
	var g1 uint64 = (x0_1 & x1_1)
	var g2 uint64 = (x0_2 & x1_2)
	var g3 uint64 = (x0_3 & x1_3)
	var g4 uint64 = (x0_4 & x1_4)
	var g5 uint64 = (x0_5 & x1_5)
	var g6 uint64 = (x0_6 & x1_6)
	var g7 uint64 = (x0_7 & x1_7)
	var w0 uint64 = (g0 << 0)
	var w1 uint64 = w0 | (g1 << 1)
	var w2 uint64 = w1 | (g2 << 2)
	var w3 uint64 = w2 | (g3 << 3)
	var w4 uint64 = w3 | (g4 << 4)
	var w5 uint64 = w4 | (g5 << 5)
	var w6 uint64 = w5 | (g6 << 6)
	var w7 uint64 = w6 | (g7 << 7)
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
	var w32 uint64 = w31 | (x1_32 << 32)
	var w33 uint64 = w32 | (x1_33 << 33)
	var w34 uint64 = w33 | (x1_34 << 34)
	var w35 uint64 = w34 | (x1_35 << 35)
	var w36 uint64 = w35 | (x1_36 << 36)
	var w37 uint64 = w36 | (x1_37 << 37)
	var w38 uint64 = w37 | (x1_38 << 38)
	var w39 uint64 = w38 | (x1_39 << 39)
	var w40 uint64 = w39 | (x1_40 << 40)
	var w41 uint64 = w40 | (x1_41 << 41)
	var w42 uint64 = w41 | (x1_42 << 42)
	var w43 uint64 = w42 | (x1_43 << 43)
	var w44 uint64 = w43 | (x1_44 << 44)
	var w45 uint64 = w44 | (x1_45 << 45)
	var w46 uint64 = w45 | (x1_46 << 46)
	var w47 uint64 = w46 | (x1_47 << 47)
	var w48 uint64 = w47 | (x1_48 << 48)
	var w49 uint64 = w48 | (x1_49 << 49)
	var w50 uint64 = w49 | (x1_50 << 50)
	var w51 uint64 = w50 | (x1_51 << 51)
	var w52 uint64 = w51 | (x1_52 << 52)
	var w53 uint64 = w52 | (x1_53 << 53)
	var w54 uint64 = w53 | (x1_54 << 54)
	var w55 uint64 = w54 | (x1_55 << 55)
	var w56 uint64 = w55 | (x1_56 << 56)
	var w57 uint64 = w56 | (x1_57 << 57)
	var w58 uint64 = w57 | (x1_58 << 58)
	var w59 uint64 = w58 | (x1_59 << 59)
	var w60 uint64 = w59 | (x1_60 << 60)
	var w61 uint64 = w60 | (x1_61 << 61)
	var w62 uint64 = w61 | (x1_62 << 62)
	var w63 uint64 = w62 | (x1_63 << 63)
	return uint64(w63)
}

var g0 uint64
var g1 uint8
var sink interface{}

func main() {
	sink = emu_and_cl_gpr_8__reg_rdi__go__bit_blast(g0, g1)
	_ = sink
}
