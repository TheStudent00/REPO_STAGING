// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of cwtl_none_64__reg_rax__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 15, v0), Extract(15, 0, v0))
package main

//go:noinline
func emu_cwtl_none_64__reg_rax__go(a uint16) uint64 {
	return uint64((uint64(((uint64(uint32(0x0))) << 32) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 31) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 30) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 29) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 28) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 27) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 26) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 25) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 24) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 23) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 22) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 21) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 20) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 19) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 18) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 17) | ((uint64(((uint32((uint32(a)) >> 15)) & uint32(0x1)))) << 16) | (uint64(uint32(a))))))
}

var g0 uint16
var sink interface{}

func main() {
	sink = emu_cwtl_none_64__reg_rax__go(g0)
	_ = sink
}
