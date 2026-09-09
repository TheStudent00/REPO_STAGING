// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of idiv_gpr_one_16__reg_rax__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v1), Extract(15, 0, bvsdiv_i(Concat(Extract(15, 0, v0), Extract(15, 0, v1)), Concat(Extract(15, 15, v2), Extract(15, 15, v2), Extract(15, 15, v2), Extract(15, 15, v2), Extract(15, 15, v2), Extract(15, 15, v2), Extract(15, 15, v2), Extract(15, 15, v2), Extract(15, 15, v2), Extract(15, 15, v2), Extract(15, 15, v2), Extract(15, 15, v2), Extract(15, 15, v2), Extract(15, 15, v2), Extract(15, 15, v2), Extract(15, 15, v2), Extract(15, 0, v2)))))
package main

//go:noinline
func emu_idiv_gpr_one_16__reg_rax__go(a uint16, b uint64, c uint16) uint64 {
	return uint64((uint64(((uint64(((uint64((uint64(b)) >> 16)) & uint64(0xffffffffffff)))) << 16) | (uint64(((uint32((uint32((uint32(uint32((int32((uint32(((uint32(uint32(a))) << 16) | (uint32(((uint32((uint64(b)) >> 0)) & uint32(0xffff)))))))) / (int32((uint32(((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 31) | ((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 30) | ((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 29) | ((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 28) | ((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 27) | ((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 26) | ((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 25) | ((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 24) | ((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 23) | ((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 22) | ((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 21) | ((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 20) | ((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 19) | ((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 18) | ((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 17) | ((uint32(((uint32((uint32(c)) >> 15)) & uint32(0x1)))) << 16) | (uint32(uint32(c)))))))))))) >> 0)) & uint32(0xffff)))))))
}

var g0 uint16
var g1 uint64
var g2 uint16
var sink interface{}

func main() {
	sink = emu_idiv_gpr_one_16__reg_rax__go(g0, g1, g2)
	_ = sink
}
