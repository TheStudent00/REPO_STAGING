// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of divw_gpr_gpr_same_32__reg_a0__go__native_first.
//   Concat(If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v0), Extract(31, 0, v0)))), If(Or(Extract
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_divw_gpr_gpr_same_32__reg_a0__go__native_first(a uint32) uint64 {
	var v0 uint32 = uint32(a)
	var v1 uint32 = (uint32(uint32((int32(v0)) / (int32(v0)))))
	var v2 bool = ((uint32(v0)) == (uint32(uint32(0xffffffff))))
	var v3 bool = ((uint32(v0)) == (uint32(uint32(0x80000000))))
	var v4 bool = ((v3) && (v2))
	var v5 uint32 = sel32(v4, uint32(uint32(0x80000000)), uint32(v1))
	var v6 bool = ((uint32(v0)) == (uint32(uint32(0x0))))
	var v7 uint32 = sel32(v6, uint32(uint32(0xffffffff)), uint32(v5))
	var v8 uint32 = ((uint32((uint32(v1)) >> 31)) & uint32(0x1))
	var v9 bool = ((v6) || (v4))
	var v10 uint32 = sel32(v9, uint32(uint32(0x1)), uint32(v8))
	var v11 uint64 = (uint64(((uint64(v10)) << 63) | ((uint64(v10)) << 62) | ((uint64(v10)) << 61) | ((uint64(v10)) << 60) | ((uint64(v10)) << 59) | ((uint64(v10)) << 58) | ((uint64(v10)) << 57) | ((uint64(v10)) << 56) | ((uint64(v10)) << 55) | ((uint64(v10)) << 54) | ((uint64(v10)) << 53) | ((uint64(v10)) << 52) | ((uint64(v10)) << 51) | ((uint64(v10)) << 50) | ((uint64(v10)) << 49) | ((uint64(v10)) << 48) | ((uint64(v10)) << 47) | ((uint64(v10)) << 46) | ((uint64(v10)) << 45) | ((uint64(v10)) << 44) | ((uint64(v10)) << 43) | ((uint64(v10)) << 42) | ((uint64(v10)) << 41) | ((uint64(v10)) << 40) | ((uint64(v10)) << 39) | ((uint64(v10)) << 38) | ((uint64(v10)) << 37) | ((uint64(v10)) << 36) | ((uint64(v10)) << 35) | ((uint64(v10)) << 34) | ((uint64(v10)) << 33) | ((uint64(v10)) << 32) | (uint64(v7))))
	return uint64(v11)
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_divw_gpr_gpr_same_32__reg_a0__go__native_first(g0)
	_ = sink
}
