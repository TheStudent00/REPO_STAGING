// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of xor_imm_gpr_8__flags__go__bit_blast.
//   Concat(Extract(7, 0, v0) ^ Extract(7, 0, v1), 0)
package main

//go:noinline
func emu_xor_imm_gpr_8__flags__go__bit_blast(a uint8, b uint8) uint16 {
	var x1_0 uint32 = (uint32(a) >> 0) & 1
	var x0_0 uint32 = (uint32(b) >> 0) & 1
	var x1_1 uint32 = (uint32(a) >> 1) & 1
	var x0_1 uint32 = (uint32(b) >> 1) & 1
	var x1_2 uint32 = (uint32(a) >> 2) & 1
	var x0_2 uint32 = (uint32(b) >> 2) & 1
	var x1_3 uint32 = (uint32(a) >> 3) & 1
	var x0_3 uint32 = (uint32(b) >> 3) & 1
	var x1_4 uint32 = (uint32(a) >> 4) & 1
	var x0_4 uint32 = (uint32(b) >> 4) & 1
	var x1_5 uint32 = (uint32(a) >> 5) & 1
	var x0_5 uint32 = (uint32(b) >> 5) & 1
	var x1_6 uint32 = (uint32(a) >> 6) & 1
	var x0_6 uint32 = (uint32(b) >> 6) & 1
	var x1_7 uint32 = (uint32(a) >> 7) & 1
	var x0_7 uint32 = (uint32(b) >> 7) & 1
	var k0 uint32 = 0
	var g0 uint32 = (x0_0 ^ x1_0)
	var g1 uint32 = (g0 ^ 1)
	var g2 uint32 = (g1 ^ 1)
	var g3 uint32 = (x0_1 ^ x1_1)
	var g4 uint32 = (g3 ^ 1)
	var g5 uint32 = (g4 ^ 1)
	var g6 uint32 = (x0_2 ^ x1_2)
	var g7 uint32 = (g6 ^ 1)
	var g8 uint32 = (g7 ^ 1)
	var g9 uint32 = (x0_3 ^ x1_3)
	var g10 uint32 = (g9 ^ 1)
	var g11 uint32 = (g10 ^ 1)
	var g12 uint32 = (x0_4 ^ x1_4)
	var g13 uint32 = (g12 ^ 1)
	var g14 uint32 = (g13 ^ 1)
	var g15 uint32 = (x0_5 ^ x1_5)
	var g16 uint32 = (g15 ^ 1)
	var g17 uint32 = (g16 ^ 1)
	var g18 uint32 = (x0_6 ^ x1_6)
	var g19 uint32 = (g18 ^ 1)
	var g20 uint32 = (g19 ^ 1)
	var g21 uint32 = (x0_7 ^ x1_7)
	var g22 uint32 = (g21 ^ 1)
	var g23 uint32 = (g22 ^ 1)
	var w0 uint32 = (k0 << 0)
	var w1 uint32 = w0 | (k0 << 1)
	var w2 uint32 = w1 | (k0 << 2)
	var w3 uint32 = w2 | (k0 << 3)
	var w4 uint32 = w3 | (k0 << 4)
	var w5 uint32 = w4 | (k0 << 5)
	var w6 uint32 = w5 | (k0 << 6)
	var w7 uint32 = w6 | (k0 << 7)
	var w8 uint32 = w7 | (g2 << 8)
	var w9 uint32 = w8 | (g5 << 9)
	var w10 uint32 = w9 | (g8 << 10)
	var w11 uint32 = w10 | (g11 << 11)
	var w12 uint32 = w11 | (g14 << 12)
	var w13 uint32 = w12 | (g17 << 13)
	var w14 uint32 = w13 | (g20 << 14)
	var w15 uint32 = w14 | (g23 << 15)
	return uint16(w15)
}

var g0 uint8
var g1 uint8
var sink interface{}

func main() {
	sink = emu_xor_imm_gpr_8__flags__go__bit_blast(g0, g1)
	_ = sink
}
