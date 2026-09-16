// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of sll_gpr_gpr_gpr_64__reg_a0__go__all_constructed.
//   v0 << Concat(0, Extract(5, 0, v1))
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_sll_gpr_gpr_gpr_64__reg_a0__go__all_constructed(a uint64, b uint8) uint64 {
	var v0 uint32 = ((uint32((uint32(b)) >> 0)) & uint32(0x3f))
	var v1 uint32 = v0
	var v2 uint64 = uint64(0x0)
	var v3 uint64 = (uint64(((uint64(v2)) << 6) | (uint64(v1))))
	var v4 uint32 = ((uint32((uint64(v3)) >> 5)) & uint32(0x1))
	var v5 bool = ((uint32(uint32(0x1))) == (uint32(v4)))
	var v6 uint64 = sel64(v5, uint64(uint64(0xffffffffffffffff)), uint64(uint64(0x0)))
	var v7 uint64 = (uint64(^(uint64(v6))))
	var v8 uint32 = ((uint32((uint64(v3)) >> 4)) & uint32(0x1))
	var v9 bool = ((uint32(uint32(0x1))) == (uint32(v8)))
	var v10 uint64 = sel64(v9, uint64(uint64(0xffffffffffffffff)), uint64(uint64(0x0)))
	var v11 uint64 = (uint64(^(uint64(v10))))
	var v12 uint32 = ((uint32((uint64(v3)) >> 3)) & uint32(0x1))
	var v13 bool = ((uint32(uint32(0x1))) == (uint32(v12)))
	var v14 uint64 = sel64(v13, uint64(uint64(0xffffffffffffffff)), uint64(uint64(0x0)))
	var v15 uint64 = (uint64(^(uint64(v14))))
	var v16 uint32 = ((uint32((uint64(v3)) >> 2)) & uint32(0x1))
	var v17 bool = ((uint32(uint32(0x1))) == (uint32(v16)))
	var v18 uint64 = sel64(v17, uint64(uint64(0xffffffffffffffff)), uint64(uint64(0x0)))
	var v19 uint64 = (uint64(^(uint64(v18))))
	var v20 uint32 = ((uint32((uint64(v3)) >> 1)) & uint32(0x1))
	var v21 bool = ((uint32(uint32(0x1))) == (uint32(v20)))
	var v22 uint64 = sel64(v21, uint64(uint64(0xffffffffffffffff)), uint64(uint64(0x0)))
	var v23 uint64 = (uint64(^(uint64(v22))))
	var v24 uint32 = ((uint32((uint64(v3)) >> 0)) & uint32(0x1))
	var v25 bool = ((uint32(uint32(0x1))) == (uint32(v24)))
	var v26 uint64 = sel64(v25, uint64(uint64(0xffffffffffffffff)), uint64(uint64(0x0)))
	var v27 uint64 = (uint64(^(uint64(v26))))
	var v28 uint64 = (uint64((uint64(uint64(a))) & (uint64(v27))))
	var v29 uint64 = (uint64((uint64(uint64(a))) << ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v30 uint64 = (uint64((uint64(v29)) & (uint64(v26))))
	var v31 uint64 = (uint64((uint64(v30)) | (uint64(v28))))
	var v32 uint64 = (uint64((uint64(v31)) & (uint64(v23))))
	var v33 uint64 = (uint64((uint64(v31)) << ((uint64(uint64(0x2))) & uint64(0x3f))))
	var v34 uint64 = (uint64((uint64(v33)) & (uint64(v22))))
	var v35 uint64 = (uint64((uint64(v34)) | (uint64(v32))))
	var v36 uint64 = (uint64((uint64(v35)) & (uint64(v19))))
	var v37 uint64 = (uint64((uint64(v35)) << ((uint64(uint64(0x4))) & uint64(0x3f))))
	var v38 uint64 = (uint64((uint64(v37)) & (uint64(v18))))
	var v39 uint64 = (uint64((uint64(v38)) | (uint64(v36))))
	var v40 uint64 = (uint64((uint64(v39)) & (uint64(v15))))
	var v41 uint64 = (uint64((uint64(v39)) << ((uint64(uint64(0x8))) & uint64(0x3f))))
	var v42 uint64 = (uint64((uint64(v41)) & (uint64(v14))))
	var v43 uint64 = (uint64((uint64(v42)) | (uint64(v40))))
	var v44 uint64 = (uint64((uint64(v43)) & (uint64(v11))))
	var v45 uint64 = (uint64((uint64(v43)) << ((uint64(uint64(0x10))) & uint64(0x3f))))
	var v46 uint64 = (uint64((uint64(v45)) & (uint64(v10))))
	var v47 uint64 = (uint64((uint64(v46)) | (uint64(v44))))
	var v48 uint64 = (uint64((uint64(v47)) & (uint64(v7))))
	var v49 uint64 = (uint64((uint64(v47)) << ((uint64(uint64(0x20))) & uint64(0x3f))))
	var v50 uint64 = (uint64((uint64(v49)) & (uint64(v6))))
	var v51 uint64 = (uint64((uint64(v50)) | (uint64(v48))))
	var v52 uint64 = (uint64(uint32(0x1)))
	var v53 uint64 = (uint64(^(uint64(uint64(0x40)))))
	var v54 uint64 = (uint64((uint64(v3)) ^ (uint64(v53))))
	var v55 uint64 = (uint64((uint64(v54)) & (uint64(v52))))
	var v56 uint64 = (uint64((uint64(v3)) & (uint64(v53))))
	var v57 uint64 = (uint64((uint64(v56)) | (uint64(v55))))
	var v58 uint64 = (uint64((uint64(v57)) << ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v59 uint64 = (uint64((uint64(v54)) & (uint64(v58))))
	var v60 uint64 = (uint64((uint64(v57)) | (uint64(v59))))
	var v61 uint64 = (uint64((uint64(v60)) << ((uint64(uint64(0x2))) & uint64(0x3f))))
	var v62 uint64 = (uint64((uint64(v54)) << ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v63 uint64 = (uint64((uint64(v54)) & (uint64(v62))))
	var v64 uint64 = (uint64((uint64(v63)) & (uint64(v61))))
	var v65 uint64 = (uint64((uint64(v60)) | (uint64(v64))))
	var v66 uint64 = (uint64((uint64(v65)) << ((uint64(uint64(0x4))) & uint64(0x3f))))
	var v67 uint64 = (uint64((uint64(v63)) << ((uint64(uint64(0x2))) & uint64(0x3f))))
	var v68 uint64 = (uint64((uint64(v63)) & (uint64(v67))))
	var v69 uint64 = (uint64((uint64(v68)) & (uint64(v66))))
	var v70 uint64 = (uint64((uint64(v65)) | (uint64(v69))))
	var v71 uint64 = (uint64((uint64(v70)) << ((uint64(uint64(0x8))) & uint64(0x3f))))
	var v72 uint64 = (uint64((uint64(v68)) << ((uint64(uint64(0x4))) & uint64(0x3f))))
	var v73 uint64 = (uint64((uint64(v68)) & (uint64(v72))))
	var v74 uint64 = (uint64((uint64(v73)) & (uint64(v71))))
	var v75 uint64 = (uint64((uint64(v70)) | (uint64(v74))))
	var v76 uint64 = (uint64((uint64(v75)) << ((uint64(uint64(0x10))) & uint64(0x3f))))
	var v77 uint64 = (uint64((uint64(v73)) << ((uint64(uint64(0x8))) & uint64(0x3f))))
	var v78 uint64 = (uint64((uint64(v73)) & (uint64(v77))))
	var v79 uint64 = (uint64((uint64(v78)) & (uint64(v76))))
	var v80 uint64 = (uint64((uint64(v75)) | (uint64(v79))))
	var v81 uint64 = (uint64((uint64(v80)) << ((uint64(uint64(0x20))) & uint64(0x3f))))
	var v82 uint64 = (uint64((uint64(v78)) << ((uint64(uint64(0x10))) & uint64(0x3f))))
	var v83 uint64 = (uint64((uint64(v78)) & (uint64(v82))))
	var v84 uint64 = (uint64((uint64(v83)) & (uint64(v81))))
	var v85 uint64 = (uint64((uint64(v80)) | (uint64(v84))))
	var v86 uint32 = ((uint32((uint64(v85)) >> 63)) & uint32(0x1))
	var v87 bool = ((uint32(uint32(0x0))) == (uint32(v86)))
	var v88 bool = (!(v87))
	var v89 uint64 = sel64(v88, uint64(uint64(0x0)), uint64(v51))
	return uint64(v89)
}

var g0 uint64
var g1 uint8
var sink interface{}

func main() {
	sink = emu_sll_gpr_gpr_gpr_64__reg_a0__go__all_constructed(g0, g1)
	_ = sink
}
