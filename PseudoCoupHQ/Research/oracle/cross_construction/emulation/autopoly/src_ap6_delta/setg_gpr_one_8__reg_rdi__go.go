// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of setg_gpr_one_8__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(~(~Extract(7, 0, v0) | ~Extract(7, 0, v1)) <= 0, 0, 1))
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_setg_gpr_one_8__reg_rdi__go(a uint8, b uint8) uint64 {
	return uint64((uint64(((uint64(uint64(0x0))) << 8) | (uint64(sel32(((((int32(((uint32(^(uint32(((uint32((uint32(((uint32(^(uint32(uint32(b))))) & uint32(0xff)))) | (uint32(((uint32(^(uint32(uint32(a))))) & uint32(0xff)))))) & uint32(0xff)))))) & uint32(0xff))) << 24) >> 24)) <= (((int32(uint32(0x0)) << 24) >> 24))), uint32(uint32(0x0)), uint32(uint32(0x1))))))))
}

var g0 uint8
var g1 uint8
var sink interface{}

func main() {
	sink = emu_setg_gpr_one_8__reg_rdi__go(g0, g1)
	_ = sink
}
