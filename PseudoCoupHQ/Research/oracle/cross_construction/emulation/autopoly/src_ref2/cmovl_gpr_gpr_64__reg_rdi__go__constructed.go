// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of cmovl_gpr_gpr_64__reg_rdi__go__constructed.
// The term's layer-5 text, LITERAL:
//   If(Extract(63, 63, v0 + 18446744073709551613) == If(Extract(63, 63, Concat(Extract(63, 63, v0), v0) + 36893488147419103229) == Extract(64, 64, Concat(Extract(63, 63, v0), v0) + 36893488147419103229), 1, 0), v1, v2)
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_cmovl_gpr_gpr_64__reg_rdi__go__constructed(a uint64, b uint64, c uint64) uint64 {
	return uint64(sel64(((uint32(((uint32((uint64((uint64((uint64(uint64(a))) + (uint64(uint64(0xfffffffffffffffd))))))) >> 63)) & uint32(0x1)))) == (uint32(sel32(((uint32(((uint32((uint32(((uint32((uint64(a)) >> 63)) & uint32(0x1)))) + (uint32(sel32(((((uint32(((uint32((uint64(a)) >> 0)) & uint32(0x3)))) == (uint32(uint32(0x3))))) || ((!(((uint64(((uint64((uint64(a)) >> 2)) & uint64(0x3fffffffffffffff)))) == (uint64(uint64(0x0)))))))), uint32(uint32(0x0)), uint32(uint32(0x1))))))) & uint32(0x1)))) == (uint32(((uint32((uint64((uint64((uint64(uint64(a))) + (uint64(uint64(0xfffffffffffffffd))))))) >> 63)) & uint32(0x1))))), uint32(uint32(0x1)), uint32(uint32(0x0)))))), uint64(uint64(b)), uint64(uint64(c))))
}

var g0 uint64
var g1 uint64
var g2 uint64
var sink interface{}

func main() {
	sink = emu_cmovl_gpr_gpr_64__reg_rdi__go__constructed(g0, g1, g2)
	_ = sink
}
