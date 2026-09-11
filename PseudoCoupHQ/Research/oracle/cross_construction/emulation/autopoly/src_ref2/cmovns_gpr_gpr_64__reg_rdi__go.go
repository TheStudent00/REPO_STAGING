// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of cmovns_gpr_gpr_64__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   If(Or(Extract(63, 63, v0) == 0, Extract(63, 63, v1) == 0), v2, v3)
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_cmovns_gpr_gpr_64__reg_rdi__go(a uint64, b uint64, c uint64, d uint64) uint64 {
	return uint64(sel64(((((uint32(((uint32((uint64(b)) >> 63)) & uint32(0x1)))) == (uint32(uint32(0x0))))) || (((uint32(((uint32((uint64(a)) >> 63)) & uint32(0x1)))) == (uint32(uint32(0x0)))))), uint64(uint64(c)), uint64(uint64(d))))
}

var g0 uint64
var g1 uint64
var g2 uint64
var g3 uint64
var sink interface{}

func main() {
	sink = emu_cmovns_gpr_gpr_64__reg_rdi__go(g0, g1, g2, g3)
	_ = sink
}
