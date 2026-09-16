// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sub_gpr_gpr_gpr_64__reg_a0__go__native_first.
//   v0*18446744073709551615 + v1
package main

//go:noinline
func emu_sub_gpr_gpr_gpr_64__reg_a0__go__native_first(a uint64, b uint64) uint64 {
	var v0 uint64 = (uint64((uint64(uint64(b))) * (uint64(uint64(0xffffffffffffffff)))))
	var v1 uint64 = (uint64((uint64(v0)) + (uint64(uint64(a)))))
	return uint64(v1)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_sub_gpr_gpr_gpr_64__reg_a0__go__native_first(g0, g1)
	_ = sink
}
