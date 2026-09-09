// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of shl_cl_gpr_64__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   v0 << Concat(0, Extract(5, 0, v1))
package main

//go:noinline
func emu_shl_cl_gpr_64__reg_rdi__go(a uint64, b uint8) uint64 {
	return uint64((uint64((uint64(uint64(a))) << ((uint64((uint64(((uint64(uint64(0x0))) << 6) | (uint64(((uint32((uint32(b)) >> 0)) & uint32(0x3f)))))))) & uint64(0x3f)))))
}

var g0 uint64
var g1 uint8
var sink interface{}

func main() {
	sink = emu_shl_cl_gpr_64__reg_rdi__go(g0, g1)
	_ = sink
}
