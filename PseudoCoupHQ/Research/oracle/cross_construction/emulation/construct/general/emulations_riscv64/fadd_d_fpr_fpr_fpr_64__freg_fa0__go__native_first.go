// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of fadd_d_fpr_fpr_fpr_64__freg_fa0__go__native_first.
//   fp.to_ieee_bv(fpToFP(v0) + fpToFP(v1))
package main

import "math"

//go:noinline
func emu_fadd_d_fpr_fpr_fpr_64__freg_fa0__go__native_first(a uint64, b uint64) uint64 {
	var v0 float64 = math.Float64frombits(uint64(uint64(b)))
	var v1 float64 = math.Float64frombits(uint64(uint64(a)))
	var v2 float64 = ((v1) + (v0))
	var v3 uint64 = uint64(math.Float64bits(v2))
	return uint64(v3)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_fadd_d_fpr_fpr_fpr_64__freg_fa0__go__native_first(g0, g1)
	_ = sink
}
