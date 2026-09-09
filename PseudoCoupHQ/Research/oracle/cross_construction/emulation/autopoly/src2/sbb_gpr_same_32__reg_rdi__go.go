// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of sbb_gpr_same_32__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(Extract(32, 32, Concat(0, Extract(31, 0, v0)) + Concat(0, Extract(31, 0, v1))) == 1, 1, 0)*4294967295)
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_sbb_gpr_same_32__reg_rdi__go(a uint32, b uint32, c uint64) uint64 {
	return uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint32(sel32(((uint32(((uint32((uint64(((uint64((uint64(((uint64(((uint64(uint32(0x0))) << 32) | (uint64(uint32(b))))) & uint64(0x1ffffffff)))) + (uint64(((uint64(((uint64(uint32(0x0))) << 32) | (uint64(uint32(a))))) & uint64(0x1ffffffff)))))) & uint64(0x1ffffffff)))) >> 32)) & uint32(0x1)))) == (uint32(uint32(0x1)))), uint32(uint32(0x1)), uint32(uint32(0x0))))) * (uint32(uint32(0xffffffff))))))))))
}

var g0 uint32
var g1 uint32
var g2 uint64
var sink interface{}

func main() {
	sink = emu_sbb_gpr_same_32__reg_rdi__go(g0, g1, g2)
	_ = sink
}
