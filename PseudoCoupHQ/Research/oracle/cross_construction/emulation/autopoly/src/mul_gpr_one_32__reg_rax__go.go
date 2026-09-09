// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of mul_gpr_one_32__reg_rax__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0)*Extract(31, 0, v1))
package main

//go:noinline
func emu_mul_gpr_one_32__reg_rax__go(a uint32, b uint32) uint64 {
	return uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint32(uint32(a))) * (uint32(uint32(b))))))))))
}

var g0 uint32
var g1 uint32
var sink interface{}

func main() {
	sink = emu_mul_gpr_one_32__reg_rax__go(g0, g1)
	_ = sink
}
