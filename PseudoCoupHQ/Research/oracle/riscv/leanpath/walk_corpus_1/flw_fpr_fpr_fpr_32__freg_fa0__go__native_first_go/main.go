// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of flw_fpr_fpr_fpr_32__freg_fa0__go__native_first.
//   Concat(4294967295, Extract(31, 0, v0))
package main

//go:noinline
func emu_flw_fpr_fpr_fpr_32__freg_fa0__go__native_first(a uint32) uint64 {
	var v0 uint32 = uint32(a)
	var v1 uint64 = (uint64(((uint64(uint32(0xffffffff))) << 32) | (uint64(v0))))
	return uint64(v1)
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_flw_fpr_fpr_fpr_32__freg_fa0__go__native_first(g0)
	_ = sink
}
