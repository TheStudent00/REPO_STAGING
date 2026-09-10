// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of fcvt_d_wu_fpr_gpr_64__freg_fa0__go.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFPUnsigned(RNE(), Extract(31, 0, v0)))
package main

import "math"

//go:noinline
func emu_fcvt_d_wu_fpr_gpr_64__freg_fa0__go(a uint32) uint64 {
	return uint64(uint64(math.Float64bits(float64(uint32(uint32(a))))))
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_fcvt_d_wu_fpr_gpr_64__freg_fa0__go(g0)
	_ = sink
}
