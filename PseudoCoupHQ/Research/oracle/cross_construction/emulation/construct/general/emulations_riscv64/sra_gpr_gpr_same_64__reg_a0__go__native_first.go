// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sra_gpr_gpr_same_64__reg_a0__go__native_first.
//   v0 >> Concat(0, Extract(5, 0, v0))
package main

//go:noinline
func emu_sra_gpr_gpr_same_64__reg_a0__go__native_first(a uint64) uint64 {
	var v0 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0x3f))
	var v1 uint64 = (uint64(((uint64(uint64(0x0))) << 6) | (uint64(v0))))
	var v2 uint64 = (uint64(uint64((int64(uint64(a))) >> ((uint64(v1)) & uint64(0x3f)))))
	return uint64(v2)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_sra_gpr_gpr_same_64__reg_a0__go__native_first(g0)
	_ = sink
}
