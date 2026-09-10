// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of fcvt_d_lu_fpr_gpr_64__freg_fa0__go.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFPUnsigned(RNE(), v0))
package main

import "math"

//go:noinline
func emu_fcvt_d_lu_fpr_gpr_64__freg_fa0__go(a uint64) uint64 {
	return uint64(uint64(math.Float64bits(float64(uint64(uint64(a))))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_fcvt_d_lu_fpr_gpr_64__freg_fa0__go(g0)
	_ = sink
}
