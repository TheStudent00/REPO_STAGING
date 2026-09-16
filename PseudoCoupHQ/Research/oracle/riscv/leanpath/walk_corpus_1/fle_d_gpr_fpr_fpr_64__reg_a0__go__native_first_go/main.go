// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of fle_d_gpr_fpr_fpr_64__reg_a0__go__native_first.
//   If(fpToFP(v0) <= fpToFP(v1), 1, 0)
package main

import "math"

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_fle_d_gpr_fpr_fpr_64__reg_a0__go__native_first(a uint64, b uint64) uint64 {
	var v0 float64 = math.Float64frombits(uint64(uint64(b)))
	var v1 float64 = math.Float64frombits(uint64(uint64(a)))
	var v2 bool = ((v1) <= (v0))
	var v3 uint64 = sel64(v2, uint64(uint64(0x1)), uint64(uint64(0x0)))
	return uint64(v3)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_fle_d_gpr_fpr_fpr_64__reg_a0__go__native_first(g0, g1)
	_ = sink
}
