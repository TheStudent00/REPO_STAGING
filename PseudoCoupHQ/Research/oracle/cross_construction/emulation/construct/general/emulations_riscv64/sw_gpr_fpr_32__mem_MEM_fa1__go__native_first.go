// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sw_gpr_fpr_32__mem_MEM_fa1__go__native_first.
//   Concat(Extract(63, 32, v0), Extract(31, 0, v1))
package main

//go:noinline
func emu_sw_gpr_fpr_32__mem_MEM_fa1__go__native_first(a uint64, b uint32) uint64 {
	var v0 uint32 = uint32(b)
	var v1 uint32 = (uint32((uint64(a)) >> 32))
	var v2 uint64 = (uint64(((uint64(v1)) << 32) | (uint64(v0))))
	return uint64(v2)
}

var g0 uint64
var g1 uint32
var sink interface{}

func main() {
	sink = emu_sw_gpr_fpr_32__mem_MEM_fa1__go__native_first(g0, g1)
	_ = sink
}
