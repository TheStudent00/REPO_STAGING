// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of remw_gpr_gpr_gpr_32__reg_a0__go__native_first.
//   Concat(If(Extract(31, 0, v1) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v1) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v1))))), If(Extract(31, 0, v1) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v1) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v1))))), If(Extract(31, 0, v1) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v1) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v1))))), If(Extract(31, 0, v1) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v1) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v1))))), If(Extract(31, 0, v1) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, 
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_remw_gpr_gpr_gpr_32__reg_a0__go__native_first(a uint32, b uint32) uint64 {
	var v0 uint32 = uint32(b)
	var v1 uint32 = uint32(a)
	var v2 uint32 = (uint32(uint32((int32(v1)) % (int32(v0)))))
	var v3 bool = ((uint32(v0)) == (uint32(uint32(0xffffffff))))
	var v4 bool = ((uint32(v1)) == (uint32(uint32(0x80000000))))
	var v5 bool = ((v4) && (v3))
	var v6 uint32 = sel32(v5, uint32(uint32(0x0)), uint32(v2))
	var v7 bool = ((uint32(v0)) == (uint32(uint32(0x0))))
	var v8 uint32 = sel32(v7, uint32(v1), uint32(v6))
	var v9 uint32 = ((uint32((uint32(v2)) >> 31)) & uint32(0x1))
	var v10 uint32 = sel32(v5, uint32(uint32(0x0)), uint32(v9))
	var v11 uint32 = ((uint32((uint32(a)) >> 31)) & uint32(0x1))
	var v12 uint32 = sel32(v7, uint32(v11), uint32(v10))
	var v13 uint64 = (uint64(((uint64(v12)) << 63) | ((uint64(v12)) << 62) | ((uint64(v12)) << 61) | ((uint64(v12)) << 60) | ((uint64(v12)) << 59) | ((uint64(v12)) << 58) | ((uint64(v12)) << 57) | ((uint64(v12)) << 56) | ((uint64(v12)) << 55) | ((uint64(v12)) << 54) | ((uint64(v12)) << 53) | ((uint64(v12)) << 52) | ((uint64(v12)) << 51) | ((uint64(v12)) << 50) | ((uint64(v12)) << 49) | ((uint64(v12)) << 48) | ((uint64(v12)) << 47) | ((uint64(v12)) << 46) | ((uint64(v12)) << 45) | ((uint64(v12)) << 44) | ((uint64(v12)) << 43) | ((uint64(v12)) << 42) | ((uint64(v12)) << 41) | ((uint64(v12)) << 40) | ((uint64(v12)) << 39) | ((uint64(v12)) << 38) | ((uint64(v12)) << 37) | ((uint64(v12)) << 36) | ((uint64(v12)) << 35) | ((uint64(v12)) << 34) | ((uint64(v12)) << 33) | ((uint64(v12)) << 32) | (uint64(v8))))
	return uint64(v13)
}

var g0 uint32
var g1 uint32
var sink interface{}

func main() {
	sink = emu_remw_gpr_gpr_gpr_32__reg_a0__go__native_first(g0, g1)
	_ = sink
}
