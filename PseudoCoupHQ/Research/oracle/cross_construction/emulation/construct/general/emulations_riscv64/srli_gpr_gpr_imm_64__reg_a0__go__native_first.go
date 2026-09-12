// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of srli_gpr_gpr_imm_64__reg_a0__go__native_first.
//   Concat(0, Extract(63, 3, v0))
package main

//go:noinline
func emu_srli_gpr_gpr_imm_64__reg_a0__go__native_first(a uint64) uint64 {
	var v0 uint64 = ((uint64((uint64(a)) >> 3)) & uint64(0x1fffffffffffffff))
	var v1 uint64 = (uint64(((uint64(uint32(0x0))) << 61) | (uint64(v0))))
	return uint64(v1)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_srli_gpr_gpr_imm_64__reg_a0__go__native_first(g0)
	_ = sink
}
