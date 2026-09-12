// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of neg_gpr_one_16__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), Extract(15, 0, v0)*65535)
package main

//go:noinline
func emu_neg_gpr_one_16__reg_rdi__go(a uint64) uint64 {
	return uint64((uint64(((uint64(((uint64((uint64(a)) >> 16)) & uint64(0xffffffffffff)))) << 16) | (uint64(((uint32((uint32(((uint32((uint64(a)) >> 0)) & uint32(0xffff)))) * (uint32(uint32(0xffff))))) & uint32(0xffff)))))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_neg_gpr_one_16__reg_rdi__go(g0)
	_ = sink
}
