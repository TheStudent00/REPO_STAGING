// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of idiv_gpr_one_8__reg_rax__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v1), Extract(7, 0, bvsrem_i(Extract(15, 0, v1), Concat(Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 0, v0)))), Extract(7, 0, bvsdiv_i(Extract(15, 0, v1), Concat(Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 0, v0)))))
package main

//go:noinline
func emu_idiv_gpr_one_8__reg_rax__go(a uint64, b uint8) uint64 {
	return uint64((uint64(((uint64(((uint64((uint64(a)) >> 16)) & uint64(0xffffffffffff)))) << 16) | ((uint64(((uint32((uint32(((uint32(uint32(((int32(((uint32((uint64(a)) >> 0)) & uint32(0xffff))) << 16) >> 16) % ((int32(((uint32(((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 15) | ((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 14) | ((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 13) | ((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 12) | ((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 11) | ((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 10) | ((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 9) | ((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 8) | (uint32(uint32(b))))) & uint32(0xffff))) << 16) >> 16)))) & uint32(0xffff)))) >> 0)) & uint32(0xff)))) << 8) | (uint64(((uint32((uint32(((uint32(uint32(((int32(((uint32((uint64(a)) >> 0)) & uint32(0xffff))) << 16) >> 16) / ((int32(((uint32(((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 15) | ((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 14) | ((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 13) | ((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 12) | ((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 11) | ((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 10) | ((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 9) | ((uint32(((uint32((uint32(b)) >> 7)) & uint32(0x1)))) << 8) | (uint32(uint32(b))))) & uint32(0xffff))) << 16) >> 16)))) & uint32(0xffff)))) >> 0)) & uint32(0xff)))))))
}

var g0 uint64
var g1 uint8
var sink interface{}

func main() {
	sink = emu_idiv_gpr_one_8__reg_rax__go(g0, g1)
	_ = sink
}
