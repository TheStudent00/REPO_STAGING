// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of movslq_widen_gpr_gpr_64__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 0, v0))
package main

//go:noinline
func emu_movslq_widen_gpr_gpr_64__reg_rdi__go(a uint32) uint64 {
	return uint64((uint64(((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 63) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 62) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 61) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 60) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 59) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 58) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 57) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 56) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 55) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 54) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 53) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 52) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 51) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 50) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 49) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 48) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 47) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 46) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 45) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 44) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 43) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 42) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 41) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 40) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 39) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 38) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 37) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 36) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 35) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 34) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 33) | ((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 32) | (uint64(uint32(a))))))
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_movslq_widen_gpr_gpr_64__reg_rdi__go(g0)
	_ = sink
}
