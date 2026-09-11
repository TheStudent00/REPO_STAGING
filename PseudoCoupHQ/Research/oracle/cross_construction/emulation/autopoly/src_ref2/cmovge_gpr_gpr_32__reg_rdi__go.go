// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of cmovge_gpr_gpr_32__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(Extract(31, 31, Extract(31, 0, v0)*4294967295 + Extract(31, 0, v1)) == If(Extract(31, 31, Concat(Extract(31, 31, v0), Extract(31, 0, v0))*8589934591 + Concat(Extract(31, 31, v1), Extract(31, 0, v1))) == Extract(32, 32, Concat(Extract(31, 31, v0), Extract(31, 0, v0))*8589934591 + Concat(Extract(31, 31, v1), Extract(31, 0, v1))), 0, 1), Extract(31, 0, v2), Extract(31, 0, v3)))
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_cmovge_gpr_gpr_32__reg_rdi__go(a uint32, b uint32, c uint32, d uint32) uint64 {
	return uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64(sel32(((uint32(((uint32((uint32((uint32((uint32((uint32((uint32(uint32(b))) * (uint32(uint32(0xffffffff))))))) + (uint32(uint32(a))))))) >> 31)) & uint32(0x1)))) == (uint32(sel32(((uint32(((uint32((uint64(((uint64((uint64(((uint64((uint64(((uint64(((uint64(((uint32((uint32(b)) >> 31)) & uint32(0x1)))) << 32) | (uint64(uint32(b))))) & uint64(0x1ffffffff)))) * (uint64(uint64(0x1ffffffff))))) & uint64(0x1ffffffff)))) + (uint64(((uint64(((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 32) | (uint64(uint32(a))))) & uint64(0x1ffffffff)))))) & uint64(0x1ffffffff)))) >> 31)) & uint32(0x1)))) == (uint32(((uint32((uint64(((uint64((uint64(((uint64((uint64(((uint64(((uint64(((uint32((uint32(b)) >> 31)) & uint32(0x1)))) << 32) | (uint64(uint32(b))))) & uint64(0x1ffffffff)))) * (uint64(uint64(0x1ffffffff))))) & uint64(0x1ffffffff)))) + (uint64(((uint64(((uint64(((uint32((uint32(a)) >> 31)) & uint32(0x1)))) << 32) | (uint64(uint32(a))))) & uint64(0x1ffffffff)))))) & uint64(0x1ffffffff)))) >> 32)) & uint32(0x1))))), uint32(uint32(0x0)), uint32(uint32(0x1)))))), uint32(uint32(c)), uint32(uint32(d))))))))
}

var g0 uint32
var g1 uint32
var g2 uint32
var g3 uint32
var sink interface{}

func main() {
	sink = emu_cmovge_gpr_gpr_32__reg_rdi__go(g0, g1, g2, g3)
	_ = sink
}
