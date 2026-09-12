// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of neg_gpr_one_16__flags__go__bit_blast.
//   Concat(Extract(15, 0, v0), 0)
package main

//go:noinline
func emu_neg_gpr_one_16__flags__go__bit_blast(a uint16) uint32 {
	var x0_0 uint32 = (uint32(a) >> 0) & 1
	var x0_1 uint32 = (uint32(a) >> 1) & 1
	var x0_2 uint32 = (uint32(a) >> 2) & 1
	var x0_3 uint32 = (uint32(a) >> 3) & 1
	var x0_4 uint32 = (uint32(a) >> 4) & 1
	var x0_5 uint32 = (uint32(a) >> 5) & 1
	var x0_6 uint32 = (uint32(a) >> 6) & 1
	var x0_7 uint32 = (uint32(a) >> 7) & 1
	var x0_8 uint32 = (uint32(a) >> 8) & 1
	var x0_9 uint32 = (uint32(a) >> 9) & 1
	var x0_10 uint32 = (uint32(a) >> 10) & 1
	var x0_11 uint32 = (uint32(a) >> 11) & 1
	var x0_12 uint32 = (uint32(a) >> 12) & 1
	var x0_13 uint32 = (uint32(a) >> 13) & 1
	var x0_14 uint32 = (uint32(a) >> 14) & 1
	var x0_15 uint32 = (uint32(a) >> 15) & 1
	var k0 uint32 = 0
	var w0 uint32 = (k0 << 0)
	var w1 uint32 = w0 | (k0 << 1)
	var w2 uint32 = w1 | (k0 << 2)
	var w3 uint32 = w2 | (k0 << 3)
	var w4 uint32 = w3 | (k0 << 4)
	var w5 uint32 = w4 | (k0 << 5)
	var w6 uint32 = w5 | (k0 << 6)
	var w7 uint32 = w6 | (k0 << 7)
	var w8 uint32 = w7 | (k0 << 8)
	var w9 uint32 = w8 | (k0 << 9)
	var w10 uint32 = w9 | (k0 << 10)
	var w11 uint32 = w10 | (k0 << 11)
	var w12 uint32 = w11 | (k0 << 12)
	var w13 uint32 = w12 | (k0 << 13)
	var w14 uint32 = w13 | (k0 << 14)
	var w15 uint32 = w14 | (k0 << 15)
	var w16 uint32 = w15 | (x0_0 << 16)
	var w17 uint32 = w16 | (x0_1 << 17)
	var w18 uint32 = w17 | (x0_2 << 18)
	var w19 uint32 = w18 | (x0_3 << 19)
	var w20 uint32 = w19 | (x0_4 << 20)
	var w21 uint32 = w20 | (x0_5 << 21)
	var w22 uint32 = w21 | (x0_6 << 22)
	var w23 uint32 = w22 | (x0_7 << 23)
	var w24 uint32 = w23 | (x0_8 << 24)
	var w25 uint32 = w24 | (x0_9 << 25)
	var w26 uint32 = w25 | (x0_10 << 26)
	var w27 uint32 = w26 | (x0_11 << 27)
	var w28 uint32 = w27 | (x0_12 << 28)
	var w29 uint32 = w28 | (x0_13 << 29)
	var w30 uint32 = w29 | (x0_14 << 30)
	var w31 uint32 = w30 | (x0_15 << 31)
	return uint32(w31)
}

var g0 uint16
var sink interface{}

func main() {
	sink = emu_neg_gpr_one_16__flags__go__bit_blast(g0)
	_ = sink
}
