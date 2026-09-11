// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of sbb_gpr_same_64__reg_rdi__go__constructed.
// The term's layer-5 text, LITERAL:
//   If(Extract(64, 64, Concat(0, v0) + Concat(0, v1)) == 1, 1, 0)*18446744073709551615
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_sbb_gpr_same_64__reg_rdi__go__constructed(a uint64, b uint64, c uint64) uint64 {
	return uint64((uint64((uint64(sel64((((uint64(uint64(a)))) <= ((uint64((uint64((uint64(uint64(a))) + (uint64(uint64(b))))))))), uint64(uint64(0x0)), uint64(uint64(0x1))))) * (uint64(uint64(0xffffffffffffffff))))))
}

var g0 uint64
var g1 uint64
var g2 uint64
var sink interface{}

func main() {
	sink = emu_sbb_gpr_same_64__reg_rdi__go__constructed(g0, g1, g2)
	_ = sink
}
