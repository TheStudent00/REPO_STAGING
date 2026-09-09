// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of punpckldq_mem_xmm_128__reg_xmm0_low__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(31, 0, v0), Extract(31, 0, v1))
package main

import "math"
import "unsafe"

//go:noinline
func emu_punpckldq_mem_xmm_128__reg_xmm0_low__go(a uint32, b float32) float64 {
	return math.Float64frombits(uint64((uint64(((uint64(uint32(a))) << 32) | (uint64(uint32(*(*uint32)(unsafe.Pointer(&b)))))))))
}

var g0 uint32
var g1 float32
var sink interface{}

func main() {
	sink = emu_punpckldq_mem_xmm_128__reg_xmm0_low__go(g0, g1)
	_ = sink
}
