// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of mulss_xmm_xmm_32__reg_xmm0__go.
// The term's layer-5 text, LITERAL:
//   fp.to_ieee_bv(fpToFP(Extract(31, 0, v0)) * fpToFP(Extract(31, 0, v1)))
package main

import "math"

//go:noinline
func emu_mulss_xmm_xmm_32__reg_xmm0__go(a float32, b float32) float32 {
	return math.Float32frombits(uint32(uint32(math.Float32bits(((a) * (b))))))
}

var g0 float32
var g1 float32
var sink interface{}

func main() {
	sink = emu_mulss_xmm_xmm_32__reg_xmm0__go(g0, g1)
	_ = sink
}
