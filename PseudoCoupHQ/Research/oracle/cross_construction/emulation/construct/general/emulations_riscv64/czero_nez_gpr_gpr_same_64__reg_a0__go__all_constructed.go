// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of czero_nez_gpr_gpr_same_64__reg_a0__go__all_constructed.
//   If(v0 == 0, v0, 0)
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_czero_nez_gpr_gpr_same_64__reg_a0__go__all_constructed(a uint64) uint64 {
	var v0 uint64 = (uint64((uint64(uint64(a))) ^ (uint64(uint64(0x0)))))
	var v1 uint64 = (uint64((uint64(v0)) >> ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v2 uint64 = (uint64((uint64(v0)) | (uint64(v1))))
	var v3 uint64 = (uint64((uint64(v2)) >> ((uint64(uint64(0x2))) & uint64(0x3f))))
	var v4 uint64 = (uint64((uint64(v2)) | (uint64(v3))))
	var v5 uint64 = (uint64((uint64(v4)) >> ((uint64(uint64(0x4))) & uint64(0x3f))))
	var v6 uint64 = (uint64((uint64(v4)) | (uint64(v5))))
	var v7 uint64 = (uint64((uint64(v6)) >> ((uint64(uint64(0x8))) & uint64(0x3f))))
	var v8 uint64 = (uint64((uint64(v6)) | (uint64(v7))))
	var v9 uint64 = (uint64((uint64(v8)) >> ((uint64(uint64(0x10))) & uint64(0x3f))))
	var v10 uint64 = (uint64((uint64(v8)) | (uint64(v9))))
	var v11 uint64 = (uint64((uint64(v10)) >> ((uint64(uint64(0x20))) & uint64(0x3f))))
	var v12 uint64 = (uint64((uint64(v10)) | (uint64(v11))))
	var v13 uint32 = ((uint32((uint64(v12)) >> 0)) & uint32(0x1))
	var v14 bool = ((uint32(uint32(0x1))) == (uint32(v13)))
	var v15 bool = (!(v14))
	var v16 uint64 = sel64(v15, uint64(uint64(a)), uint64(uint64(0x0)))
	return uint64(v16)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_czero_nez_gpr_gpr_same_64__reg_a0__go__all_constructed(g0)
	_ = sink
}
