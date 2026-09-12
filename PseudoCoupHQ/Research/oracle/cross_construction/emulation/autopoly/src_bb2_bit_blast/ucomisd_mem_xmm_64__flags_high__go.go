// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of ucomisd_mem_xmm_64__flags_high__go.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(Extract(63, 0, v0)))
package main

import "math"

//go:noinline
func emu_ucomisd_mem_xmm_64__flags_high__go(a float64) uint64 {
	return uint64(uint64(math.Float64bits(a)))
}

var g0 float64
var sink interface{}

func main() {
	sink = emu_ucomisd_mem_xmm_64__flags_high__go(g0)
	_ = sink
}
