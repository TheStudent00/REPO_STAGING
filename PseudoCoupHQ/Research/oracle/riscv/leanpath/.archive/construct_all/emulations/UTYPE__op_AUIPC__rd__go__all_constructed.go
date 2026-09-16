// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of UTYPE__op_AUIPC__rd__go__all_constructed.
//   
package main

//go:noinline
func emu_UTYPE__op_AUIPC__rd__go__all_constructed(a uint64, b uint32) uint64 {
	var v0 uint32 = ((uint32((uint32(b)) >> 0)) & uint32(0xfffff))
	var v1 uint32 = ((uint32((uint32(b)) >> 19)) & uint32(0x1))
	var v2 uint32 = uint32(0x0)
	var v3 uint32 = v0
	var v4 uint32 = v1
	var v5 uint32 = ((uint32(((uint32(v4)) << 1) | (uint32(v4)))) & uint32(0x3))
	var v6 uint32 = ((uint32(((uint32(v5)) << 1) | (uint32(v4)))) & uint32(0x7))
	var v7 uint32 = ((uint32(((uint32(v6)) << 1) | (uint32(v4)))) & uint32(0xf))
	var v8 uint32 = ((uint32(((uint32(v7)) << 1) | (uint32(v4)))) & uint32(0x1f))
	var v9 uint32 = ((uint32(((uint32(v8)) << 1) | (uint32(v4)))) & uint32(0x3f))
	var v10 uint32 = ((uint32(((uint32(v9)) << 1) | (uint32(v4)))) & uint32(0x7f))
	var v11 uint32 = ((uint32(((uint32(v10)) << 1) | (uint32(v4)))) & uint32(0xff))
	var v12 uint32 = ((uint32(((uint32(v11)) << 1) | (uint32(v4)))) & uint32(0x1ff))
	var v13 uint32 = ((uint32(((uint32(v12)) << 1) | (uint32(v4)))) & uint32(0x3ff))
	var v14 uint32 = ((uint32(((uint32(v13)) << 1) | (uint32(v4)))) & uint32(0x7ff))
	var v15 uint32 = ((uint32(((uint32(v14)) << 1) | (uint32(v4)))) & uint32(0xfff))
	var v16 uint32 = ((uint32(((uint32(v15)) << 1) | (uint32(v4)))) & uint32(0x1fff))
	var v17 uint32 = ((uint32(((uint32(v16)) << 1) | (uint32(v4)))) & uint32(0x3fff))
	var v18 uint32 = ((uint32(((uint32(v17)) << 1) | (uint32(v4)))) & uint32(0x7fff))
	var v19 uint32 = ((uint32(((uint32(v18)) << 1) | (uint32(v4)))) & uint32(0xffff))
	var v20 uint32 = ((uint32(((uint32(v19)) << 1) | (uint32(v4)))) & uint32(0x1ffff))
	var v21 uint32 = ((uint32(((uint32(v20)) << 1) | (uint32(v4)))) & uint32(0x3ffff))
	var v22 uint32 = ((uint32(((uint32(v21)) << 1) | (uint32(v4)))) & uint32(0x7ffff))
	var v23 uint32 = ((uint32(((uint32(v22)) << 1) | (uint32(v4)))) & uint32(0xfffff))
	var v24 uint32 = ((uint32(((uint32(v23)) << 1) | (uint32(v4)))) & uint32(0x1fffff))
	var v25 uint32 = ((uint32(((uint32(v24)) << 1) | (uint32(v4)))) & uint32(0x3fffff))
	var v26 uint32 = ((uint32(((uint32(v25)) << 1) | (uint32(v4)))) & uint32(0x7fffff))
	var v27 uint32 = ((uint32(((uint32(v26)) << 1) | (uint32(v4)))) & uint32(0xffffff))
	var v28 uint32 = ((uint32(((uint32(v27)) << 1) | (uint32(v4)))) & uint32(0x1ffffff))
	var v29 uint32 = ((uint32(((uint32(v28)) << 1) | (uint32(v4)))) & uint32(0x3ffffff))
	var v30 uint32 = ((uint32(((uint32(v29)) << 1) | (uint32(v4)))) & uint32(0x7ffffff))
	var v31 uint32 = ((uint32(((uint32(v30)) << 1) | (uint32(v4)))) & uint32(0xfffffff))
	var v32 uint32 = ((uint32(((uint32(v31)) << 1) | (uint32(v4)))) & uint32(0x1fffffff))
	var v33 uint32 = ((uint32(((uint32(v32)) << 1) | (uint32(v4)))) & uint32(0x3fffffff))
	var v34 uint32 = ((uint32(((uint32(v33)) << 1) | (uint32(v4)))) & uint32(0x7fffffff))
	var v35 uint32 = (uint32(((uint32(v34)) << 1) | (uint32(v4))))
	var v36 uint64 = ((uint64(((uint64(v35)) << 20) | (uint64(v3)))) & uint64(0xfffffffffffff))
	var v37 uint64 = (uint64(((uint64(v36)) << 12) | (uint64(v2))))
	var v38 uint64 = (uint64((uint64(v37)) & (uint64(uint64(a)))))
	var v39 uint64 = (uint64((uint64(v38)) << ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v40 uint64 = (uint64((uint64(v37)) ^ (uint64(uint64(a)))))
	var v41 uint64 = (uint64((uint64(v40)) & (uint64(v39))))
	var v42 uint64 = (uint64((uint64(v38)) | (uint64(v41))))
	var v43 uint64 = (uint64((uint64(v42)) << ((uint64(uint64(0x2))) & uint64(0x3f))))
	var v44 uint64 = (uint64((uint64(v40)) << ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v45 uint64 = (uint64((uint64(v40)) & (uint64(v44))))
	var v46 uint64 = (uint64((uint64(v45)) & (uint64(v43))))
	var v47 uint64 = (uint64((uint64(v42)) | (uint64(v46))))
	var v48 uint64 = (uint64((uint64(v47)) << ((uint64(uint64(0x4))) & uint64(0x3f))))
	var v49 uint64 = (uint64((uint64(v45)) << ((uint64(uint64(0x2))) & uint64(0x3f))))
	var v50 uint64 = (uint64((uint64(v45)) & (uint64(v49))))
	var v51 uint64 = (uint64((uint64(v50)) & (uint64(v48))))
	var v52 uint64 = (uint64((uint64(v47)) | (uint64(v51))))
	var v53 uint64 = (uint64((uint64(v52)) << ((uint64(uint64(0x8))) & uint64(0x3f))))
	var v54 uint64 = (uint64((uint64(v50)) << ((uint64(uint64(0x4))) & uint64(0x3f))))
	var v55 uint64 = (uint64((uint64(v50)) & (uint64(v54))))
	var v56 uint64 = (uint64((uint64(v55)) & (uint64(v53))))
	var v57 uint64 = (uint64((uint64(v52)) | (uint64(v56))))
	var v58 uint64 = (uint64((uint64(v57)) << ((uint64(uint64(0x10))) & uint64(0x3f))))
	var v59 uint64 = (uint64((uint64(v55)) << ((uint64(uint64(0x8))) & uint64(0x3f))))
	var v60 uint64 = (uint64((uint64(v55)) & (uint64(v59))))
	var v61 uint64 = (uint64((uint64(v60)) & (uint64(v58))))
	var v62 uint64 = (uint64((uint64(v57)) | (uint64(v61))))
	var v63 uint64 = (uint64((uint64(v62)) << ((uint64(uint64(0x20))) & uint64(0x3f))))
	var v64 uint64 = (uint64((uint64(v60)) << ((uint64(uint64(0x10))) & uint64(0x3f))))
	var v65 uint64 = (uint64((uint64(v60)) & (uint64(v64))))
	var v66 uint64 = (uint64((uint64(v65)) & (uint64(v63))))
	var v67 uint64 = (uint64((uint64(v62)) | (uint64(v66))))
	var v68 uint64 = (uint64((uint64(v67)) << ((uint64(uint64(0x1))) & uint64(0x3f))))
	var v69 uint64 = (uint64((uint64(v40)) ^ (uint64(v68))))
	return uint64(v69)
}

var g0 uint64
var g1 uint32
var sink interface{}

func main() {
	sink = emu_UTYPE__op_AUIPC__rd__go__all_constructed(g0, g1)
	_ = sink
}
