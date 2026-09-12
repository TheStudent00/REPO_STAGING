// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of fcvt_d_s_fpr_fpr_64__freg_fa0__go__native_first.
//   fp.to_ieee_bv(fpToFP(RNE(), fpToFP(Extract(31, 0, v0))))
package main

import "math"

//go:noinline
func emu_fcvt_d_s_fpr_fpr_64__freg_fa0__go__native_first(a uint32) uint64 {
	var v0 uint32 = uint32(a)
	var v1 float32 = math.Float32frombits(uint32(v0))
	var v2 float64 = float64(v1)
	var v3 uint64 = uint64(math.Float64bits(v2))
	return uint64(v3)
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_fcvt_d_s_fpr_fpr_64__freg_fa0__go__native_first(g0)
	_ = sink
}
