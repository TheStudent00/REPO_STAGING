// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sh_gpr_gpr_gpr_16__mem_MEM_a1__go__native_first.
//   Concat(Extract(63, 16, v0), Extract(15, 0, v1))
package main

//go:noinline
func emu_sh_gpr_gpr_gpr_16__mem_MEM_a1__go__native_first(a uint64, b uint16) uint64 {
	var v0 uint32 = uint32(b)
	var v1 uint64 = ((uint64((uint64(a)) >> 16)) & uint64(0xffffffffffff))
	var v2 uint64 = (uint64(((uint64(v1)) << 16) | (uint64(v0))))
	return uint64(v2)
}

var g0 uint64
var g1 uint16
var sink interface{}

func main() {
	sink = emu_sh_gpr_gpr_gpr_16__mem_MEM_a1__go__native_first(g0, g1)
	_ = sink
}
