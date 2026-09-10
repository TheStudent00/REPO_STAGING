// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of cmpeqsd_mem_xmm_64__reg_xmm0__go.
// The term's layer-5 text, LITERAL:
//   If(And(fpEQ(fpToFP(Extract(63, 0, v0)), fpToFP(v1)), Not(Or(fpIsNaN(fpToFP(Extract(63, 0, v0))), fpIsNaN(fpToFP(v1))))), 18446744073709551615, 0)
package main

import "math"

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_cmpeqsd_mem_xmm_64__reg_xmm0__go(a uint64, b float64) float64 {
	return math.Float64frombits(uint64(sel64(((((b) == (math.Float64frombits(uint64(uint64(a)))))) && ((!(((((b) != (b))) || (((math.Float64frombits(uint64(uint64(a)))) != (math.Float64frombits(uint64(uint64(a))))))))))), uint64(uint64(0xffffffffffffffff)), uint64(uint64(0x0)))))
}

var g0 uint64
var g1 float64
var sink interface{}

func main() {
	sink = emu_cmpeqsd_mem_xmm_64__reg_xmm0__go(g0, g1)
	_ = sink
}
