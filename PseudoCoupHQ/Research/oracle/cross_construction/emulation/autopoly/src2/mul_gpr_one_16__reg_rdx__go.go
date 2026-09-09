// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of mul_gpr_one_16__reg_rdx__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v2), Extract(31, 16, Concat(0, Extract(15, 0, v0))*Concat(0, Extract(15, 0, v1))))
package main

//go:noinline
func emu_mul_gpr_one_16__reg_rdx__go(a uint16, b uint16, c uint64) uint64 {
	return uint64((uint64(((uint64(((uint64((uint64(c)) >> 16)) & uint64(0xffffffffffff)))) << 16) | (uint64(((uint32((uint32((uint32((uint32((uint32(((uint32(uint32(0x0))) << 16) | (uint32(uint32(a))))))) * (uint32((uint32(((uint32(uint32(0x0))) << 16) | (uint32(uint32(b))))))))))) >> 16)) & uint32(0xffff)))))))
}

var g0 uint16
var g1 uint16
var g2 uint64
var sink interface{}

func main() {
	sink = emu_mul_gpr_one_16__reg_rdx__go(g0, g1, g2)
	_ = sink
}
