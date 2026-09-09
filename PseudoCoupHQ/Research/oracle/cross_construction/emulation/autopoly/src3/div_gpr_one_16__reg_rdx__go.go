// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of div_gpr_one_16__reg_rdx__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), Extract(15, 0, bvurem_i(Concat(Extract(15, 0, v0), Extract(15, 0, v1)), Concat(0, Extract(15, 0, v2)))))
package main

//go:noinline
func emu_div_gpr_one_16__reg_rdx__go(a uint64, b uint16, c uint16) uint64 {
	return uint64((uint64(((uint64(((uint64((uint64(a)) >> 16)) & uint64(0xffffffffffff)))) << 16) | (uint64(((uint32((uint32((uint32((uint32((uint32(((uint32(((uint32((uint64(a)) >> 0)) & uint32(0xffff)))) << 16) | (uint32(uint32(b))))))) % (uint32((uint32(((uint32(uint32(0x0))) << 16) | (uint32(uint32(c))))))))))) >> 0)) & uint32(0xffff)))))))
}

var g0 uint64
var g1 uint16
var g2 uint16
var sink interface{}

func main() {
	sink = emu_div_gpr_one_16__reg_rdx__go(g0, g1, g2)
	_ = sink
}
