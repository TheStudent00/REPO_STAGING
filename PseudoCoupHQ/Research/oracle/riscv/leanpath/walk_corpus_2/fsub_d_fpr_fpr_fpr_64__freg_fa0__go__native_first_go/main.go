// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of fsub_d_fpr_fpr_fpr_64__freg_fa0__go__native_first.
//   fp.to_ieee_bv(-fpToFP(v0) + fpToFP(v1))
package main

import "math"

//go:noinline
func emu_fsub_d_fpr_fpr_fpr_64__freg_fa0__go__native_first(a uint64, b uint64) uint64 {
	var v0 float64 = math.Float64frombits(uint64(uint64(a)))
	var v1 float64 = math.Float64frombits(uint64(uint64(b)))
	var v2 float64 = (-(v1))
	var v3 float64 = ((v2) + (v0))
	var v4 uint64 = uint64(math.Float64bits(v3))
	return uint64(v4)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_fsub_d_fpr_fpr_fpr_64__freg_fa0__go__native_first(g0, g1)
	_ = sink
}
