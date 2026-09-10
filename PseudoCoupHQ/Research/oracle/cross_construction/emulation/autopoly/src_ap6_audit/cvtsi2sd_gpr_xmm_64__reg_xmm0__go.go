// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of cvtsi2sd_gpr_xmm_64__reg_xmm0__go.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(RNE(), v0))
package main

import "math"

//go:noinline
func emu_cvtsi2sd_gpr_xmm_64__reg_xmm0__go(a uint64) float64 {
	return math.Float64frombits(uint64(uint64(math.Float64bits(float64((int64(uint64(a))))))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_cvtsi2sd_gpr_xmm_64__reg_xmm0__go(g0)
	_ = sink
}
