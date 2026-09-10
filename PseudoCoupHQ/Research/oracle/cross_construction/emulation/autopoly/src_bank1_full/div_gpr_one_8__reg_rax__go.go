// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of div_gpr_one_8__reg_rax__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), Extract(7, 0, bvurem_i(Extract(15, 0, v0), Concat(0, Extract(7, 0, v1)))), Extract(7, 0, bvudiv_i(Extract(15, 0, v0), Concat(0, Extract(7, 0, v1)))))
package main

//go:noinline
func emu_div_gpr_one_8__reg_rax__go(a uint64, b uint8) uint64 {
	return uint64((uint64(((uint64(((uint64((uint64(a)) >> 16)) & uint64(0xffffffffffff)))) << 16) | ((uint64(((uint32((uint32(((uint32((uint32(((uint32((uint64(a)) >> 0)) & uint32(0xffff)))) % (uint32(((uint32(((uint32(uint32(0x0))) << 8) | (uint32(uint32(b))))) & uint32(0xffff)))))) & uint32(0xffff)))) >> 0)) & uint32(0xff)))) << 8) | (uint64(((uint32((uint32(((uint32((uint32(((uint32((uint64(a)) >> 0)) & uint32(0xffff)))) / (uint32(((uint32(((uint32(uint32(0x0))) << 8) | (uint32(uint32(b))))) & uint32(0xffff)))))) & uint32(0xffff)))) >> 0)) & uint32(0xff)))))))
}

var g0 uint64
var g1 uint8
var sink interface{}

func main() {
	sink = emu_div_gpr_one_8__reg_rax__go(g0, g1)
	_ = sink
}
