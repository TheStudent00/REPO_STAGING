// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of idiv_gpr_one_32__reg_rax__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, bvsdiv_i(Concat(Extract(31, 0, v0), Extract(31, 0, v1)), Concat(Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 31, v2), Extract(31, 0, v2)))))
package main

//go:noinline
func emu_idiv_gpr_one_32__reg_rax__go(a uint32, b uint32, c uint32) uint64 {
	return uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32((uint64((uint64(uint64((int64((uint64(((uint64(uint32(a))) << 32) | (uint64(uint32(b))))))) / (int64((uint64(((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 63) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 62) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 61) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 60) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 59) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 58) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 57) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 56) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 55) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 54) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 53) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 52) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 51) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 50) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 49) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 48) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 47) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 46) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 45) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 44) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 43) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 42) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 41) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 40) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 39) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 38) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 37) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 36) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 35) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 34) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 33) | ((uint64(((uint32((uint32(c)) >> 31)) & uint32(0x1)))) << 32) | (uint64(uint32(c)))))))))))) >> 0)))))))
}

var g0 uint32
var g1 uint32
var g2 uint32
var sink interface{}

func main() {
	sink = emu_idiv_gpr_one_32__reg_rax__go(g0, g1, g2)
	_ = sink
}
