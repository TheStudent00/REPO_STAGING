// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of not_gpr_one_32__reg_rdi__go__bit_blast.
//   Concat(0, ~Extract(31, 0, v0))
package main

//go:noinline
func emu_not_gpr_one_32__reg_rdi__go__bit_blast(a uint32) uint64 {
	var x0_0 uint64 = (uint64(a) >> 0) & 1
	var x0_1 uint64 = (uint64(a) >> 1) & 1
	var x0_2 uint64 = (uint64(a) >> 2) & 1
	var x0_3 uint64 = (uint64(a) >> 3) & 1
	var x0_4 uint64 = (uint64(a) >> 4) & 1
	var x0_5 uint64 = (uint64(a) >> 5) & 1
	var x0_6 uint64 = (uint64(a) >> 6) & 1
	var x0_7 uint64 = (uint64(a) >> 7) & 1
	var x0_8 uint64 = (uint64(a) >> 8) & 1
	var x0_9 uint64 = (uint64(a) >> 9) & 1
	var x0_10 uint64 = (uint64(a) >> 10) & 1
	var x0_11 uint64 = (uint64(a) >> 11) & 1
	var x0_12 uint64 = (uint64(a) >> 12) & 1
	var x0_13 uint64 = (uint64(a) >> 13) & 1
	var x0_14 uint64 = (uint64(a) >> 14) & 1
	var x0_15 uint64 = (uint64(a) >> 15) & 1
	var x0_16 uint64 = (uint64(a) >> 16) & 1
	var x0_17 uint64 = (uint64(a) >> 17) & 1
	var x0_18 uint64 = (uint64(a) >> 18) & 1
	var x0_19 uint64 = (uint64(a) >> 19) & 1
	var x0_20 uint64 = (uint64(a) >> 20) & 1
	var x0_21 uint64 = (uint64(a) >> 21) & 1
	var x0_22 uint64 = (uint64(a) >> 22) & 1
	var x0_23 uint64 = (uint64(a) >> 23) & 1
	var x0_24 uint64 = (uint64(a) >> 24) & 1
	var x0_25 uint64 = (uint64(a) >> 25) & 1
	var x0_26 uint64 = (uint64(a) >> 26) & 1
	var x0_27 uint64 = (uint64(a) >> 27) & 1
	var x0_28 uint64 = (uint64(a) >> 28) & 1
	var x0_29 uint64 = (uint64(a) >> 29) & 1
	var x0_30 uint64 = (uint64(a) >> 30) & 1
	var x0_31 uint64 = (uint64(a) >> 31) & 1
	var g0 uint64 = (x0_0 ^ 1)
	var g1 uint64 = (x0_1 ^ 1)
	var g2 uint64 = (x0_2 ^ 1)
	var g3 uint64 = (x0_3 ^ 1)
	var g4 uint64 = (x0_4 ^ 1)
	var g5 uint64 = (x0_5 ^ 1)
	var g6 uint64 = (x0_6 ^ 1)
	var g7 uint64 = (x0_7 ^ 1)
	var g8 uint64 = (x0_8 ^ 1)
	var g9 uint64 = (x0_9 ^ 1)
	var g10 uint64 = (x0_10 ^ 1)
	var g11 uint64 = (x0_11 ^ 1)
	var g12 uint64 = (x0_12 ^ 1)
	var g13 uint64 = (x0_13 ^ 1)
	var g14 uint64 = (x0_14 ^ 1)
	var g15 uint64 = (x0_15 ^ 1)
	var g16 uint64 = (x0_16 ^ 1)
	var g17 uint64 = (x0_17 ^ 1)
	var g18 uint64 = (x0_18 ^ 1)
	var g19 uint64 = (x0_19 ^ 1)
	var g20 uint64 = (x0_20 ^ 1)
	var g21 uint64 = (x0_21 ^ 1)
	var g22 uint64 = (x0_22 ^ 1)
	var g23 uint64 = (x0_23 ^ 1)
	var g24 uint64 = (x0_24 ^ 1)
	var g25 uint64 = (x0_25 ^ 1)
	var g26 uint64 = (x0_26 ^ 1)
	var g27 uint64 = (x0_27 ^ 1)
	var g28 uint64 = (x0_28 ^ 1)
	var g29 uint64 = (x0_29 ^ 1)
	var g30 uint64 = (x0_30 ^ 1)
	var g31 uint64 = (x0_31 ^ 1)
	var k0 uint64 = 0
	var w0 uint64 = (g0 << 0)
	var w1 uint64 = w0 | (g1 << 1)
	var w2 uint64 = w1 | (g2 << 2)
	var w3 uint64 = w2 | (g3 << 3)
	var w4 uint64 = w3 | (g4 << 4)
	var w5 uint64 = w4 | (g5 << 5)
	var w6 uint64 = w5 | (g6 << 6)
	var w7 uint64 = w6 | (g7 << 7)
	var w8 uint64 = w7 | (g8 << 8)
	var w9 uint64 = w8 | (g9 << 9)
	var w10 uint64 = w9 | (g10 << 10)
	var w11 uint64 = w10 | (g11 << 11)
	var w12 uint64 = w11 | (g12 << 12)
	var w13 uint64 = w12 | (g13 << 13)
	var w14 uint64 = w13 | (g14 << 14)
	var w15 uint64 = w14 | (g15 << 15)
	var w16 uint64 = w15 | (g16 << 16)
	var w17 uint64 = w16 | (g17 << 17)
	var w18 uint64 = w17 | (g18 << 18)
	var w19 uint64 = w18 | (g19 << 19)
	var w20 uint64 = w19 | (g20 << 20)
	var w21 uint64 = w20 | (g21 << 21)
	var w22 uint64 = w21 | (g22 << 22)
	var w23 uint64 = w22 | (g23 << 23)
	var w24 uint64 = w23 | (g24 << 24)
	var w25 uint64 = w24 | (g25 << 25)
	var w26 uint64 = w25 | (g26 << 26)
	var w27 uint64 = w26 | (g27 << 27)
	var w28 uint64 = w27 | (g28 << 28)
	var w29 uint64 = w28 | (g29 << 29)
	var w30 uint64 = w29 | (g30 << 30)
	var w31 uint64 = w30 | (g31 << 31)
	var w32 uint64 = w31 | (k0 << 32)
	var w33 uint64 = w32 | (k0 << 33)
	var w34 uint64 = w33 | (k0 << 34)
	var w35 uint64 = w34 | (k0 << 35)
	var w36 uint64 = w35 | (k0 << 36)
	var w37 uint64 = w36 | (k0 << 37)
	var w38 uint64 = w37 | (k0 << 38)
	var w39 uint64 = w38 | (k0 << 39)
	var w40 uint64 = w39 | (k0 << 40)
	var w41 uint64 = w40 | (k0 << 41)
	var w42 uint64 = w41 | (k0 << 42)
	var w43 uint64 = w42 | (k0 << 43)
	var w44 uint64 = w43 | (k0 << 44)
	var w45 uint64 = w44 | (k0 << 45)
	var w46 uint64 = w45 | (k0 << 46)
	var w47 uint64 = w46 | (k0 << 47)
	var w48 uint64 = w47 | (k0 << 48)
	var w49 uint64 = w48 | (k0 << 49)
	var w50 uint64 = w49 | (k0 << 50)
	var w51 uint64 = w50 | (k0 << 51)
	var w52 uint64 = w51 | (k0 << 52)
	var w53 uint64 = w52 | (k0 << 53)
	var w54 uint64 = w53 | (k0 << 54)
	var w55 uint64 = w54 | (k0 << 55)
	var w56 uint64 = w55 | (k0 << 56)
	var w57 uint64 = w56 | (k0 << 57)
	var w58 uint64 = w57 | (k0 << 58)
	var w59 uint64 = w58 | (k0 << 59)
	var w60 uint64 = w59 | (k0 << 60)
	var w61 uint64 = w60 | (k0 << 61)
	var w62 uint64 = w61 | (k0 << 62)
	var w63 uint64 = w62 | (k0 << 63)
	return uint64(w63)
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_not_gpr_one_32__reg_rdi__go__bit_blast(g0)
	_ = sink
}
