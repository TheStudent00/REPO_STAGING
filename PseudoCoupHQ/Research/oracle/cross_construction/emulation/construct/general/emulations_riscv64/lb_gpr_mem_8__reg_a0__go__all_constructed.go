// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of lb_gpr_mem_8__reg_a0__go__all_constructed.
//   Concat(Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), Extract(7, 7, v0), 
package main

//go:noinline
func emu_lb_gpr_mem_8__reg_a0__go__all_constructed(a uint8) uint64 {
	var v0 uint32 = uint32(a)
	var v1 uint32 = ((uint32((uint32(a)) >> 7)) & uint32(0x1))
	var v2 uint32 = v0
	var v3 uint32 = v1
	var v4 uint32 = ((uint32(((uint32(v3)) << 1) | (uint32(v3)))) & uint32(0x3))
	var v5 uint32 = ((uint32(((uint32(v4)) << 1) | (uint32(v3)))) & uint32(0x7))
	var v6 uint32 = ((uint32(((uint32(v5)) << 1) | (uint32(v3)))) & uint32(0xf))
	var v7 uint32 = ((uint32(((uint32(v6)) << 1) | (uint32(v3)))) & uint32(0x1f))
	var v8 uint32 = ((uint32(((uint32(v7)) << 1) | (uint32(v3)))) & uint32(0x3f))
	var v9 uint32 = ((uint32(((uint32(v8)) << 1) | (uint32(v3)))) & uint32(0x7f))
	var v10 uint32 = ((uint32(((uint32(v9)) << 1) | (uint32(v3)))) & uint32(0xff))
	var v11 uint32 = ((uint32(((uint32(v10)) << 1) | (uint32(v3)))) & uint32(0x1ff))
	var v12 uint32 = ((uint32(((uint32(v11)) << 1) | (uint32(v3)))) & uint32(0x3ff))
	var v13 uint32 = ((uint32(((uint32(v12)) << 1) | (uint32(v3)))) & uint32(0x7ff))
	var v14 uint32 = ((uint32(((uint32(v13)) << 1) | (uint32(v3)))) & uint32(0xfff))
	var v15 uint32 = ((uint32(((uint32(v14)) << 1) | (uint32(v3)))) & uint32(0x1fff))
	var v16 uint32 = ((uint32(((uint32(v15)) << 1) | (uint32(v3)))) & uint32(0x3fff))
	var v17 uint32 = ((uint32(((uint32(v16)) << 1) | (uint32(v3)))) & uint32(0x7fff))
	var v18 uint32 = ((uint32(((uint32(v17)) << 1) | (uint32(v3)))) & uint32(0xffff))
	var v19 uint32 = ((uint32(((uint32(v18)) << 1) | (uint32(v3)))) & uint32(0x1ffff))
	var v20 uint32 = ((uint32(((uint32(v19)) << 1) | (uint32(v3)))) & uint32(0x3ffff))
	var v21 uint32 = ((uint32(((uint32(v20)) << 1) | (uint32(v3)))) & uint32(0x7ffff))
	var v22 uint32 = ((uint32(((uint32(v21)) << 1) | (uint32(v3)))) & uint32(0xfffff))
	var v23 uint32 = ((uint32(((uint32(v22)) << 1) | (uint32(v3)))) & uint32(0x1fffff))
	var v24 uint32 = ((uint32(((uint32(v23)) << 1) | (uint32(v3)))) & uint32(0x3fffff))
	var v25 uint32 = ((uint32(((uint32(v24)) << 1) | (uint32(v3)))) & uint32(0x7fffff))
	var v26 uint32 = ((uint32(((uint32(v25)) << 1) | (uint32(v3)))) & uint32(0xffffff))
	var v27 uint32 = ((uint32(((uint32(v26)) << 1) | (uint32(v3)))) & uint32(0x1ffffff))
	var v28 uint32 = ((uint32(((uint32(v27)) << 1) | (uint32(v3)))) & uint32(0x3ffffff))
	var v29 uint32 = ((uint32(((uint32(v28)) << 1) | (uint32(v3)))) & uint32(0x7ffffff))
	var v30 uint32 = ((uint32(((uint32(v29)) << 1) | (uint32(v3)))) & uint32(0xfffffff))
	var v31 uint32 = ((uint32(((uint32(v30)) << 1) | (uint32(v3)))) & uint32(0x1fffffff))
	var v32 uint32 = ((uint32(((uint32(v31)) << 1) | (uint32(v3)))) & uint32(0x3fffffff))
	var v33 uint32 = ((uint32(((uint32(v32)) << 1) | (uint32(v3)))) & uint32(0x7fffffff))
	var v34 uint32 = (uint32(((uint32(v33)) << 1) | (uint32(v3))))
	var v35 uint64 = ((uint64(((uint64(v34)) << 1) | (uint64(v3)))) & uint64(0x1ffffffff))
	var v36 uint64 = ((uint64(((uint64(v35)) << 1) | (uint64(v3)))) & uint64(0x3ffffffff))
	var v37 uint64 = ((uint64(((uint64(v36)) << 1) | (uint64(v3)))) & uint64(0x7ffffffff))
	var v38 uint64 = ((uint64(((uint64(v37)) << 1) | (uint64(v3)))) & uint64(0xfffffffff))
	var v39 uint64 = ((uint64(((uint64(v38)) << 1) | (uint64(v3)))) & uint64(0x1fffffffff))
	var v40 uint64 = ((uint64(((uint64(v39)) << 1) | (uint64(v3)))) & uint64(0x3fffffffff))
	var v41 uint64 = ((uint64(((uint64(v40)) << 1) | (uint64(v3)))) & uint64(0x7fffffffff))
	var v42 uint64 = ((uint64(((uint64(v41)) << 1) | (uint64(v3)))) & uint64(0xffffffffff))
	var v43 uint64 = ((uint64(((uint64(v42)) << 1) | (uint64(v3)))) & uint64(0x1ffffffffff))
	var v44 uint64 = ((uint64(((uint64(v43)) << 1) | (uint64(v3)))) & uint64(0x3ffffffffff))
	var v45 uint64 = ((uint64(((uint64(v44)) << 1) | (uint64(v3)))) & uint64(0x7ffffffffff))
	var v46 uint64 = ((uint64(((uint64(v45)) << 1) | (uint64(v3)))) & uint64(0xfffffffffff))
	var v47 uint64 = ((uint64(((uint64(v46)) << 1) | (uint64(v3)))) & uint64(0x1fffffffffff))
	var v48 uint64 = ((uint64(((uint64(v47)) << 1) | (uint64(v3)))) & uint64(0x3fffffffffff))
	var v49 uint64 = ((uint64(((uint64(v48)) << 1) | (uint64(v3)))) & uint64(0x7fffffffffff))
	var v50 uint64 = ((uint64(((uint64(v49)) << 1) | (uint64(v3)))) & uint64(0xffffffffffff))
	var v51 uint64 = ((uint64(((uint64(v50)) << 1) | (uint64(v3)))) & uint64(0x1ffffffffffff))
	var v52 uint64 = ((uint64(((uint64(v51)) << 1) | (uint64(v3)))) & uint64(0x3ffffffffffff))
	var v53 uint64 = ((uint64(((uint64(v52)) << 1) | (uint64(v3)))) & uint64(0x7ffffffffffff))
	var v54 uint64 = ((uint64(((uint64(v53)) << 1) | (uint64(v3)))) & uint64(0xfffffffffffff))
	var v55 uint64 = ((uint64(((uint64(v54)) << 1) | (uint64(v3)))) & uint64(0x1fffffffffffff))
	var v56 uint64 = ((uint64(((uint64(v55)) << 1) | (uint64(v3)))) & uint64(0x3fffffffffffff))
	var v57 uint64 = ((uint64(((uint64(v56)) << 1) | (uint64(v3)))) & uint64(0x7fffffffffffff))
	var v58 uint64 = ((uint64(((uint64(v57)) << 1) | (uint64(v3)))) & uint64(0xffffffffffffff))
	var v59 uint64 = (uint64(((uint64(v58)) << 8) | (uint64(v2))))
	return uint64(v59)
}

var g0 uint8
var sink interface{}

func main() {
	sink = emu_lb_gpr_mem_8__reg_a0__go__all_constructed(g0)
	_ = sink
}
