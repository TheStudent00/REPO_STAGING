// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of div_gpr_one_32__reg_rax__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, bvudiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(0, Extract(31, 0, v2)))))
package main

//go:noinline
func emu_div_gpr_one_32__reg_rax__go(a uint32, b uint32, c uint32) uint64 {
	return uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64((uint64((uint64((uint64(((uint64(uint32(a))) << 32) | (uint64(uint32(b))))))) / (uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64(uint32(c))))))))))) >> 0)))))))
}

var g0 uint32
var g1 uint32
var g2 uint32
var sink interface{}

func main() {
	sink = emu_div_gpr_one_32__reg_rax__go(g0, g1, g2)
	_ = sink
}
