// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of shr_imm_gpr_32__reg_rdi__go__bit_blast.
//   Concat(0, Extract(31, 3, v0))
package main

//go:noinline
func emu_shr_imm_gpr_32__reg_rdi__go__bit_blast(a uint32) uint64 {
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
	var k0 uint64 = 0
	var w0 uint64 = (x0_3 << 0)
	var w1 uint64 = w0 | (x0_4 << 1)
	var w2 uint64 = w1 | (x0_5 << 2)
	var w3 uint64 = w2 | (x0_6 << 3)
	var w4 uint64 = w3 | (x0_7 << 4)
	var w5 uint64 = w4 | (x0_8 << 5)
	var w6 uint64 = w5 | (x0_9 << 6)
	var w7 uint64 = w6 | (x0_10 << 7)
	var w8 uint64 = w7 | (x0_11 << 8)
	var w9 uint64 = w8 | (x0_12 << 9)
	var w10 uint64 = w9 | (x0_13 << 10)
	var w11 uint64 = w10 | (x0_14 << 11)
	var w12 uint64 = w11 | (x0_15 << 12)
	var w13 uint64 = w12 | (x0_16 << 13)
	var w14 uint64 = w13 | (x0_17 << 14)
	var w15 uint64 = w14 | (x0_18 << 15)
	var w16 uint64 = w15 | (x0_19 << 16)
	var w17 uint64 = w16 | (x0_20 << 17)
	var w18 uint64 = w17 | (x0_21 << 18)
	var w19 uint64 = w18 | (x0_22 << 19)
	var w20 uint64 = w19 | (x0_23 << 20)
	var w21 uint64 = w20 | (x0_24 << 21)
	var w22 uint64 = w21 | (x0_25 << 22)
	var w23 uint64 = w22 | (x0_26 << 23)
	var w24 uint64 = w23 | (x0_27 << 24)
	var w25 uint64 = w24 | (x0_28 << 25)
	var w26 uint64 = w25 | (x0_29 << 26)
	var w27 uint64 = w26 | (x0_30 << 27)
	var w28 uint64 = w27 | (x0_31 << 28)
	var w29 uint64 = w28 | (k0 << 29)
	var w30 uint64 = w29 | (k0 << 30)
	var w31 uint64 = w30 | (k0 << 31)
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
	sink = emu_shr_imm_gpr_32__reg_rdi__go__bit_blast(g0)
	_ = sink
}
