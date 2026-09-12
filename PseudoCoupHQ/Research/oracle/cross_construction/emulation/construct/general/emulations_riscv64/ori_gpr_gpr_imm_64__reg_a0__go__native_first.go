// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ori_gpr_gpr_imm_64__reg_a0__go__native_first.
//   Concat(Extract(63, 2, v0), 3)
package main

//go:noinline
func emu_ori_gpr_gpr_imm_64__reg_a0__go__native_first(a uint64) uint64 {
	var v0 uint64 = ((uint64((uint64(a)) >> 2)) & uint64(0x3fffffffffffffff))
	var v1 uint64 = (uint64(((uint64(v0)) << 2) | (uint64(uint32(0x3)))))
	return uint64(v1)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_ori_gpr_gpr_imm_64__reg_a0__go__native_first(g0)
	_ = sink
}
