// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of setne_gpr_one_8__reg_rdi__go__bit_blast.
//   Concat(Extract(63, 8, v2), If(Extract(7, 0, v0) | Extract(7, 0, v1) == 0, 0, 1))
package main

//go:noinline
func emu_setne_gpr_one_8__reg_rdi__go__bit_blast(a uint8, b uint8, c uint64) uint64 {
	var x1_7 uint64 = (uint64(a) >> 7) & 1
	var x0_7 uint64 = (uint64(b) >> 7) & 1
	var x1_6 uint64 = (uint64(a) >> 6) & 1
	var x0_6 uint64 = (uint64(b) >> 6) & 1
	var x1_5 uint64 = (uint64(a) >> 5) & 1
	var x0_5 uint64 = (uint64(b) >> 5) & 1
	var x1_4 uint64 = (uint64(a) >> 4) & 1
	var x0_4 uint64 = (uint64(b) >> 4) & 1
	var x1_3 uint64 = (uint64(a) >> 3) & 1
	var x0_3 uint64 = (uint64(b) >> 3) & 1
	var x1_2 uint64 = (uint64(a) >> 2) & 1
	var x0_2 uint64 = (uint64(b) >> 2) & 1
	var x1_1 uint64 = (uint64(a) >> 1) & 1
	var x0_1 uint64 = (uint64(b) >> 1) & 1
	var x1_0 uint64 = (uint64(a) >> 0) & 1
	var x0_0 uint64 = (uint64(b) >> 0) & 1
	var x2_8 uint64 = (uint64(c) >> 8) & 1
	var x2_9 uint64 = (uint64(c) >> 9) & 1
	var x2_10 uint64 = (uint64(c) >> 10) & 1
	var x2_11 uint64 = (uint64(c) >> 11) & 1
	var x2_12 uint64 = (uint64(c) >> 12) & 1
	var x2_13 uint64 = (uint64(c) >> 13) & 1
	var x2_14 uint64 = (uint64(c) >> 14) & 1
	var x2_15 uint64 = (uint64(c) >> 15) & 1
	var x2_16 uint64 = (uint64(c) >> 16) & 1
	var x2_17 uint64 = (uint64(c) >> 17) & 1
	var x2_18 uint64 = (uint64(c) >> 18) & 1
	var x2_19 uint64 = (uint64(c) >> 19) & 1
	var x2_20 uint64 = (uint64(c) >> 20) & 1
	var x2_21 uint64 = (uint64(c) >> 21) & 1
	var x2_22 uint64 = (uint64(c) >> 22) & 1
	var x2_23 uint64 = (uint64(c) >> 23) & 1
	var x2_24 uint64 = (uint64(c) >> 24) & 1
	var x2_25 uint64 = (uint64(c) >> 25) & 1
	var x2_26 uint64 = (uint64(c) >> 26) & 1
	var x2_27 uint64 = (uint64(c) >> 27) & 1
	var x2_28 uint64 = (uint64(c) >> 28) & 1
	var x2_29 uint64 = (uint64(c) >> 29) & 1
	var x2_30 uint64 = (uint64(c) >> 30) & 1
	var x2_31 uint64 = (uint64(c) >> 31) & 1
	var x2_32 uint64 = (uint64(c) >> 32) & 1
	var x2_33 uint64 = (uint64(c) >> 33) & 1
	var x2_34 uint64 = (uint64(c) >> 34) & 1
	var x2_35 uint64 = (uint64(c) >> 35) & 1
	var x2_36 uint64 = (uint64(c) >> 36) & 1
	var x2_37 uint64 = (uint64(c) >> 37) & 1
	var x2_38 uint64 = (uint64(c) >> 38) & 1
	var x2_39 uint64 = (uint64(c) >> 39) & 1
	var x2_40 uint64 = (uint64(c) >> 40) & 1
	var x2_41 uint64 = (uint64(c) >> 41) & 1
	var x2_42 uint64 = (uint64(c) >> 42) & 1
	var x2_43 uint64 = (uint64(c) >> 43) & 1
	var x2_44 uint64 = (uint64(c) >> 44) & 1
	var x2_45 uint64 = (uint64(c) >> 45) & 1
	var x2_46 uint64 = (uint64(c) >> 46) & 1
	var x2_47 uint64 = (uint64(c) >> 47) & 1
	var x2_48 uint64 = (uint64(c) >> 48) & 1
	var x2_49 uint64 = (uint64(c) >> 49) & 1
	var x2_50 uint64 = (uint64(c) >> 50) & 1
	var x2_51 uint64 = (uint64(c) >> 51) & 1
	var x2_52 uint64 = (uint64(c) >> 52) & 1
	var x2_53 uint64 = (uint64(c) >> 53) & 1
	var x2_54 uint64 = (uint64(c) >> 54) & 1
	var x2_55 uint64 = (uint64(c) >> 55) & 1
	var x2_56 uint64 = (uint64(c) >> 56) & 1
	var x2_57 uint64 = (uint64(c) >> 57) & 1
	var x2_58 uint64 = (uint64(c) >> 58) & 1
	var x2_59 uint64 = (uint64(c) >> 59) & 1
	var x2_60 uint64 = (uint64(c) >> 60) & 1
	var x2_61 uint64 = (uint64(c) >> 61) & 1
	var x2_62 uint64 = (uint64(c) >> 62) & 1
	var x2_63 uint64 = (uint64(c) >> 63) & 1
	var g0 uint64 = (x0_7 | x1_7)
	var g1 uint64 = (x0_6 | x1_6)
	var g2 uint64 = (x0_5 | x1_5)
	var g3 uint64 = (x0_4 | x1_4)
	var g4 uint64 = (x0_3 | x1_3)
	var g5 uint64 = (x0_2 | x1_2)
	var g6 uint64 = (x0_1 | x1_1)
	var g7 uint64 = (x0_0 | x1_0)
	var g8 uint64 = (g7 | g6)
	var g9 uint64 = (g8 | g5)
	var g10 uint64 = (g9 | g4)
	var g11 uint64 = (g10 | g3)
	var g12 uint64 = (g11 | g2)
	var g13 uint64 = (g12 | g1)
	var g14 uint64 = (g13 | g0)
	var g15 uint64 = (g14 ^ 1)
	var g16 uint64 = (g15 ^ 1)
	var k0 uint64 = 0
	var w0 uint64 = (g16 << 0)
	var w1 uint64 = w0 | (k0 << 1)
	var w2 uint64 = w1 | (k0 << 2)
	var w3 uint64 = w2 | (k0 << 3)
	var w4 uint64 = w3 | (k0 << 4)
	var w5 uint64 = w4 | (k0 << 5)
	var w6 uint64 = w5 | (k0 << 6)
	var w7 uint64 = w6 | (k0 << 7)
	var w8 uint64 = w7 | (x2_8 << 8)
	var w9 uint64 = w8 | (x2_9 << 9)
	var w10 uint64 = w9 | (x2_10 << 10)
	var w11 uint64 = w10 | (x2_11 << 11)
	var w12 uint64 = w11 | (x2_12 << 12)
	var w13 uint64 = w12 | (x2_13 << 13)
	var w14 uint64 = w13 | (x2_14 << 14)
	var w15 uint64 = w14 | (x2_15 << 15)
	var w16 uint64 = w15 | (x2_16 << 16)
	var w17 uint64 = w16 | (x2_17 << 17)
	var w18 uint64 = w17 | (x2_18 << 18)
	var w19 uint64 = w18 | (x2_19 << 19)
	var w20 uint64 = w19 | (x2_20 << 20)
	var w21 uint64 = w20 | (x2_21 << 21)
	var w22 uint64 = w21 | (x2_22 << 22)
	var w23 uint64 = w22 | (x2_23 << 23)
	var w24 uint64 = w23 | (x2_24 << 24)
	var w25 uint64 = w24 | (x2_25 << 25)
	var w26 uint64 = w25 | (x2_26 << 26)
	var w27 uint64 = w26 | (x2_27 << 27)
	var w28 uint64 = w27 | (x2_28 << 28)
	var w29 uint64 = w28 | (x2_29 << 29)
	var w30 uint64 = w29 | (x2_30 << 30)
	var w31 uint64 = w30 | (x2_31 << 31)
	var w32 uint64 = w31 | (x2_32 << 32)
	var w33 uint64 = w32 | (x2_33 << 33)
	var w34 uint64 = w33 | (x2_34 << 34)
	var w35 uint64 = w34 | (x2_35 << 35)
	var w36 uint64 = w35 | (x2_36 << 36)
	var w37 uint64 = w36 | (x2_37 << 37)
	var w38 uint64 = w37 | (x2_38 << 38)
	var w39 uint64 = w38 | (x2_39 << 39)
	var w40 uint64 = w39 | (x2_40 << 40)
	var w41 uint64 = w40 | (x2_41 << 41)
	var w42 uint64 = w41 | (x2_42 << 42)
	var w43 uint64 = w42 | (x2_43 << 43)
	var w44 uint64 = w43 | (x2_44 << 44)
	var w45 uint64 = w44 | (x2_45 << 45)
	var w46 uint64 = w45 | (x2_46 << 46)
	var w47 uint64 = w46 | (x2_47 << 47)
	var w48 uint64 = w47 | (x2_48 << 48)
	var w49 uint64 = w48 | (x2_49 << 49)
	var w50 uint64 = w49 | (x2_50 << 50)
	var w51 uint64 = w50 | (x2_51 << 51)
	var w52 uint64 = w51 | (x2_52 << 52)
	var w53 uint64 = w52 | (x2_53 << 53)
	var w54 uint64 = w53 | (x2_54 << 54)
	var w55 uint64 = w54 | (x2_55 << 55)
	var w56 uint64 = w55 | (x2_56 << 56)
	var w57 uint64 = w56 | (x2_57 << 57)
	var w58 uint64 = w57 | (x2_58 << 58)
	var w59 uint64 = w58 | (x2_59 << 59)
	var w60 uint64 = w59 | (x2_60 << 60)
	var w61 uint64 = w60 | (x2_61 << 61)
	var w62 uint64 = w61 | (x2_62 << 62)
	var w63 uint64 = w62 | (x2_63 << 63)
	return uint64(w63)
}

var g0 uint8
var g1 uint8
var g2 uint64
var sink interface{}

func main() {
	sink = emu_setne_gpr_one_8__reg_rdi__go__bit_blast(g0, g1, g2)
	_ = sink
}
