// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of and_gpr_gpr_gpr_64__reg_a0__go__native_first.
//   ~(~v0 | ~v1)
package main

//go:noinline
func emu_and_gpr_gpr_gpr_64__reg_a0__go__native_first(a uint64, b uint64) uint64 {
	var v0 uint64 = (uint64(^(uint64(uint64(b)))))
	var v1 uint64 = (uint64(^(uint64(uint64(a)))))
	var v2 uint64 = (uint64((uint64(v1)) | (uint64(v0))))
	var v3 uint64 = (uint64(^(uint64(v2))))
	return uint64(v3)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_and_gpr_gpr_gpr_64__reg_a0__go__native_first(g0, g1)
	_ = sink
}
