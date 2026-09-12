// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of divw_gpr_gpr_gpr_32__reg_a0__go__native_first.
//   Concat(If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v1) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v1) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v1) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v1) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Or(Extract(31, 0, v0) == 0, And(Extract(31, 0, v1) == 2147483648, Extract(31, 0, v0) == 4294967295)), 1, Extract(31, 31, bvsdiv_i(Extract(31, 0, v1), Extract(31, 0, v0)))), If(Or(Extract
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_divw_gpr_gpr_gpr_32__reg_a0__go__native_first(a uint32, b uint32) uint64 {
	var v0 uint32 = uint32(b)
	var v1 uint32 = uint32(a)
	var v2 uint32 = (uint32(uint32((int32(v1)) / (int32(v0)))))
	var v3 bool = ((uint32(v0)) == (uint32(uint32(0xffffffff))))
	var v4 bool = ((uint32(v1)) == (uint32(uint32(0x80000000))))
	var v5 bool = ((v4) && (v3))
	var v6 uint32 = sel32(v5, uint32(uint32(0x80000000)), uint32(v2))
	var v7 bool = ((uint32(v0)) == (uint32(uint32(0x0))))
	var v8 uint32 = sel32(v7, uint32(uint32(0xffffffff)), uint32(v6))
	var v9 uint32 = ((uint32((uint32(v2)) >> 31)) & uint32(0x1))
	var v10 bool = ((v7) || (v5))
	var v11 uint32 = sel32(v10, uint32(uint32(0x1)), uint32(v9))
	var v12 uint64 = (uint64(((uint64(v11)) << 63) | ((uint64(v11)) << 62) | ((uint64(v11)) << 61) | ((uint64(v11)) << 60) | ((uint64(v11)) << 59) | ((uint64(v11)) << 58) | ((uint64(v11)) << 57) | ((uint64(v11)) << 56) | ((uint64(v11)) << 55) | ((uint64(v11)) << 54) | ((uint64(v11)) << 53) | ((uint64(v11)) << 52) | ((uint64(v11)) << 51) | ((uint64(v11)) << 50) | ((uint64(v11)) << 49) | ((uint64(v11)) << 48) | ((uint64(v11)) << 47) | ((uint64(v11)) << 46) | ((uint64(v11)) << 45) | ((uint64(v11)) << 44) | ((uint64(v11)) << 43) | ((uint64(v11)) << 42) | ((uint64(v11)) << 41) | ((uint64(v11)) << 40) | ((uint64(v11)) << 39) | ((uint64(v11)) << 38) | ((uint64(v11)) << 37) | ((uint64(v11)) << 36) | ((uint64(v11)) << 35) | ((uint64(v11)) << 34) | ((uint64(v11)) << 33) | ((uint64(v11)) << 32) | (uint64(v8))))
	return uint64(v12)
}

var g0 uint32
var g1 uint32
var sink interface{}

func main() {
	sink = emu_divw_gpr_gpr_gpr_32__reg_a0__go__native_first(g0, g1)
	_ = sink
}
