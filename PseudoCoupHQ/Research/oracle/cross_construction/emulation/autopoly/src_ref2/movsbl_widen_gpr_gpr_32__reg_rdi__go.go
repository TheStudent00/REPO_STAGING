// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of movsbl_widen_gpr_gpr_32__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 0, v0))
package main

//go:noinline
func emu_movsbl_widen_gpr_gpr_32__reg_rdi__go(a uint8) uint64 {
	return uint64((uint64(((uint64(uint32(0x0))) << 32) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 31) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 30) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 29) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 28) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 27) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 26) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 25) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 24) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 23) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 22) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 21) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 20) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 19) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 18) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 17) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 16) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 15) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 14) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 13) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 12) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 11) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 10) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 9) | ((uint64(((uint32((uint32(a)) >> 7)) & uint32(0x1)))) << 8) | (uint64(uint32(a))))))
}

var g0 uint8
var sink interface{}

func main() {
	sink = emu_movsbl_widen_gpr_gpr_32__reg_rdi__go(g0)
	_ = sink
}
