// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of lea_lea_mem_32__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   v0 + v1
package main

//go:noinline
func emu_lea_lea_mem_32__reg_rdi__go(a uint64, b uint64) uint64 {
	return uint64((uint64((uint64(uint64(b))) + (uint64(uint64(a))))))
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_lea_lea_mem_32__reg_rdi__go(g0, g1)
	_ = sink
}
