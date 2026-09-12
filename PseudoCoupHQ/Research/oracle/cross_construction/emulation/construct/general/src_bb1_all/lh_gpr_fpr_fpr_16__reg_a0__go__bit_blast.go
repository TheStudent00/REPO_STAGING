// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of lh_gpr_fpr_fpr_16__reg_a0__go__bit_blast.
//   Concat(Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15,
package main

//go:noinline
func emu_lh_gpr_fpr_fpr_16__reg_a0__go__bit_blast(a uint16) uint64 {
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
	var w0 uint64 = (x0_0 << 0)
	var w1 uint64 = w0 | (x0_1 << 1)
	var w2 uint64 = w1 | (x0_2 << 2)
	var w3 uint64 = w2 | (x0_3 << 3)
	var w4 uint64 = w3 | (x0_4 << 4)
	var w5 uint64 = w4 | (x0_5 << 5)
	var w6 uint64 = w5 | (x0_6 << 6)
	var w7 uint64 = w6 | (x0_7 << 7)
	var w8 uint64 = w7 | (x0_8 << 8)
	var w9 uint64 = w8 | (x0_9 << 9)
	var w10 uint64 = w9 | (x0_10 << 10)
	var w11 uint64 = w10 | (x0_11 << 11)
	var w12 uint64 = w11 | (x0_12 << 12)
	var w13 uint64 = w12 | (x0_13 << 13)
	var w14 uint64 = w13 | (x0_14 << 14)
	var w15 uint64 = w14 | (x0_15 << 15)
	var w16 uint64 = w15 | (x0_15 << 16)
	var w17 uint64 = w16 | (x0_15 << 17)
	var w18 uint64 = w17 | (x0_15 << 18)
	var w19 uint64 = w18 | (x0_15 << 19)
	var w20 uint64 = w19 | (x0_15 << 20)
	var w21 uint64 = w20 | (x0_15 << 21)
	var w22 uint64 = w21 | (x0_15 << 22)
	var w23 uint64 = w22 | (x0_15 << 23)
	var w24 uint64 = w23 | (x0_15 << 24)
	var w25 uint64 = w24 | (x0_15 << 25)
	var w26 uint64 = w25 | (x0_15 << 26)
	var w27 uint64 = w26 | (x0_15 << 27)
	var w28 uint64 = w27 | (x0_15 << 28)
	var w29 uint64 = w28 | (x0_15 << 29)
	var w30 uint64 = w29 | (x0_15 << 30)
	var w31 uint64 = w30 | (x0_15 << 31)
	var w32 uint64 = w31 | (x0_15 << 32)
	var w33 uint64 = w32 | (x0_15 << 33)
	var w34 uint64 = w33 | (x0_15 << 34)
	var w35 uint64 = w34 | (x0_15 << 35)
	var w36 uint64 = w35 | (x0_15 << 36)
	var w37 uint64 = w36 | (x0_15 << 37)
	var w38 uint64 = w37 | (x0_15 << 38)
	var w39 uint64 = w38 | (x0_15 << 39)
	var w40 uint64 = w39 | (x0_15 << 40)
	var w41 uint64 = w40 | (x0_15 << 41)
	var w42 uint64 = w41 | (x0_15 << 42)
	var w43 uint64 = w42 | (x0_15 << 43)
	var w44 uint64 = w43 | (x0_15 << 44)
	var w45 uint64 = w44 | (x0_15 << 45)
	var w46 uint64 = w45 | (x0_15 << 46)
	var w47 uint64 = w46 | (x0_15 << 47)
	var w48 uint64 = w47 | (x0_15 << 48)
	var w49 uint64 = w48 | (x0_15 << 49)
	var w50 uint64 = w49 | (x0_15 << 50)
	var w51 uint64 = w50 | (x0_15 << 51)
	var w52 uint64 = w51 | (x0_15 << 52)
	var w53 uint64 = w52 | (x0_15 << 53)
	var w54 uint64 = w53 | (x0_15 << 54)
	var w55 uint64 = w54 | (x0_15 << 55)
	var w56 uint64 = w55 | (x0_15 << 56)
	var w57 uint64 = w56 | (x0_15 << 57)
	var w58 uint64 = w57 | (x0_15 << 58)
	var w59 uint64 = w58 | (x0_15 << 59)
	var w60 uint64 = w59 | (x0_15 << 60)
	var w61 uint64 = w60 | (x0_15 << 61)
	var w62 uint64 = w61 | (x0_15 << 62)
	var w63 uint64 = w62 | (x0_15 << 63)
	return uint64(w63)
}

var g0 uint16
var sink interface{}

func main() {
	sink = emu_lh_gpr_fpr_fpr_16__reg_a0__go__bit_blast(g0)
	_ = sink
}
