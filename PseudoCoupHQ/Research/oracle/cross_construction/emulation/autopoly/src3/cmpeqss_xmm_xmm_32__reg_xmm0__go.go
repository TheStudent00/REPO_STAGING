// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of cmpeqss_xmm_xmm_32__reg_xmm0__go.
// The term's layer-5 text, LITERAL:
//   If(And(fpEQ(fpToFP(Extract(31, 0, v0)), fpToFP(Extract(31, 0, v1))), Not(Or(fpIsNaN(fpToFP(Extract(31, 0, v0))), fpIsNaN(fpToFP(Extract(31, 0, v1)))))), 4294967295, 0)
package main

import "math"

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_cmpeqss_xmm_xmm_32__reg_xmm0__go(a float32, b float32) float32 {
	return math.Float32frombits(uint32(sel32(((((a) == (b))) && ((!(((((a) != (a))) || (((b) != (b)))))))), uint32(uint32(0xffffffff)), uint32(uint32(0x0)))))
}

var g0 float32
var g1 float32
var sink interface{}

func main() {
	sink = emu_cmpeqss_xmm_xmm_32__reg_xmm0__go(g0, g1)
	_ = sink
}
