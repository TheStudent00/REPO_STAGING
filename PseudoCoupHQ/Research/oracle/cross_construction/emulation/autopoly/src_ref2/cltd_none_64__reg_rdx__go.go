// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of cltd_none_64__reg_rdx__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, Extract(31, 0, v0) >> 31)
package main

//go:noinline
func emu_cltd_none_64__reg_rdx__go(a uint32) uint64 {
	return uint64((uint64(((uint64(uint32(0x0))) << 32) | (uint64((uint32(uint32((int32(uint32(a))) >> ((uint32(uint32(0x1f))) & uint32(0x1f))))))))))
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_cltd_none_64__reg_rdx__go(g0)
	_ = sink
}
