// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of addiw_gpr_gpr_imm_32__reg_a0__go__all_constructed.
//   Concat(Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v0) + 3), Extract(31, 31, Extract(31, 0, v
package main

//go:noinline
func emu_addiw_gpr_gpr_imm_32__reg_a0__go__all_constructed(a uint32) uint64 {
	var v0 uint32 = uint32(a)
	var v1 uint32 = (uint32((uint32(v0)) & (uint32(uint32(0x3)))))
	var v2 uint32 = (uint32((uint32(v1)) << ((uint32(uint32(0x1))) & uint32(0x1f))))
	var v3 uint32 = (uint32((uint32(v0)) ^ (uint32(uint32(0x3)))))
	var v4 uint32 = (uint32((uint32(v3)) & (uint32(v2))))
	var v5 uint32 = (uint32((uint32(v1)) | (uint32(v4))))
	var v6 uint32 = (uint32((uint32(v5)) << ((uint32(uint32(0x2))) & uint32(0x1f))))
	var v7 uint32 = (uint32((uint32(v3)) << ((uint32(uint32(0x1))) & uint32(0x1f))))
	var v8 uint32 = (uint32((uint32(v3)) & (uint32(v7))))
	var v9 uint32 = (uint32((uint32(v8)) & (uint32(v6))))
	var v10 uint32 = (uint32((uint32(v5)) | (uint32(v9))))
	var v11 uint32 = (uint32((uint32(v10)) << ((uint32(uint32(0x4))) & uint32(0x1f))))
	var v12 uint32 = (uint32((uint32(v8)) << ((uint32(uint32(0x2))) & uint32(0x1f))))
	var v13 uint32 = (uint32((uint32(v8)) & (uint32(v12))))
	var v14 uint32 = (uint32((uint32(v13)) & (uint32(v11))))
	var v15 uint32 = (uint32((uint32(v10)) | (uint32(v14))))
	var v16 uint32 = (uint32((uint32(v15)) << ((uint32(uint32(0x8))) & uint32(0x1f))))
	var v17 uint32 = (uint32((uint32(v13)) << ((uint32(uint32(0x4))) & uint32(0x1f))))
	var v18 uint32 = (uint32((uint32(v13)) & (uint32(v17))))
	var v19 uint32 = (uint32((uint32(v18)) & (uint32(v16))))
	var v20 uint32 = (uint32((uint32(v15)) | (uint32(v19))))
	var v21 uint32 = (uint32((uint32(v20)) << ((uint32(uint32(0x10))) & uint32(0x1f))))
	var v22 uint32 = (uint32((uint32(v18)) << ((uint32(uint32(0x8))) & uint32(0x1f))))
	var v23 uint32 = (uint32((uint32(v18)) & (uint32(v22))))
	var v24 uint32 = (uint32((uint32(v23)) & (uint32(v21))))
	var v25 uint32 = (uint32((uint32(v20)) | (uint32(v24))))
	var v26 uint32 = (uint32((uint32(v25)) << ((uint32(uint32(0x1))) & uint32(0x1f))))
	var v27 uint32 = (uint32((uint32(v3)) ^ (uint32(v26))))
	var v28 uint32 = ((uint32((uint32(v27)) >> 31)) & uint32(0x1))
	var v29 uint32 = v27
	var v30 uint32 = v28
	var v31 uint32 = ((uint32(((uint32(v30)) << 1) | (uint32(v30)))) & uint32(0x3))
	var v32 uint32 = ((uint32(((uint32(v31)) << 1) | (uint32(v30)))) & uint32(0x7))
	var v33 uint32 = ((uint32(((uint32(v32)) << 1) | (uint32(v30)))) & uint32(0xf))
	var v34 uint32 = ((uint32(((uint32(v33)) << 1) | (uint32(v30)))) & uint32(0x1f))
	var v35 uint32 = ((uint32(((uint32(v34)) << 1) | (uint32(v30)))) & uint32(0x3f))
	var v36 uint32 = ((uint32(((uint32(v35)) << 1) | (uint32(v30)))) & uint32(0x7f))
	var v37 uint32 = ((uint32(((uint32(v36)) << 1) | (uint32(v30)))) & uint32(0xff))
	var v38 uint32 = ((uint32(((uint32(v37)) << 1) | (uint32(v30)))) & uint32(0x1ff))
	var v39 uint32 = ((uint32(((uint32(v38)) << 1) | (uint32(v30)))) & uint32(0x3ff))
	var v40 uint32 = ((uint32(((uint32(v39)) << 1) | (uint32(v30)))) & uint32(0x7ff))
	var v41 uint32 = ((uint32(((uint32(v40)) << 1) | (uint32(v30)))) & uint32(0xfff))
	var v42 uint32 = ((uint32(((uint32(v41)) << 1) | (uint32(v30)))) & uint32(0x1fff))
	var v43 uint32 = ((uint32(((uint32(v42)) << 1) | (uint32(v30)))) & uint32(0x3fff))
	var v44 uint32 = ((uint32(((uint32(v43)) << 1) | (uint32(v30)))) & uint32(0x7fff))
	var v45 uint32 = ((uint32(((uint32(v44)) << 1) | (uint32(v30)))) & uint32(0xffff))
	var v46 uint32 = ((uint32(((uint32(v45)) << 1) | (uint32(v30)))) & uint32(0x1ffff))
	var v47 uint32 = ((uint32(((uint32(v46)) << 1) | (uint32(v30)))) & uint32(0x3ffff))
	var v48 uint32 = ((uint32(((uint32(v47)) << 1) | (uint32(v30)))) & uint32(0x7ffff))
	var v49 uint32 = ((uint32(((uint32(v48)) << 1) | (uint32(v30)))) & uint32(0xfffff))
	var v50 uint32 = ((uint32(((uint32(v49)) << 1) | (uint32(v30)))) & uint32(0x1fffff))
	var v51 uint32 = ((uint32(((uint32(v50)) << 1) | (uint32(v30)))) & uint32(0x3fffff))
	var v52 uint32 = ((uint32(((uint32(v51)) << 1) | (uint32(v30)))) & uint32(0x7fffff))
	var v53 uint32 = ((uint32(((uint32(v52)) << 1) | (uint32(v30)))) & uint32(0xffffff))
	var v54 uint32 = ((uint32(((uint32(v53)) << 1) | (uint32(v30)))) & uint32(0x1ffffff))
	var v55 uint32 = ((uint32(((uint32(v54)) << 1) | (uint32(v30)))) & uint32(0x3ffffff))
	var v56 uint32 = ((uint32(((uint32(v55)) << 1) | (uint32(v30)))) & uint32(0x7ffffff))
	var v57 uint32 = ((uint32(((uint32(v56)) << 1) | (uint32(v30)))) & uint32(0xfffffff))
	var v58 uint32 = ((uint32(((uint32(v57)) << 1) | (uint32(v30)))) & uint32(0x1fffffff))
	var v59 uint32 = ((uint32(((uint32(v58)) << 1) | (uint32(v30)))) & uint32(0x3fffffff))
	var v60 uint32 = ((uint32(((uint32(v59)) << 1) | (uint32(v30)))) & uint32(0x7fffffff))
	var v61 uint32 = (uint32(((uint32(v60)) << 1) | (uint32(v30))))
	var v62 uint64 = (uint64(((uint64(v61)) << 32) | (uint64(v29))))
	return uint64(v62)
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_addiw_gpr_gpr_imm_32__reg_a0__go__all_constructed(g0)
	_ = sink
}
