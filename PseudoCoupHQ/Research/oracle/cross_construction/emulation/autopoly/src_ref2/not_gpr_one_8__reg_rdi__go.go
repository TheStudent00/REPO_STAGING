// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of not_gpr_one_8__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 8, v0), ~Extract(7, 0, v0))
package main

//go:noinline
func emu_not_gpr_one_8__reg_rdi__go(a uint64) uint64 {
	return uint64((uint64(((uint64(((uint64((uint64(a)) >> 8)) & uint64(0xffffffffffffff)))) << 8) | (uint64(((uint32(^(uint32(((uint32((uint64(a)) >> 0)) & uint32(0xff)))))) & uint32(0xff)))))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_not_gpr_one_8__reg_rdi__go(g0)
	_ = sink
}
