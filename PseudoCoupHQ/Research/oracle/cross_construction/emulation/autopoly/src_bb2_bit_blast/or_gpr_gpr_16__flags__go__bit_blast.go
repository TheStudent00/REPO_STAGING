// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of or_gpr_gpr_16__flags__go__bit_blast.
//   Concat(Extract(15, 0, v0) | Extract(15, 0, v1), 0)
package main

//go:noinline
func emu_or_gpr_gpr_16__flags__go__bit_blast(a uint16, b uint16) uint32 {
	var x1_0 uint32 = (uint32(b) >> 0) & 1
	var x0_0 uint32 = (uint32(a) >> 0) & 1
	var x1_1 uint32 = (uint32(b) >> 1) & 1
	var x0_1 uint32 = (uint32(a) >> 1) & 1
	var x1_2 uint32 = (uint32(b) >> 2) & 1
	var x0_2 uint32 = (uint32(a) >> 2) & 1
	var x1_3 uint32 = (uint32(b) >> 3) & 1
	var x0_3 uint32 = (uint32(a) >> 3) & 1
	var x1_4 uint32 = (uint32(b) >> 4) & 1
	var x0_4 uint32 = (uint32(a) >> 4) & 1
	var x1_5 uint32 = (uint32(b) >> 5) & 1
	var x0_5 uint32 = (uint32(a) >> 5) & 1
	var x1_6 uint32 = (uint32(b) >> 6) & 1
	var x0_6 uint32 = (uint32(a) >> 6) & 1
	var x1_7 uint32 = (uint32(b) >> 7) & 1
	var x0_7 uint32 = (uint32(a) >> 7) & 1
	var x1_8 uint32 = (uint32(b) >> 8) & 1
	var x0_8 uint32 = (uint32(a) >> 8) & 1
	var x1_9 uint32 = (uint32(b) >> 9) & 1
	var x0_9 uint32 = (uint32(a) >> 9) & 1
	var x1_10 uint32 = (uint32(b) >> 10) & 1
	var x0_10 uint32 = (uint32(a) >> 10) & 1
	var x1_11 uint32 = (uint32(b) >> 11) & 1
	var x0_11 uint32 = (uint32(a) >> 11) & 1
	var x1_12 uint32 = (uint32(b) >> 12) & 1
	var x0_12 uint32 = (uint32(a) >> 12) & 1
	var x1_13 uint32 = (uint32(b) >> 13) & 1
	var x0_13 uint32 = (uint32(a) >> 13) & 1
	var x1_14 uint32 = (uint32(b) >> 14) & 1
	var x0_14 uint32 = (uint32(a) >> 14) & 1
	var x1_15 uint32 = (uint32(b) >> 15) & 1
	var x0_15 uint32 = (uint32(a) >> 15) & 1
	var k0 uint32 = 0
	var g0 uint32 = (x0_0 | x1_0)
	var g1 uint32 = (x0_1 | x1_1)
	var g2 uint32 = (x0_2 | x1_2)
	var g3 uint32 = (x0_3 | x1_3)
	var g4 uint32 = (x0_4 | x1_4)
	var g5 uint32 = (x0_5 | x1_5)
	var g6 uint32 = (x0_6 | x1_6)
	var g7 uint32 = (x0_7 | x1_7)
	var g8 uint32 = (x0_8 | x1_8)
	var g9 uint32 = (x0_9 | x1_9)
	var g10 uint32 = (x0_10 | x1_10)
	var g11 uint32 = (x0_11 | x1_11)
	var g12 uint32 = (x0_12 | x1_12)
	var g13 uint32 = (x0_13 | x1_13)
	var g14 uint32 = (x0_14 | x1_14)
	var g15 uint32 = (x0_15 | x1_15)
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
	var w16 uint32 = w15 | (g0 << 16)
	var w17 uint32 = w16 | (g1 << 17)
	var w18 uint32 = w17 | (g2 << 18)
	var w19 uint32 = w18 | (g3 << 19)
	var w20 uint32 = w19 | (g4 << 20)
	var w21 uint32 = w20 | (g5 << 21)
	var w22 uint32 = w21 | (g6 << 22)
	var w23 uint32 = w22 | (g7 << 23)
	var w24 uint32 = w23 | (g8 << 24)
	var w25 uint32 = w24 | (g9 << 25)
	var w26 uint32 = w25 | (g10 << 26)
	var w27 uint32 = w26 | (g11 << 27)
	var w28 uint32 = w27 | (g12 << 28)
	var w29 uint32 = w28 | (g13 << 29)
	var w30 uint32 = w29 | (g14 << 30)
	var w31 uint32 = w30 | (g15 << 31)
	return uint32(w31)
}

var g0 uint16
var g1 uint16
var sink interface{}

func main() {
	sink = emu_or_gpr_gpr_16__flags__go__bit_blast(g0, g1)
	_ = sink
}
