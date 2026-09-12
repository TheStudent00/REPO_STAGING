// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of sar_cl_gpr_16__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(Extract(63, 16, v0), Extract(15, 0, v0) >> Concat(0, Extract(4, 0, v1)))
package main

//go:noinline
func emu_sar_cl_gpr_16__reg_rdi__go(a uint64, b uint8) uint64 {
	return uint64((uint64(((uint64(((uint64((uint64(a)) >> 16)) & uint64(0xffffffffffff)))) << 16) | (uint64(((uint32(uint32(((int32(((uint32((uint64(a)) >> 0)) & uint32(0xffff))) << 16) >> 16) >> (uint32(((uint32(((uint32(uint32(0x0))) << 5) | (uint32(((uint32((uint32(b)) >> 0)) & uint32(0x1f)))))) & uint32(0xffff))))))) & uint32(0xffff)))))))
}

var g0 uint64
var g1 uint8
var sink interface{}

func main() {
	sink = emu_sar_cl_gpr_16__reg_rdi__go(g0, g1)
	_ = sink
}
