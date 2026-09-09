// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of punpckldq_mem_xmm_128__reg_xmm0_high__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 32, v0), Extract(63, 32, v1))
package main

import "math"
import "unsafe"

//go:noinline
func emu_punpckldq_mem_xmm_128__reg_xmm0_high__go(a uint64, b float64) float64 {
	return math.Float64frombits(uint64((uint64(((uint64((uint32((uint64(a)) >> 32)))) << 32) | (uint64((uint32((uint64(*(*uint64)(unsafe.Pointer(&b)))) >> 32))))))))
}

var g0 uint64
var g1 float64
var sink interface{}

func main() {
	sink = emu_punpckldq_mem_xmm_128__reg_xmm0_high__go(g0, g1)
	_ = sink
}
