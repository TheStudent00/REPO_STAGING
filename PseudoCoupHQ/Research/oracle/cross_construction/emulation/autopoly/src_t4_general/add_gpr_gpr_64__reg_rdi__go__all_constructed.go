// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of add_gpr_gpr_64__reg_rdi__go__all_constructed.
//   v0 + v1
package main

//go:noinline
func emu_add_gpr_gpr_64__reg_rdi__go__all_constructed(a uint64, b uint64) uint64 {
	var v0 uint64 = (uint64((uint64(uint64(a))) & (uint64(uint64(b)))))
	var v1 uint64 = (uint64((uint64(v0)) << ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v2 uint64 = (uint64((uint64(uint64(a))) ^ (uint64(uint64(b)))))
	var v3 uint64 = (uint64((uint64(v2)) & (uint64(v1))))
	var v4 uint64 = (uint64((uint64(v0)) | (uint64(v3))))
	var v5 uint64 = (uint64((uint64(v4)) << ((uint64(uint64(0x2))) & uint64(0x3f))))
	var v6 uint64 = (uint64((uint64(v2)) << ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v7 uint64 = (uint64((uint64(v2)) & (uint64(v6))))
	var v8 uint64 = (uint64((uint64(v7)) & (uint64(v5))))
	var v9 uint64 = (uint64((uint64(v4)) | (uint64(v8))))
	var v10 uint64 = (uint64((uint64(v9)) << ((uint64(uint64(0x4))) & uint64(0x3f))))
	var v11 uint64 = (uint64((uint64(v7)) << ((uint64(uint64(0x2))) & uint64(0x3f))))
	var v12 uint64 = (uint64((uint64(v7)) & (uint64(v11))))
	var v13 uint64 = (uint64((uint64(v12)) & (uint64(v10))))
	var v14 uint64 = (uint64((uint64(v9)) | (uint64(v13))))
	var v15 uint64 = (uint64((uint64(v14)) << ((uint64(uint64(0x8))) & uint64(0x3f))))
	var v16 uint64 = (uint64((uint64(v12)) << ((uint64(uint64(0x4))) & uint64(0x3f))))
	var v17 uint64 = (uint64((uint64(v12)) & (uint64(v16))))
	var v18 uint64 = (uint64((uint64(v17)) & (uint64(v15))))
	var v19 uint64 = (uint64((uint64(v14)) | (uint64(v18))))
	var v20 uint64 = (uint64((uint64(v19)) << ((uint64(uint64(0x10))) & uint64(0x3f))))
	var v21 uint64 = (uint64((uint64(v17)) << ((uint64(uint64(0x8))) & uint64(0x3f))))
	var v22 uint64 = (uint64((uint64(v17)) & (uint64(v21))))
	var v23 uint64 = (uint64((uint64(v22)) & (uint64(v20))))
	var v24 uint64 = (uint64((uint64(v19)) | (uint64(v23))))
	var v25 uint64 = (uint64((uint64(v24)) << ((uint64(uint64(0x20))) & uint64(0x3f))))
	var v26 uint64 = (uint64((uint64(v22)) << ((uint64(uint64(0x10))) & uint64(0x3f))))
	var v27 uint64 = (uint64((uint64(v22)) & (uint64(v26))))
	var v28 uint64 = (uint64((uint64(v27)) & (uint64(v25))))
	var v29 uint64 = (uint64((uint64(v24)) | (uint64(v28))))
	var v30 uint64 = (uint64((uint64(v29)) << ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v31 uint64 = (uint64((uint64(v2)) ^ (uint64(v30))))
	return uint64(v31)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_add_gpr_gpr_64__reg_rdi__go__all_constructed(g0, g1)
	_ = sink
}
