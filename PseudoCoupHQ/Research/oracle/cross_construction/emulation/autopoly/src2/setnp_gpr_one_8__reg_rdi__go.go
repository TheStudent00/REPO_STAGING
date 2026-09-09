// task g1 emulation -- rendered by go_render.py
// GoRenderer from the layer-4 term of setnp_gpr_one_8__reg_rdi__go.
// The term's layer-5 text, LITERAL:
//   Concat(0, If(Extract(1, 1, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(2, 2, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(3, 3, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(4, 4, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(5, 5, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(6, 6, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(7, 7, Extract(7, 0, v0)*255 + Extract(7, 0, v1)) == If(Extract(0, 0, v1) + 1 == Extract(0, 0, v0), 1, 0), 1, 0), 1, 0), 1, 0), 1, 0), 1, 0), 1, 0), 0, 1))
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_setnp_gpr_one_8__reg_rdi__go(a uint8, b uint8) uint64 {
	return uint64((uint64(((uint64(uint64(0x0))) << 8) | (uint64(sel32(((uint32(((uint32((uint32(((uint32((uint32(((uint32((uint32(uint32(b))) * (uint32(uint32(0xff))))) & uint32(0xff)))) + (uint32(uint32(a))))) & uint32(0xff)))) >> 1)) & uint32(0x1)))) == (uint32(sel32(((uint32(((uint32((uint32(((uint32((uint32(((uint32((uint32(uint32(b))) * (uint32(uint32(0xff))))) & uint32(0xff)))) + (uint32(uint32(a))))) & uint32(0xff)))) >> 2)) & uint32(0x1)))) == (uint32(sel32(((uint32(((uint32((uint32(((uint32((uint32(((uint32((uint32(uint32(b))) * (uint32(uint32(0xff))))) & uint32(0xff)))) + (uint32(uint32(a))))) & uint32(0xff)))) >> 3)) & uint32(0x1)))) == (uint32(sel32(((uint32(((uint32((uint32(((uint32((uint32(((uint32((uint32(uint32(b))) * (uint32(uint32(0xff))))) & uint32(0xff)))) + (uint32(uint32(a))))) & uint32(0xff)))) >> 4)) & uint32(0x1)))) == (uint32(sel32(((uint32(((uint32((uint32(((uint32((uint32(((uint32((uint32(uint32(b))) * (uint32(uint32(0xff))))) & uint32(0xff)))) + (uint32(uint32(a))))) & uint32(0xff)))) >> 5)) & uint32(0x1)))) == (uint32(sel32(((uint32(((uint32((uint32(((uint32((uint32(((uint32((uint32(uint32(b))) * (uint32(uint32(0xff))))) & uint32(0xff)))) + (uint32(uint32(a))))) & uint32(0xff)))) >> 6)) & uint32(0x1)))) == (uint32(sel32(((uint32(((uint32((uint32(((uint32((uint32(((uint32((uint32(uint32(b))) * (uint32(uint32(0xff))))) & uint32(0xff)))) + (uint32(uint32(a))))) & uint32(0xff)))) >> 7)) & uint32(0x1)))) == (uint32(sel32(((uint32(((uint32((uint32(((uint32((uint32(a)) >> 0)) & uint32(0x1)))) + (uint32(uint32(0x1))))) & uint32(0x1)))) == (uint32(((uint32((uint32(b)) >> 0)) & uint32(0x1))))), uint32(uint32(0x1)), uint32(uint32(0x0)))))), uint32(uint32(0x1)), uint32(uint32(0x0)))))), uint32(uint32(0x1)), uint32(uint32(0x0)))))), uint32(uint32(0x1)), uint32(uint32(0x0)))))), uint32(uint32(0x1)), uint32(uint32(0x0)))))), uint32(uint32(0x1)), uint32(uint32(0x0)))))), uint32(uint32(0x1)), uint32(uint32(0x0)))))), uint32(uint32(0x0)), uint32(uint32(0x1))))))))
}

var g0 uint8
var g1 uint8
var sink interface{}

func main() {
	sink = emu_setnp_gpr_one_8__reg_rdi__go(g0, g1)
	_ = sink
}
