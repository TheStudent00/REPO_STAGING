// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of mul_gpr_gpr_same_64__reg_a0__go__native_first.
//   v0*v0
package main

//go:noinline
func emu_mul_gpr_gpr_same_64__reg_a0__go__native_first(a uint64) uint64 {
	var v0 uint64 = (uint64((uint64(uint64(a))) * (uint64(uint64(a)))))
	return uint64(v0)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_mul_gpr_gpr_same_64__reg_a0__go__native_first(g0)
	_ = sink
}
