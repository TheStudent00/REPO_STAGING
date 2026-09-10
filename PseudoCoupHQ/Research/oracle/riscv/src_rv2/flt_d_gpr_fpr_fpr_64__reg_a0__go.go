// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of flt_d_gpr_fpr_fpr_64__reg_a0__go.
// The term's layer-5 text, LITERAL:
//   If(fpToFP(v0) < fpToFP(v1), 1, 0)
package main

import "math"

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_flt_d_gpr_fpr_fpr_64__reg_a0__go(a uint64, b uint64) uint64 {
	return uint64(sel64(((math.Float64frombits(uint64(uint64(a)))) < (math.Float64frombits(uint64(uint64(b))))), uint64(uint64(0x1)), uint64(uint64(0x0))))
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_flt_d_gpr_fpr_fpr_64__reg_a0__go(g0, g1)
	_ = sink
}
