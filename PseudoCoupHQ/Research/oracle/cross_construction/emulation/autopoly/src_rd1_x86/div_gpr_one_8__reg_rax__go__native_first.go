// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of div_gpr_one_8__reg_rax__go__native_first.
//   Concat(Extract(63, 16, v0), Extract(7, 0, bvurem_i(Extract(15, 0, v0), Concat(0, Extract(7, 0, v1)))), Extract(7, 0, bvudiv_i(Extract(15, 0, v0), Concat(0, Extract(7, 0, v1)))))
package main

//go:noinline
func emu_div_gpr_one_8__reg_rax__go__native_first(a uint64, b uint8) uint64 {
	var v0 uint32 = uint32(b)
	var v1 uint32 = ((uint32(((uint32(uint32(0x0))) << 8) | (uint32(v0)))) & uint32(0xffff))
	var v2 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0xffff))
	var v3 uint32 = ((uint32((uint32(v2)) / (uint32(v1)))) & uint32(0xffff))
	var v4 uint32 = ((uint32((uint32(v3)) >> 0)) & uint32(0xff))
	var v5 uint32 = ((uint32((uint32(v2)) % (uint32(v1)))) & uint32(0xffff))
	var v6 uint32 = ((uint32((uint32(v5)) >> 0)) & uint32(0xff))
	var v7 uint64 = ((uint64((uint64(a)) >> 16)) & uint64(0xffffffffffff))
	var v8 uint64 = (uint64(((uint64(v7)) << 16) | ((uint64(v6)) << 8) | (uint64(v4))))
	return uint64(v8)
}

var g0 uint64
var g1 uint8
var sink interface{}

func main() {
	sink = emu_div_gpr_one_8__reg_rax__go__native_first(g0, g1)
	_ = sink
}
