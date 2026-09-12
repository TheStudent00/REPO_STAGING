// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed.
//   If(Or(Extract(1, 0, v0) == 3, Not(Extract(63, 2, v0) == 0)), 0, 1)
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed(a uint64) uint64 {
	var v0 uint64 = ((uint64((uint64(a)) >> 2)) & uint64(0x3fffffffffffffff))
	var v1 uint64 = ((uint64((uint64(v0)) ^ (uint64(uint64(0x0))))) & uint64(0x3fffffffffffffff))
	var v2 uint64 = ((uint64((uint64(v1)) >> ((uint64(uint64(0x1))) & uint64(0x3d)))) & uint64(0x3fffffffffffffff))
	var v3 uint64 = ((uint64((uint64(v1)) | (uint64(v2)))) & uint64(0x3fffffffffffffff))
	var v4 uint64 = ((uint64((uint64(v3)) >> ((uint64(uint64(0x2))) & uint64(0x3d)))) & uint64(0x3fffffffffffffff))
	var v5 uint64 = ((uint64((uint64(v3)) | (uint64(v4)))) & uint64(0x3fffffffffffffff))
	var v6 uint64 = ((uint64((uint64(v5)) >> ((uint64(uint64(0x4))) & uint64(0x3d)))) & uint64(0x3fffffffffffffff))
	var v7 uint64 = ((uint64((uint64(v5)) | (uint64(v6)))) & uint64(0x3fffffffffffffff))
	var v8 uint64 = ((uint64((uint64(v7)) >> ((uint64(uint64(0x8))) & uint64(0x3d)))) & uint64(0x3fffffffffffffff))
	var v9 uint64 = ((uint64((uint64(v7)) | (uint64(v8)))) & uint64(0x3fffffffffffffff))
	var v10 uint64 = ((uint64((uint64(v9)) >> ((uint64(uint64(0x10))) & uint64(0x3d)))) & uint64(0x3fffffffffffffff))
	var v11 uint64 = ((uint64((uint64(v9)) | (uint64(v10)))) & uint64(0x3fffffffffffffff))
	var v12 uint64 = ((uint64((uint64(v11)) >> ((uint64(uint64(0x20))) & uint64(0x3d)))) & uint64(0x3fffffffffffffff))
	var v13 uint64 = ((uint64((uint64(v11)) | (uint64(v12)))) & uint64(0x3fffffffffffffff))
	var v14 uint32 = ((uint32((uint64(v13)) >> 0)) & uint32(0x1))
	var v15 bool = ((uint32(uint32(0x1))) == (uint32(v14)))
	var v16 bool = (!(v15))
	var v17 bool = (!(v16))
	var v18 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0x3))
	var v19 uint32 = ((uint32((uint32(v18)) ^ (uint32(uint32(0x3))))) & uint32(0x3))
	var v20 uint32 = ((uint32((uint32(v19)) >> ((uint32(uint32(0x1))) & uint32(0x1)))) & uint32(0x3))
	var v21 uint32 = ((uint32((uint32(v19)) | (uint32(v20)))) & uint32(0x3))
	var v22 uint32 = ((uint32((uint32(v21)) >> 0)) & uint32(0x1))
	var v23 bool = ((uint32(uint32(0x1))) == (uint32(v22)))
	var v24 bool = (!(v23))
	var v25 bool = ((v24) || (v17))
	var v26 uint64 = sel64(v25, uint64(uint64(0x0)), uint64(uint64(0x1)))
	return uint64(v26)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_sltiu_gpr_gpr_imm_64__reg_a0__go__all_constructed(g0)
	_ = sink
}
