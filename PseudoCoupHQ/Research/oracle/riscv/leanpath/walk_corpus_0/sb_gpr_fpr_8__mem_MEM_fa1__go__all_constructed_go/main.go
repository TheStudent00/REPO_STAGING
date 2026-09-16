// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sb_gpr_fpr_8__mem_MEM_fa1__go__all_constructed.
//   Concat(Extract(63, 8, v0), Extract(7, 0, v1))
package main

//go:noinline
func emu_sb_gpr_fpr_8__mem_MEM_fa1__go__all_constructed(a uint64, b uint8) uint64 {
	var v0 uint32 = uint32(b)
	var v1 uint64 = ((uint64((uint64(a)) >> 8)) & uint64(0xffffffffffffff))
	var v2 uint32 = v0
	var v3 uint64 = v1
	var v4 uint64 = (uint64(((uint64(v3)) << 8) | (uint64(v2))))
	return uint64(v4)
}

var g0 uint64
var g1 uint8
var sink interface{}

func main() {
	sink = emu_sb_gpr_fpr_8__mem_MEM_fa1__go__all_constructed(g0, g1)
	_ = sink
}
