// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of flt_s_gpr_fpr_fpr_32__reg_a0__go__native_first.
//   If(fpToFP(Extract(31, 0, v0)) < fpToFP(Extract(31, 0, v1)), 1, 0)
package main

import "math"

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_flt_s_gpr_fpr_fpr_32__reg_a0__go__native_first(a uint32, b uint32) uint64 {
	var v0 uint32 = uint32(b)
	var v1 float32 = math.Float32frombits(uint32(v0))
	var v2 uint32 = uint32(a)
	var v3 float32 = math.Float32frombits(uint32(v2))
	var v4 bool = ((v3) < (v1))
	var v5 uint64 = sel64(v4, uint64(uint64(0x1)), uint64(uint64(0x0)))
	return uint64(v5)
}

var g0 uint32
var g1 uint32
var sink interface{}

func main() {
	sink = emu_flt_s_gpr_fpr_fpr_32__reg_a0__go__native_first(g0, g1)
	_ = sink
}
