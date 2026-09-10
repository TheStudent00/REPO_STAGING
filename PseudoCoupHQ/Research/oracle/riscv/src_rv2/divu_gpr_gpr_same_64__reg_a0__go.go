// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of divu_gpr_gpr_same_64__reg_a0__go.
// The term's layer-5 text, LITERAL:
//   If(v0 == 0, 18446744073709551615, bvudiv_i(v0, v0))
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_divu_gpr_gpr_same_64__reg_a0__go(a uint64) uint64 {
	return uint64(sel64(((uint64(uint64(a))) == (uint64(uint64(0x0)))), uint64(uint64(0xffffffffffffffff)), uint64((uint64((uint64(uint64(a))) / (uint64(uint64(a))))))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_divu_gpr_gpr_same_64__reg_a0__go(g0)
	_ = sink
}
