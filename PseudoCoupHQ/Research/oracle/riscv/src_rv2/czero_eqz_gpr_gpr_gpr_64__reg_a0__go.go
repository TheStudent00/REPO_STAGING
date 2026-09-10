// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of czero_eqz_gpr_gpr_gpr_64__reg_a0__go.
// The term's layer-5 text, LITERAL:
//   If(v0 == 0, 0, v1)
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_czero_eqz_gpr_gpr_gpr_64__reg_a0__go(a uint64, b uint64) uint64 {
	return uint64(sel64(((uint64(uint64(a))) == (uint64(uint64(0x0)))), uint64(uint64(0x0)), uint64(uint64(b))))
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_czero_eqz_gpr_gpr_gpr_64__reg_a0__go(g0, g1)
	_ = sink
}
