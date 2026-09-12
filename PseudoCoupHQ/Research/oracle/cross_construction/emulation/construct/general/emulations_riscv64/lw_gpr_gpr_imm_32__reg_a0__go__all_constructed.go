// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of lw_gpr_gpr_imm_32__reg_a0__go__all_constructed.
//   Concat(Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 31, v0), Extract(31, 0, v0))
package main

//go:noinline
func emu_lw_gpr_gpr_imm_32__reg_a0__go__all_constructed(a uint32) uint64 {
	var v0 uint32 = uint32(a)
	var v1 uint32 = ((uint32((uint32(a)) >> 31)) & uint32(0x1))
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
	var v35 uint64 = (uint64(((uint64(v34)) << 32) | (uint64(v2))))
	return uint64(v35)
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_lw_gpr_gpr_imm_32__reg_a0__go__all_constructed(g0)
	_ = sink
}
