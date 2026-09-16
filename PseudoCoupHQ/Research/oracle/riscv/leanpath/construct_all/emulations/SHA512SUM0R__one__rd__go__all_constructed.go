// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of SHA512SUM0R__one__rd__go__all_constructed.
//   
package main

//go:noinline
func emu_SHA512SUM0R__one__rd__go__all_constructed(a uint64, b uint64) uint64 {
	var v0 uint32 = ((uint32((uint64(b)) >> 2)) & uint32(0xf))
	var v1 uint32 = ((uint32((uint64(a)) >> 28)) & uint32(0xf))
	var v2 uint32 = ((uint32((uint64(b)) >> 7)) & uint32(0xf))
	var v3 uint32 = ((uint32((uint32(v2)) ^ (uint32(v1)))) & uint32(0xf))
	var v4 uint32 = ((uint32((uint32(v3)) ^ (uint32(v0)))) & uint32(0xf))
	var v5 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x1fffff))
	var v6 uint32 = ((uint32((uint64(b)) >> 11)) & uint32(0x1fffff))
	var v7 uint32 = ((uint32((uint64(b)) >> 6)) & uint32(0x1fffff))
	var v8 uint32 = ((uint32((uint64(b)) >> 0)) & uint32(0x1fffff))
	var v9 uint32 = ((uint32((uint32(v8)) ^ (uint32(v7)))) & uint32(0x1fffff))
	var v10 uint32 = ((uint32((uint32(v9)) ^ (uint32(v6)))) & uint32(0x1fffff))
	var v11 uint32 = ((uint32((uint32(v10)) ^ (uint32(v5)))) & uint32(0x1fffff))
	var v12 uint32 = ((uint32((uint64(a)) >> 53)) & uint32(0x1f))
	var v13 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0x1f))
	var v14 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x1f))
	var v15 uint32 = ((uint32((uint64(b)) >> 27)) & uint32(0x1f))
	var v16 uint32 = ((uint32((uint64(b)) >> 21)) & uint32(0x1f))
	var v17 uint32 = ((uint32((uint32(v16)) ^ (uint32(v15)))) & uint32(0x1f))
	var v18 uint32 = ((uint32((uint32(v17)) ^ (uint32(v14)))) & uint32(0x1f))
	var v19 uint32 = ((uint32((uint32(v18)) ^ (uint32(v13)))) & uint32(0x1f))
	var v20 uint32 = ((uint32((uint32(v19)) ^ (uint32(v12)))) & uint32(0x1f))
	var v21 uint32 = ((uint32((uint64(a)) >> 58)) & uint32(0x3f))
	var v22 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0x3f))
	var v23 uint32 = ((uint32((uint64(b)) >> 37)) & uint32(0x3f))
	var v24 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x3f))
	var v25 uint32 = ((uint32((uint64(b)) >> 26)) & uint32(0x3f))
	var v26 uint32 = ((uint32((uint64(a)) >> 5)) & uint32(0x3f))
	var v27 uint32 = ((uint32((uint32(v26)) ^ (uint32(v25)))) & uint32(0x3f))
	var v28 uint32 = ((uint32((uint32(v27)) ^ (uint32(v24)))) & uint32(0x3f))
	var v29 uint32 = ((uint32((uint32(v28)) ^ (uint32(v23)))) & uint32(0x3f))
	var v30 uint32 = ((uint32((uint32(v29)) ^ (uint32(v22)))) & uint32(0x3f))
	var v31 uint32 = ((uint32((uint32(v30)) ^ (uint32(v21)))) & uint32(0x3f))
	var v32 uint32 = ((uint32((uint64(b)) >> 43)) & uint32(0x1fffff))
	var v33 uint32 = ((uint32((uint64(b)) >> 38)) & uint32(0x1fffff))
	var v34 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x1fffff))
	var v35 uint32 = ((uint32((uint64(a)) >> 11)) & uint32(0x1fffff))
	var v36 uint32 = ((uint32((uint64(a)) >> 6)) & uint32(0x1fffff))
	var v37 uint32 = ((uint32((uint32(v36)) ^ (uint32(v35)))) & uint32(0x1fffff))
	var v38 uint32 = ((uint32((uint32(v37)) ^ (uint32(v34)))) & uint32(0x1fffff))
	var v39 uint32 = ((uint32((uint32(v38)) ^ (uint32(v33)))) & uint32(0x1fffff))
	var v40 uint32 = ((uint32((uint32(v39)) ^ (uint32(v32)))) & uint32(0x1fffff))
	var v41 uint32 = ((uint32((uint64(b)) >> 59)) & uint32(0x1f))
	var v42 uint32 = ((uint32((uint64(b)) >> 53)) & uint32(0x1f))
	var v43 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x1f))
	var v44 uint32 = ((uint32((uint64(a)) >> 27)) & uint32(0x1f))
	var v45 uint32 = ((uint32((uint32(v44)) ^ (uint32(v43)))) & uint32(0x1f))
	var v46 uint32 = ((uint32((uint32(v45)) ^ (uint32(v42)))) & uint32(0x1f))
	var v47 uint32 = ((uint32((uint32(v46)) ^ (uint32(v41)))) & uint32(0x1f))
	var v48 uint32 = ((uint32((uint64(b)) >> 58)) & uint32(0x3))
	var v49 uint32 = ((uint32((uint64(a)) >> 37)) & uint32(0x3))
	var v50 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x3))
	var v51 uint32 = ((uint32((uint32(v50)) ^ (uint32(v49)))) & uint32(0x3))
	var v52 uint32 = ((uint32((uint32(v51)) ^ (uint32(v48)))) & uint32(0x3))
	var v53 uint32 = v4
	var v54 uint32 = v11
	var v55 uint32 = v20
	var v56 uint32 = v31
	var v57 uint32 = v40
	var v58 uint32 = v47
	var v59 uint32 = v52
	var v60 uint32 = ((uint32(((uint32(v59)) << 5) | (uint32(v58)))) & uint32(0x7f))
	var v61 uint32 = ((uint32(((uint32(v60)) << 21) | (uint32(v57)))) & uint32(0xfffffff))
	var v62 uint64 = ((uint64(((uint64(v61)) << 6) | (uint64(v56)))) & uint64(0x3ffffffff))
	var v63 uint64 = ((uint64(((uint64(v62)) << 5) | (uint64(v55)))) & uint64(0x7fffffffff))
	var v64 uint64 = ((uint64(((uint64(v63)) << 21) | (uint64(v54)))) & uint64(0xfffffffffffffff))
	var v65 uint64 = (uint64(((uint64(v64)) << 4) | (uint64(v53))))
	return uint64(v65)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_SHA512SUM0R__one__rd__go__all_constructed(g0, g1)
	_ = sink
}
