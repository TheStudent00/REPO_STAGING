// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of mul_gpr_one_64__reg_rdx__go__constructed.
// The term's layer-5 text, LITERAL:
//   Extract(127, 64, Concat(0, v0)*Concat(0, v1))
package main

//go:noinline
func emu_mul_gpr_one_64__reg_rdx__go__constructed(a uint64, b uint64) uint64 {
	return uint64((uint64((uint64((uint64((uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64(a)) >> 32)))))))) * (uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64(b)) >> 32)))))))))))) + (uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64((uint64((uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint32((uint32((uint64(a)) >> 0)))) * (uint32((uint32((uint64(b)) >> 32)))))))))))) + (uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint32((uint32((uint64(b)) >> 0)))) * (uint32((uint32((uint64(a)) >> 32)))))))))))) + (uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64((uint64((uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64(a)) >> 0)))))))) * (uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64(b)) >> 0)))))))))))) >> 32)))))))))))) >> 32)))))))) + (uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64((uint64((uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64(a)) >> 0)))))))) * (uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64(b)) >> 32)))))))))))) >> 32)))))))) + (uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64((uint64((uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64(b)) >> 0)))))))) * (uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64(a)) >> 32)))))))))))) >> 32)))))))))))
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_mul_gpr_one_64__reg_rdx__go__constructed(g0, g1)
	_ = sink
}
