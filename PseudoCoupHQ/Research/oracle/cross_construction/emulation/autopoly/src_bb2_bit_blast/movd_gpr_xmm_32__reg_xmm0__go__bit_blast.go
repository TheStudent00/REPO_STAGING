// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of movd_gpr_xmm_32__reg_xmm0__go__bit_blast.
//   Extract(31, 0, v0)
package main

import "math"

//go:noinline
func emu_movd_gpr_xmm_32__reg_xmm0__go__bit_blast(a uint32) float32 {
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
	var x0_16 uint32 = (uint32(a) >> 16) & 1
	var x0_17 uint32 = (uint32(a) >> 17) & 1
	var x0_18 uint32 = (uint32(a) >> 18) & 1
	var x0_19 uint32 = (uint32(a) >> 19) & 1
	var x0_20 uint32 = (uint32(a) >> 20) & 1
	var x0_21 uint32 = (uint32(a) >> 21) & 1
	var x0_22 uint32 = (uint32(a) >> 22) & 1
	var x0_23 uint32 = (uint32(a) >> 23) & 1
	var x0_24 uint32 = (uint32(a) >> 24) & 1
	var x0_25 uint32 = (uint32(a) >> 25) & 1
	var x0_26 uint32 = (uint32(a) >> 26) & 1
	var x0_27 uint32 = (uint32(a) >> 27) & 1
	var x0_28 uint32 = (uint32(a) >> 28) & 1
	var x0_29 uint32 = (uint32(a) >> 29) & 1
	var x0_30 uint32 = (uint32(a) >> 30) & 1
	var x0_31 uint32 = (uint32(a) >> 31) & 1
	var w0 uint32 = (x0_0 << 0)
	var w1 uint32 = w0 | (x0_1 << 1)
	var w2 uint32 = w1 | (x0_2 << 2)
	var w3 uint32 = w2 | (x0_3 << 3)
	var w4 uint32 = w3 | (x0_4 << 4)
	var w5 uint32 = w4 | (x0_5 << 5)
	var w6 uint32 = w5 | (x0_6 << 6)
	var w7 uint32 = w6 | (x0_7 << 7)
	var w8 uint32 = w7 | (x0_8 << 8)
	var w9 uint32 = w8 | (x0_9 << 9)
	var w10 uint32 = w9 | (x0_10 << 10)
	var w11 uint32 = w10 | (x0_11 << 11)
	var w12 uint32 = w11 | (x0_12 << 12)
	var w13 uint32 = w12 | (x0_13 << 13)
	var w14 uint32 = w13 | (x0_14 << 14)
	var w15 uint32 = w14 | (x0_15 << 15)
	var w16 uint32 = w15 | (x0_16 << 16)
	var w17 uint32 = w16 | (x0_17 << 17)
	var w18 uint32 = w17 | (x0_18 << 18)
	var w19 uint32 = w18 | (x0_19 << 19)
	var w20 uint32 = w19 | (x0_20 << 20)
	var w21 uint32 = w20 | (x0_21 << 21)
	var w22 uint32 = w21 | (x0_22 << 22)
	var w23 uint32 = w22 | (x0_23 << 23)
	var w24 uint32 = w23 | (x0_24 << 24)
	var w25 uint32 = w24 | (x0_25 << 25)
	var w26 uint32 = w25 | (x0_26 << 26)
	var w27 uint32 = w26 | (x0_27 << 27)
	var w28 uint32 = w27 | (x0_28 << 28)
	var w29 uint32 = w28 | (x0_29 << 29)
	var w30 uint32 = w29 | (x0_30 << 30)
	var w31 uint32 = w30 | (x0_31 << 31)
	return math.Float32frombits(uint32(w31))
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_movd_gpr_xmm_32__reg_xmm0__go__bit_blast(g0)
	_ = sink
}
