// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sb_gpr_fpr_fpr_8__mem_MEM_fa1__go__native_first.
//   Concat(Extract(63, 8, v0), Extract(7, 0, v1))
package main

//go:noinline
func emu_sb_gpr_fpr_fpr_8__mem_MEM_fa1__go__native_first(a uint64, b uint8) uint64 {
	var v0 uint32 = uint32(b)
	var v1 uint64 = ((uint64((uint64(a)) >> 8)) & uint64(0xffffffffffffff))
	var v2 uint64 = (uint64(((uint64(v1)) << 8) | (uint64(v0))))
	return uint64(v2)
}

var g0 uint64
var g1 uint8
var sink interface{}

func main() {
	sink = emu_sb_gpr_fpr_fpr_8__mem_MEM_fa1__go__native_first(g0, g1)
	_ = sink
}
