// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ZBS_IOP__op_BEXTI__rd__go__all_constructed.
//   
package main

func sel64(c bool, x uint64, y uint64) uint64 {
	if c {
		return x
	}
	return y
}

func sel32(c bool, x uint32, y uint32) uint32 {
	if c {
		return x
	}
	return y
}

//go:noinline
func emu_ZBS_IOP__op_BEXTI__rd__go__all_constructed(a uint64, b uint8) uint64 {
	var v0 uint64 = (uint64(^(uint64(uint64(a)))))
	var v1 uint32 = ((uint32((uint32(b)) >> 0)) & uint32(0x3f))
	var v2 uint32 = v1
	var v3 uint64 = uint64(0x0)
	var v4 uint64 = (uint64(((uint64(v3)) << 6) | (uint64(v2))))
	var v5 uint32 = ((uint32((uint64(v4)) >> 5)) & uint32(0x1))
	var v6 bool = ((uint32(uint32(0x1))) == (uint32(v5)))
	var v7 uint64 = sel64(v6, uint64(uint64(0xffffffffffffffff)), uint64(uint64(0x0)))
	var v8 uint64 = (uint64(^(uint64(v7))))
	var v9 uint32 = ((uint32((uint64(v4)) >> 4)) & uint32(0x1))
	var v10 bool = ((uint32(uint32(0x1))) == (uint32(v9)))
	var v11 uint64 = sel64(v10, uint64(uint64(0xffffffffffffffff)), uint64(uint64(0x0)))
	var v12 uint64 = (uint64(^(uint64(v11))))
	var v13 uint32 = ((uint32((uint64(v4)) >> 3)) & uint32(0x1))
	var v14 bool = ((uint32(uint32(0x1))) == (uint32(v13)))
	var v15 uint64 = sel64(v14, uint64(uint64(0xffffffffffffffff)), uint64(uint64(0x0)))
	var v16 uint64 = (uint64(^(uint64(v15))))
	var v17 uint32 = ((uint32((uint64(v4)) >> 2)) & uint32(0x1))
	var v18 bool = ((uint32(uint32(0x1))) == (uint32(v17)))
	var v19 uint64 = sel64(v18, uint64(uint64(0xffffffffffffffff)), uint64(uint64(0x0)))
	var v20 uint64 = (uint64(^(uint64(v19))))
	var v21 uint32 = ((uint32((uint64(v4)) >> 1)) & uint32(0x1))
	var v22 bool = ((uint32(uint32(0x1))) == (uint32(v21)))
	var v23 uint64 = sel64(v22, uint64(uint64(0xffffffffffffffff)), uint64(uint64(0x0)))
	var v24 uint64 = (uint64(^(uint64(v23))))
	var v25 uint32 = ((uint32((uint64(v4)) >> 0)) & uint32(0x1))
	var v26 bool = ((uint32(uint32(0x1))) == (uint32(v25)))
	var v27 uint64 = sel64(v26, uint64(uint64(0xffffffffffffffff)), uint64(uint64(0x0)))
	var v28 uint64 = (uint64(^(uint64(v27))))
	var v29 uint64 = (uint64((uint64(uint64(0x1))) & (uint64(v28))))
	var v30 uint64 = (uint64((uint64(uint64(0x1))) << ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v31 uint64 = (uint64((uint64(v30)) & (uint64(v27))))
	var v32 uint64 = (uint64((uint64(v31)) | (uint64(v29))))
	var v33 uint64 = (uint64((uint64(v32)) & (uint64(v24))))
	var v34 uint64 = (uint64((uint64(v32)) << ((uint64(uint64(0x2))) & uint64(0x3f))))
	var v35 uint64 = (uint64((uint64(v34)) & (uint64(v23))))
	var v36 uint64 = (uint64((uint64(v35)) | (uint64(v33))))
	var v37 uint64 = (uint64((uint64(v36)) & (uint64(v20))))
	var v38 uint64 = (uint64((uint64(v36)) << ((uint64(uint64(0x4))) & uint64(0x3f))))
	var v39 uint64 = (uint64((uint64(v38)) & (uint64(v19))))
	var v40 uint64 = (uint64((uint64(v39)) | (uint64(v37))))
	var v41 uint64 = (uint64((uint64(v40)) & (uint64(v16))))
	var v42 uint64 = (uint64((uint64(v40)) << ((uint64(uint64(0x8))) & uint64(0x3f))))
	var v43 uint64 = (uint64((uint64(v42)) & (uint64(v15))))
	var v44 uint64 = (uint64((uint64(v43)) | (uint64(v41))))
	var v45 uint64 = (uint64((uint64(v44)) & (uint64(v12))))
	var v46 uint64 = (uint64((uint64(v44)) << ((uint64(uint64(0x10))) & uint64(0x3f))))
	var v47 uint64 = (uint64((uint64(v46)) & (uint64(v11))))
	var v48 uint64 = (uint64((uint64(v47)) | (uint64(v45))))
	var v49 uint64 = (uint64((uint64(v48)) & (uint64(v8))))
	var v50 uint64 = (uint64((uint64(v48)) << ((uint64(uint64(0x20))) & uint64(0x3f))))
	var v51 uint64 = (uint64((uint64(v50)) & (uint64(v7))))
	var v52 uint64 = (uint64((uint64(v51)) | (uint64(v49))))
	var v53 uint64 = (uint64(uint32(0x1)))
	var v54 uint64 = (uint64(^(uint64(uint64(0x40)))))
	var v55 uint64 = (uint64((uint64(v4)) ^ (uint64(v54))))
	var v56 uint64 = (uint64((uint64(v55)) & (uint64(v53))))
	var v57 uint64 = (uint64((uint64(v4)) & (uint64(v54))))
	var v58 uint64 = (uint64((uint64(v57)) | (uint64(v56))))
	var v59 uint64 = (uint64((uint64(v58)) << ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v60 uint64 = (uint64((uint64(v55)) & (uint64(v59))))
	var v61 uint64 = (uint64((uint64(v58)) | (uint64(v60))))
	var v62 uint64 = (uint64((uint64(v61)) << ((uint64(uint64(0x2))) & uint64(0x3f))))
	var v63 uint64 = (uint64((uint64(v55)) << ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v64 uint64 = (uint64((uint64(v55)) & (uint64(v63))))
	var v65 uint64 = (uint64((uint64(v64)) & (uint64(v62))))
	var v66 uint64 = (uint64((uint64(v61)) | (uint64(v65))))
	var v67 uint64 = (uint64((uint64(v66)) << ((uint64(uint64(0x4))) & uint64(0x3f))))
	var v68 uint64 = (uint64((uint64(v64)) << ((uint64(uint64(0x2))) & uint64(0x3f))))
	var v69 uint64 = (uint64((uint64(v64)) & (uint64(v68))))
	var v70 uint64 = (uint64((uint64(v69)) & (uint64(v67))))
	var v71 uint64 = (uint64((uint64(v66)) | (uint64(v70))))
	var v72 uint64 = (uint64((uint64(v71)) << ((uint64(uint64(0x8))) & uint64(0x3f))))
	var v73 uint64 = (uint64((uint64(v69)) << ((uint64(uint64(0x4))) & uint64(0x3f))))
	var v74 uint64 = (uint64((uint64(v69)) & (uint64(v73))))
	var v75 uint64 = (uint64((uint64(v74)) & (uint64(v72))))
	var v76 uint64 = (uint64((uint64(v71)) | (uint64(v75))))
	var v77 uint64 = (uint64((uint64(v76)) << ((uint64(uint64(0x10))) & uint64(0x3f))))
	var v78 uint64 = (uint64((uint64(v74)) << ((uint64(uint64(0x8))) & uint64(0x3f))))
	var v79 uint64 = (uint64((uint64(v74)) & (uint64(v78))))
	var v80 uint64 = (uint64((uint64(v79)) & (uint64(v77))))
	var v81 uint64 = (uint64((uint64(v76)) | (uint64(v80))))
	var v82 uint64 = (uint64((uint64(v81)) << ((uint64(uint64(0x20))) & uint64(0x3f))))
	var v83 uint64 = (uint64((uint64(v79)) << ((uint64(uint64(0x10))) & uint64(0x3f))))
	var v84 uint64 = (uint64((uint64(v79)) & (uint64(v83))))
	var v85 uint64 = (uint64((uint64(v84)) & (uint64(v82))))
	var v86 uint64 = (uint64((uint64(v81)) | (uint64(v85))))
	var v87 uint32 = ((uint32((uint64(v86)) >> 63)) & uint32(0x1))
	var v88 bool = ((uint32(uint32(0x0))) == (uint32(v87)))
	var v89 bool = (!(v88))
	var v90 uint64 = sel64(v89, uint64(uint64(0x0)), uint64(v52))
	var v91 uint64 = (uint64(^(uint64(v90))))
	var v92 uint64 = (uint64((uint64(v91)) | (uint64(v0))))
	var v93 uint64 = (uint64(^(uint64(v92))))
	var v94 uint64 = (uint64((uint64(v93)) ^ (uint64(uint64(0x0)))))
	var v95 uint64 = (uint64((uint64(v94)) >> ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v96 uint64 = (uint64((uint64(v94)) | (uint64(v95))))
	var v97 uint64 = (uint64((uint64(v96)) >> ((uint64(uint64(0x2))) & uint64(0x3f))))
	var v98 uint64 = (uint64((uint64(v96)) | (uint64(v97))))
	var v99 uint64 = (uint64((uint64(v98)) >> ((uint64(uint64(0x4))) & uint64(0x3f))))
	var v100 uint64 = (uint64((uint64(v98)) | (uint64(v99))))
	var v101 uint64 = (uint64((uint64(v100)) >> ((uint64(uint64(0x8))) & uint64(0x3f))))
	var v102 uint64 = (uint64((uint64(v100)) | (uint64(v101))))
	var v103 uint64 = (uint64((uint64(v102)) >> ((uint64(uint64(0x10))) & uint64(0x3f))))
	var v104 uint64 = (uint64((uint64(v102)) | (uint64(v103))))
	var v105 uint64 = (uint64((uint64(v104)) >> ((uint64(uint64(0x20))) & uint64(0x3f))))
	var v106 uint64 = (uint64((uint64(v104)) | (uint64(v105))))
	var v107 uint32 = ((uint32((uint64(v106)) >> 0)) & uint32(0x1))
	var v108 bool = ((uint32(uint32(0x1))) == (uint32(v107)))
	var v109 bool = (!(v108))
	var v110 uint32 = sel32(v109, uint32(uint32(0x0)), uint32(uint32(0x1)))
	var v111 uint32 = v110
	var v112 uint64 = uint64(0x0)
	var v113 uint64 = (uint64(((uint64(v112)) << 1) | (uint64(v111))))
	return uint64(v113)
}

var g0 uint64
var g1 uint8
var sink interface{}

func main() {
	sink = emu_ZBS_IOP__op_BEXTI__rd__go__all_constructed(g0, g1)
	_ = sink
}
