// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of bltu_gpr_gpr_imm_64__branch_condition__go__all_constructed.
//   If(ULE(v0, v1), 0, 1)
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_bltu_gpr_gpr_imm_64__branch_condition__go__all_constructed(a uint64, b uint64) uint64 {
	var v0 uint64 = (uint64(uint32(0x1)))
	var v1 uint64 = (uint64(^(uint64(uint64(b)))))
	var v2 uint64 = (uint64((uint64(uint64(a))) ^ (uint64(v1))))
	var v3 uint64 = (uint64((uint64(v2)) & (uint64(v0))))
	var v4 uint64 = (uint64((uint64(uint64(a))) & (uint64(v1))))
	var v5 uint64 = (uint64((uint64(v4)) | (uint64(v3))))
	var v6 uint64 = (uint64((uint64(v5)) << ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v7 uint64 = (uint64((uint64(v2)) & (uint64(v6))))
	var v8 uint64 = (uint64((uint64(v5)) | (uint64(v7))))
	var v9 uint64 = (uint64((uint64(v8)) << ((uint64(uint64(0x2))) & uint64(0x3f))))
	var v10 uint64 = (uint64((uint64(v2)) << ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v11 uint64 = (uint64((uint64(v2)) & (uint64(v10))))
	var v12 uint64 = (uint64((uint64(v11)) & (uint64(v9))))
	var v13 uint64 = (uint64((uint64(v8)) | (uint64(v12))))
	var v14 uint64 = (uint64((uint64(v13)) << ((uint64(uint64(0x4))) & uint64(0x3f))))
	var v15 uint64 = (uint64((uint64(v11)) << ((uint64(uint64(0x2))) & uint64(0x3f))))
	var v16 uint64 = (uint64((uint64(v11)) & (uint64(v15))))
	var v17 uint64 = (uint64((uint64(v16)) & (uint64(v14))))
	var v18 uint64 = (uint64((uint64(v13)) | (uint64(v17))))
	var v19 uint64 = (uint64((uint64(v18)) << ((uint64(uint64(0x8))) & uint64(0x3f))))
	var v20 uint64 = (uint64((uint64(v16)) << ((uint64(uint64(0x4))) & uint64(0x3f))))
	var v21 uint64 = (uint64((uint64(v16)) & (uint64(v20))))
	var v22 uint64 = (uint64((uint64(v21)) & (uint64(v19))))
	var v23 uint64 = (uint64((uint64(v18)) | (uint64(v22))))
	var v24 uint64 = (uint64((uint64(v23)) << ((uint64(uint64(0x10))) & uint64(0x3f))))
	var v25 uint64 = (uint64((uint64(v21)) << ((uint64(uint64(0x8))) & uint64(0x3f))))
	var v26 uint64 = (uint64((uint64(v21)) & (uint64(v25))))
	var v27 uint64 = (uint64((uint64(v26)) & (uint64(v24))))
	var v28 uint64 = (uint64((uint64(v23)) | (uint64(v27))))
	var v29 uint64 = (uint64((uint64(v28)) << ((uint64(uint64(0x20))) & uint64(0x3f))))
	var v30 uint64 = (uint64((uint64(v26)) << ((uint64(uint64(0x10))) & uint64(0x3f))))
	var v31 uint64 = (uint64((uint64(v26)) & (uint64(v30))))
	var v32 uint64 = (uint64((uint64(v31)) & (uint64(v29))))
	var v33 uint64 = (uint64((uint64(v28)) | (uint64(v32))))
	var v34 uint32 = ((uint32((uint64(v33)) >> 63)) & uint32(0x1))
	var v35 bool = ((uint32(uint32(0x0))) == (uint32(v34)))
	var v36 bool = (!(v35))
	var v37 uint64 = sel64(v36, uint64(uint64(0x0)), uint64(uint64(0x1)))
	return uint64(v37)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_bltu_gpr_gpr_imm_64__branch_condition__go__all_constructed(g0, g1)
	_ = sink
}
