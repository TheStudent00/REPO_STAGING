// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of fle_s_gpr_fpr_fpr_32__reg_a0__go.
// The term's layer-5 text, LITERAL:
//   If(fpToFP(Extract(31, 0, v0)) <= fpToFP(Extract(31, 0, v1)), 1, 0)
package main

import "math"

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_fle_s_gpr_fpr_fpr_32__reg_a0__go(a uint32, b uint32) uint64 {
	return uint64(sel64(((math.Float32frombits(uint32(uint32(a)))) <= (math.Float32frombits(uint32(uint32(b))))), uint64(uint64(0x1)), uint64(uint64(0x0))))
}

var g0 uint32
var g1 uint32
var sink interface{}

func main() {
	sink = emu_fle_s_gpr_fpr_fpr_32__reg_a0__go(g0, g1)
	_ = sink
}
