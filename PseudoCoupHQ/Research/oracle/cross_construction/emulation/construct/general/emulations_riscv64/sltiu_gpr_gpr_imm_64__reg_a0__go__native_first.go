// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sltiu_gpr_gpr_imm_64__reg_a0__go__native_first.
//   If(Or(Extract(1, 0, v0) == 3, Not(Extract(63, 2, v0) == 0)), 0, 1)
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_sltiu_gpr_gpr_imm_64__reg_a0__go__native_first(a uint64) uint64 {
	var v0 uint64 = ((uint64((uint64(a)) >> 2)) & uint64(0x3fffffffffffffff))
	var v1 bool = ((uint64(v0)) == (uint64(uint64(0x0))))
	var v2 bool = (!(v1))
	var v3 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0x3))
	var v4 bool = ((uint32(v3)) == (uint32(uint32(0x3))))
	var v5 bool = ((v4) || (v2))
	var v6 uint64 = sel64(v5, uint64(uint64(0x0)), uint64(uint64(0x1)))
	return uint64(v6)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_sltiu_gpr_gpr_imm_64__reg_a0__go__native_first(g0)
	_ = sink
}
