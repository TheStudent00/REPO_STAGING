// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of fcvt_d_l_fpr_gpr_64__freg_fa0__go__native_first.
//   fp.to_ieee_bv(fpToFP(RNE(), v0))
package main

import "math"

//go:noinline
func emu_fcvt_d_l_fpr_gpr_64__freg_fa0__go__native_first(a uint64) uint64 {
	var v0 float64 = float64((int64(uint64(a))))
	var v1 uint64 = uint64(math.Float64bits(v0))
	return uint64(v1)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_fcvt_d_l_fpr_gpr_64__freg_fa0__go__native_first(g0)
	_ = sink
}
