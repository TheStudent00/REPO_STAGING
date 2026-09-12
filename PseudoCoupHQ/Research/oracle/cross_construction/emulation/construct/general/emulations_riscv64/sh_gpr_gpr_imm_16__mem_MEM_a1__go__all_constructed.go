// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sh_gpr_gpr_imm_16__mem_MEM_a1__go__all_constructed.
//   Concat(Extract(63, 16, v0), Extract(15, 0, v1))
package main

//go:noinline
func emu_sh_gpr_gpr_imm_16__mem_MEM_a1__go__all_constructed(a uint64, b uint16) uint64 {
	var v0 uint32 = uint32(b)
	var v1 uint64 = ((uint64((uint64(a)) >> 16)) & uint64(0xffffffffffff))
	var v2 uint32 = v0
	var v3 uint64 = v1
	var v4 uint64 = (uint64(((uint64(v3)) << 16) | (uint64(v2))))
	return uint64(v4)
}

var g0 uint64
var g1 uint16
var sink interface{}

func main() {
	sink = emu_sh_gpr_gpr_imm_16__mem_MEM_a1__go__all_constructed(g0, g1)
	_ = sink
}
