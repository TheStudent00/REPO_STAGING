// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of cmpneqsd_xmm_xmm_64__reg_xmm0__go.
// The term's layer-5 text, LITERAL:
//   If(And(fpEQ(fpToFP(Extract(63, 0, v0)), fpToFP(Extract(63, 0, v1))), Not(Or(fpIsNaN(fpToFP(Extract(63, 0, v0))), fpIsNaN(fpToFP(Extract(63, 0, v1)))))), 0, 18446744073709551615)
package main

import "math"

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_cmpneqsd_xmm_xmm_64__reg_xmm0__go(a float64, b float64) float64 {
	return math.Float64frombits(uint64(sel64(((((a) == (b))) && ((!(((((a) != (a))) || (((b) != (b)))))))), uint64(uint64(0x0)), uint64(uint64(0xffffffffffffffff)))))
}

var g0 float64
var g1 float64
var sink interface{}

func main() {
	sink = emu_cmpneqsd_xmm_xmm_64__reg_xmm0__go(g0, g1)
	_ = sink
}
