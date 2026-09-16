// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of slliw_gpr_gpr_imm_32__reg_a0__go__all_constructed.
//   Concat(Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 28, v0), Extract(28, 0, v0), 0)
package main

//go:noinline
func emu_slliw_gpr_gpr_imm_32__reg_a0__go__all_constructed(a uint32) uint64 {
	var v0 uint32 = ((uint32((uint32(a)) >> 0)) & uint32(0x1fffffff))
	var v1 uint32 = ((uint32((uint32(a)) >> 28)) & uint32(0x1))
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
	var v36 uint64 = ((uint64(((uint64(v35)) << 29) | (uint64(v3)))) & uint64(0x1fffffffffffffff))
	var v37 uint64 = (uint64(((uint64(v36)) << 3) | (uint64(v2))))
	return uint64(v37)
}

var g0 uint32
var sink interface{}

func main() {
	sink = emu_slliw_gpr_gpr_imm_32__reg_a0__go__all_constructed(g0)
	_ = sink
}
