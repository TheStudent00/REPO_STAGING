// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sw_gpr_gpr_same_32__mem_MEM_a1__go__all_constructed.
//   Concat(Extract(63, 32, v0), Extract(31, 0, v1))
package main

//go:noinline
func emu_sw_gpr_gpr_same_32__mem_MEM_a1__go__all_constructed(a uint64, b uint32) uint64 {
	var v0 uint32 = uint32(b)
	var v1 uint32 = (uint32((uint64(a)) >> 32))
	var v2 uint32 = v0
	var v3 uint32 = v1
	var v4 uint64 = (uint64(((uint64(v3)) << 32) | (uint64(v2))))
	return uint64(v4)
}

var g0 uint64
var g1 uint32
var sink interface{}

func main() {
	sink = emu_sw_gpr_gpr_same_32__mem_MEM_a1__go__all_constructed(g0, g1)
	_ = sink
}
