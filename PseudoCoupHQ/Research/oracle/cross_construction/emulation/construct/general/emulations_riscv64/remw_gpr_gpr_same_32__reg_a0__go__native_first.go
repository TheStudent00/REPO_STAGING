// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of remw_gpr_gpr_same_32__reg_a0__go__native_first.
//   Concat(If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v0))))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v0))))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v0))))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, v0) == 4294967295), 0, Extract(31, 31, bvsrem_i(Extract(31, 0, v0), Extract(31, 0, v0))))), If(Extract(31, 0, v0) == 0, Extract(31, 31, v0), If(And(Extract(31, 0, v0) == 2147483648, Extract(31, 0, 
package main

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_remw_gpr_gpr_same_32__reg_a0__go__native_first(a uint32) uint64 {
	var v0 uint32 = uint32(a)
	var v1 uint32 = (uint32(uint32((int32(v0)) % (int32(v0)))))
	var v2 bool = ((uint32(v0)) == (uint32(uint32(0xffffffff))))
	var v3 bool = ((uint32(v0)) == (uint32(uint32(0x80000000))))
	var v4 bool = ((v3) && (v2))
	var v5 uint32 = sel32(v4, uint32(uint32(0x0)), uint32(v1))
	var v6 bool = ((uint32(v0)) == (uint32(uint32(0x0))))
	var v7 uint32 = sel32(v6, uint32(v0), uint32(v5))
	var v8 uint32 = ((uint32((uint32(v1)) >> 31)) & uint32(0x1))
	var v9 uint32 = sel32(v4, uint32(uint32(0x0)), uint32(v8))
	var v10 uint32 = ((uint32((uint32(a)) >> 31)) & uint32(0x1))
	var v11 uint32 = sel32(v6, uint32(v10), uint32(v9))
	var v12 uint64 = (uint64(((uint64(v11)) << 63) | ((uint64(v11)) << 62) | ((uint64(v11)) << 61) | ((uint64(v11)) << 60) | ((uint64(v11)) << 59) | ((uint64(v11)) << 58) | ((uint64(v11)) << 57) | ((uint64(v11)) << 56) | ((uint64(v11)) << 55) | ((uint64(v11)) << 54) | ((uint64(v11)) << 53) | ((uint64(v11)) << 52) | ((uint64(v11)) << 51) | ((uint64(v11)) << 50) | ((uint64(v11)) << 49) | ((uint64(v11)) << 48) | ((uint64(v11)) << 47) | ((uint64(v11)) << 46) | ((uint64(v11)) << 45) | ((uint64(v11)) << 44) | ((uint64(v11)) << 43) | ((uint64(v11)) << 42) | ((uint64(v11)) << 41) | ((uint64(v11)) << 40) | ((uint64(v11)) << 39) | ((uint64(v11)) << 38) | ((uint64(v11)) << 37) | ((uint64(v11)) << 36) | ((uint64(v11)) << 35) | ((uint64(v11)) << 34) | ((uint64(v11)) << 33) | ((uint64(v11)) << 32) | (uint64(v7))))
	return uint64(v12)
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_remw_gpr_gpr_same_32__reg_a0__go__native_first(g0)
	_ = sink
}
