// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of sra_gpr_gpr_same_64__reg_a0__go.
// The term's layer-5 text, LITERAL:
//   v0 >> Concat(0, Extract(5, 0, v0))
package main

//go:noinline
func emu_sra_gpr_gpr_same_64__reg_a0__go(a uint64) uint64 {
	return uint64((uint64(uint64((int64(uint64(a))) >> ((uint64((uint64(((uint64(uint64(0x0))) << 6) | (uint64(((uint32((uint64(a)) >> 0)) & uint32(0x3f)))))))) & uint64(0x3f))))))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_sra_gpr_gpr_same_64__reg_a0__go(g0)
	_ = sink
}
