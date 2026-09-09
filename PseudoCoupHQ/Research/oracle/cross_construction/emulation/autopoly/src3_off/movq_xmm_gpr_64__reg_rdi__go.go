// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of movq_xmm_gpr_64__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Extract(63, 0, v0)
package main

import "unsafe"

//go:noinline
func emu_movq_xmm_gpr_64__reg_rdi__go(a float64) uint64 {
	return uint64(uint64(*(*uint64)(unsafe.Pointer(&a))))
}

var g0 float64
var sink interface{}

func main() {
	sink = emu_movq_xmm_gpr_64__reg_rdi__go(g0)
	_ = sink
}
