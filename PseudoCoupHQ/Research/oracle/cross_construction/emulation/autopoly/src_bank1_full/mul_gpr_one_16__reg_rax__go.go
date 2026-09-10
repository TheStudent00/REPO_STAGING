// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of mul_gpr_one_16__reg_rax__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), Extract(15, 0, v0)*Extract(15, 0, v1))
package main

//go:noinline
func emu_mul_gpr_one_16__reg_rax__go(a uint64, b uint16) uint64 {
	return uint64((uint64(((uint64(((uint64((uint64(a)) >> 16)) & uint64(0xffffffffffff)))) << 16) | (uint64(((uint32((uint32(((uint32((uint64(a)) >> 0)) & uint32(0xffff)))) * (uint32(uint32(b))))) & uint32(0xffff)))))))
}

var g0 uint64
var g1 uint16
var sink interface{}

func main() {
	sink = emu_mul_gpr_one_16__reg_rax__go(g0, g1)
	_ = sink
}
