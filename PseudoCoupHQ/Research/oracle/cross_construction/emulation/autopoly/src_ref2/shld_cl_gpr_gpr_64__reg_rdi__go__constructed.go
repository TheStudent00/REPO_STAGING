// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of shld_cl_gpr_gpr_64__reg_rdi__go__constructed.
// The term's layer-5 text, LITERAL:
//   Extract(127, 64, Concat(v0, v1) << Concat(0, Extract(5, 0, v2)))
package main

//go:noinline
func emu_shld_cl_gpr_gpr_64__reg_rdi__go__constructed(a uint64, b uint64, c uint8) uint64 {
	return uint64((uint64((uint64((uint64((uint64(uint64(b))) >> (uint64((uint64((uint64((uint64((uint64((uint64(((uint64(uint64(0x0))) << 6) | (uint64(((uint32((uint32(c)) >> 0)) & uint32(0x3f)))))))) * (uint64(uint64(0xffffffffffffffff))))))) + (uint64(uint64(0x40))))))))))) | (uint64((uint64((uint64(uint64(a))) << ((uint64((uint64(((uint64(uint64(0x0))) << 6) | (uint64(((uint32((uint32(c)) >> 0)) & uint32(0x3f)))))))) & uint64(0x3f)))))))))
}

var g0 uint64
var g1 uint64
var g2 uint8
var sink interface{}

func main() {
	sink = emu_shld_cl_gpr_gpr_64__reg_rdi__go__constructed(g0, g1, g2)
	_ = sink
}
