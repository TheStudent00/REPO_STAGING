// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of div_gpr_gpr_gpr_64__reg_a0__go__native_first.
//   If(v0 == 0, 18446744073709551615, If(And(v0 == 18446744073709551615, v1 == 9223372036854775808), 9223372036854775808, bvsdiv_i(v1, v0)))
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_div_gpr_gpr_gpr_64__reg_a0__go__native_first(a uint64, b uint64) uint64 {
	var v0 uint64 = (uint64(uint64((int64(uint64(b))) / (int64(uint64(a))))))
	var v1 bool = ((uint64(uint64(b))) == (uint64(uint64(0x8000000000000000))))
	var v2 bool = ((uint64(uint64(a))) == (uint64(uint64(0xffffffffffffffff))))
	var v3 bool = ((v2) && (v1))
	var v4 uint64 = sel64(v3, uint64(uint64(0x8000000000000000)), uint64(v0))
	var v5 bool = ((uint64(uint64(a))) == (uint64(uint64(0x0))))
	var v6 uint64 = sel64(v5, uint64(uint64(0xffffffffffffffff)), uint64(v4))
	return uint64(v6)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_div_gpr_gpr_gpr_64__reg_a0__go__native_first(g0, g1)
	_ = sink
}
