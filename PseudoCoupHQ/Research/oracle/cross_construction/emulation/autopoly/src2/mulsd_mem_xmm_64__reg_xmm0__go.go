// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of mulsd_mem_xmm_64__reg_xmm0__go.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(Extract(63, 0, v0)) * fpToFP(v1))
package main

import "math"

//go:noinline
func emu_mulsd_mem_xmm_64__reg_xmm0__go(a uint64, b float64) float64 {
	return math.Float64frombits(uint64(uint64(math.Float64bits(((b) * (math.Float64frombits(uint64(uint64(a)))))))))
}

var g0 uint64
var g1 float64
var sink interface{}

func main() {
	sink = emu_mulsd_mem_xmm_64__reg_xmm0__go(g0, g1)
	_ = sink
}
