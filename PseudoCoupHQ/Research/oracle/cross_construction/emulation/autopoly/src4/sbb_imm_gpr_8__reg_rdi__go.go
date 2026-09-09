// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of sbb_imm_gpr_8__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(Extract(8, 8, Concat(0, Extract(7, 0, v0)) + Concat(0, Extract(7, 0, v1))) == 1, 1, 0)*255 + Extract(7, 0, v2) + 253)
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_sbb_imm_gpr_8__reg_rdi__go(a uint8, b uint8, c uint8) uint64 {
	return uint64((uint64(((uint64(uint64(0x0))) << 8) | (uint64(((uint32((uint32(((uint32((uint32(sel32(((uint32(((uint32((uint32(((uint32((uint32(((uint32(((uint32(uint32(0x0))) << 8) | (uint32(uint32(b))))) & uint32(0x1ff)))) + (uint32(((uint32(((uint32(uint32(0x0))) << 8) | (uint32(uint32(a))))) & uint32(0x1ff)))))) & uint32(0x1ff)))) >> 8)) & uint32(0x1)))) == (uint32(uint32(0x1)))), uint32(uint32(0x1)), uint32(uint32(0x0))))) * (uint32(uint32(0xff))))) & uint32(0xff)))) + (uint32(uint32(c))) + (uint32(uint32(0xfd))))) & uint32(0xff)))))))
}

var g0 uint8
var g1 uint8
var g2 uint8
var sink interface{}

func main() {
	sink = emu_sbb_imm_gpr_8__reg_rdi__go(g0, g1, g2)
	_ = sink
}
