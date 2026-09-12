// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sd_gpr_fpr_64__mem_MEM_fa1__go__all_constructed.
//   v0
package main

//go:noinline
func emu_sd_gpr_fpr_64__mem_MEM_fa1__go__all_constructed(a uint64) uint64 {
	return uint64(uint64(a))
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_sd_gpr_fpr_64__mem_MEM_fa1__go__all_constructed(g0)
	_ = sink
}
