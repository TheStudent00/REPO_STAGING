// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of test_gpr_same_8__flags__go__bit_blast.
//   Concat(Extract(7, 0, v0), 0)
package main

//go:noinline
func emu_test_gpr_same_8__flags__go__bit_blast(a uint8) uint16 {
	var x0_0 uint32 = (uint32(a) >> 0) & 1
	var x0_1 uint32 = (uint32(a) >> 1) & 1
	var x0_2 uint32 = (uint32(a) >> 2) & 1
	var x0_3 uint32 = (uint32(a) >> 3) & 1
	var x0_4 uint32 = (uint32(a) >> 4) & 1
	var x0_5 uint32 = (uint32(a) >> 5) & 1
	var x0_6 uint32 = (uint32(a) >> 6) & 1
	var x0_7 uint32 = (uint32(a) >> 7) & 1
	var k0 uint32 = 0
	var w0 uint32 = (k0 << 0)
	var w1 uint32 = w0 | (k0 << 1)
	var w2 uint32 = w1 | (k0 << 2)
	var w3 uint32 = w2 | (k0 << 3)
	var w4 uint32 = w3 | (k0 << 4)
	var w5 uint32 = w4 | (k0 << 5)
	var w6 uint32 = w5 | (k0 << 6)
	var w7 uint32 = w6 | (k0 << 7)
	var w8 uint32 = w7 | (x0_0 << 8)
	var w9 uint32 = w8 | (x0_1 << 9)
	var w10 uint32 = w9 | (x0_2 << 10)
	var w11 uint32 = w10 | (x0_3 << 11)
	var w12 uint32 = w11 | (x0_4 << 12)
	var w13 uint32 = w12 | (x0_5 << 13)
	var w14 uint32 = w13 | (x0_6 << 14)
	var w15 uint32 = w14 | (x0_7 << 15)
	return uint16(w15)
}

var g0 uint8
var sink interface{}

func main() {
	sink = emu_test_gpr_same_8__flags__go__bit_blast(g0)
	_ = sink
}
