// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of movapd_xmm_xmm_128__reg_xmm0_low__go.
// The term's layer-5 text, LITERAL:
//   Extract(63, 0, v0)
package main

import "math"
import "unsafe"

//go:noinline
func emu_movapd_xmm_xmm_128__reg_xmm0_low__go(a float64) float64 {
	return math.Float64frombits(uint64(uint64(*(*uint64)(unsafe.Pointer(&a)))))
}

var g0 float64
var sink interface{}

func main() {
	sink = emu_movapd_xmm_xmm_128__reg_xmm0_low__go(g0)
	_ = sink
}
