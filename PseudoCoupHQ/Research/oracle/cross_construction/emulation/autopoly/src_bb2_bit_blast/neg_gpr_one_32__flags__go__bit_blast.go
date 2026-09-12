// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of neg_gpr_one_32__flags__go__bit_blast.
//   Concat(Extract(31, 0, v0), 0)
package main

//go:noinline
func emu_neg_gpr_one_32__flags__go__bit_blast(a uint32) uint64 {
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
	var k0 uint64 = 0
	var w0 uint64 = (k0 << 0)
	var w1 uint64 = w0 | (k0 << 1)
	var w2 uint64 = w1 | (k0 << 2)
	var w3 uint64 = w2 | (k0 << 3)
	var w4 uint64 = w3 | (k0 << 4)
	var w5 uint64 = w4 | (k0 << 5)
	var w6 uint64 = w5 | (k0 << 6)
	var w7 uint64 = w6 | (k0 << 7)
	var w8 uint64 = w7 | (k0 << 8)
	var w9 uint64 = w8 | (k0 << 9)
	var w10 uint64 = w9 | (k0 << 10)
	var w11 uint64 = w10 | (k0 << 11)
	var w12 uint64 = w11 | (k0 << 12)
	var w13 uint64 = w12 | (k0 << 13)
	var w14 uint64 = w13 | (k0 << 14)
	var w15 uint64 = w14 | (k0 << 15)
	var w16 uint64 = w15 | (k0 << 16)
	var w17 uint64 = w16 | (k0 << 17)
	var w18 uint64 = w17 | (k0 << 18)
	var w19 uint64 = w18 | (k0 << 19)
	var w20 uint64 = w19 | (k0 << 20)
	var w21 uint64 = w20 | (k0 << 21)
	var w22 uint64 = w21 | (k0 << 22)
	var w23 uint64 = w22 | (k0 << 23)
	var w24 uint64 = w23 | (k0 << 24)
	var w25 uint64 = w24 | (k0 << 25)
	var w26 uint64 = w25 | (k0 << 26)
	var w27 uint64 = w26 | (k0 << 27)
	var w28 uint64 = w27 | (k0 << 28)
	var w29 uint64 = w28 | (k0 << 29)
	var w30 uint64 = w29 | (k0 << 30)
	var w31 uint64 = w30 | (k0 << 31)
	var w32 uint64 = w31 | (x0_0 << 32)
	var w33 uint64 = w32 | (x0_1 << 33)
	var w34 uint64 = w33 | (x0_2 << 34)
	var w35 uint64 = w34 | (x0_3 << 35)
	var w36 uint64 = w35 | (x0_4 << 36)
	var w37 uint64 = w36 | (x0_5 << 37)
	var w38 uint64 = w37 | (x0_6 << 38)
	var w39 uint64 = w38 | (x0_7 << 39)
	var w40 uint64 = w39 | (x0_8 << 40)
	var w41 uint64 = w40 | (x0_9 << 41)
	var w42 uint64 = w41 | (x0_10 << 42)
	var w43 uint64 = w42 | (x0_11 << 43)
	var w44 uint64 = w43 | (x0_12 << 44)
	var w45 uint64 = w44 | (x0_13 << 45)
	var w46 uint64 = w45 | (x0_14 << 46)
	var w47 uint64 = w46 | (x0_15 << 47)
	var w48 uint64 = w47 | (x0_16 << 48)
	var w49 uint64 = w48 | (x0_17 << 49)
	var w50 uint64 = w49 | (x0_18 << 50)
	var w51 uint64 = w50 | (x0_19 << 51)
	var w52 uint64 = w51 | (x0_20 << 52)
	var w53 uint64 = w52 | (x0_21 << 53)
	var w54 uint64 = w53 | (x0_22 << 54)
	var w55 uint64 = w54 | (x0_23 << 55)
	var w56 uint64 = w55 | (x0_24 << 56)
	var w57 uint64 = w56 | (x0_25 << 57)
	var w58 uint64 = w57 | (x0_26 << 58)
	var w59 uint64 = w58 | (x0_27 << 59)
	var w60 uint64 = w59 | (x0_28 << 60)
	var w61 uint64 = w60 | (x0_29 << 61)
	var w62 uint64 = w61 | (x0_30 << 62)
	var w63 uint64 = w62 | (x0_31 << 63)
	return uint64(w63)
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_neg_gpr_one_32__flags__go__bit_blast(g0)
	_ = sink
}
