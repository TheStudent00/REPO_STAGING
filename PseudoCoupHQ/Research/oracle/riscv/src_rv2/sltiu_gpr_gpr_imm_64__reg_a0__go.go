// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of sltiu_gpr_gpr_imm_64__reg_a0__go.
// The term's layer-5 text, LITERAL:
//   If(Or(Extract(1, 0, v0) == 3, Not(Extract(63, 2, v0) == 0)), 0, 1)
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_sltiu_gpr_gpr_imm_64__reg_a0__go(a uint64) uint64 {
	return uint64(sel64(((((uint32(((uint32((uint64(a)) >> 0)) & uint32(0x3)))) == (uint32(uint32(0x3))))) || ((!(((uint64(((uint64((uint64(a)) >> 2)) & uint64(0x3fffffffffffffff)))) == (uint64(uint64(0x0)))))))), uint64(uint64(0x0)), uint64(uint64(0x1))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_sltiu_gpr_gpr_imm_64__reg_a0__go(g0)
	_ = sink
}
