// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of SHA512SIG0H__one__rd__go__all_constructed.
//   
package main

//go:noinline
func emu_SHA512SIG0H__one__rd__go__all_constructed(a uint64, b uint64) uint64 {
	var v0 uint32 = ((uint32((uint64(a)) >> 8)) & uint32(0xffffff))
	var v1 uint32 = ((uint32((uint64(a)) >> 7)) & uint32(0xffffff))
	var v2 uint32 = ((uint32((uint64(a)) >> 1)) & uint32(0xffffff))
	var v3 uint32 = ((uint32((uint32(v2)) ^ (uint32(v1)))) & uint32(0xffffff))
	var v4 uint32 = ((uint32((uint32(v3)) ^ (uint32(v0)))) & uint32(0xffffff))
	var v5 uint32 = ((uint32((uint64(b)) >> 0)) & uint32(0x7f))
	var v6 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x7f))
	var v7 uint32 = ((uint32((uint64(a)) >> 31)) & uint32(0x7f))
	var v8 uint32 = ((uint32((uint64(a)) >> 25)) & uint32(0x7f))
	var v9 uint32 = ((uint32((uint32(v8)) ^ (uint32(v7)))) & uint32(0x7f))
	var v10 uint32 = ((uint32((uint32(v9)) ^ (uint32(v6)))) & uint32(0x7f))
	var v11 uint32 = ((uint32((uint32(v10)) ^ (uint32(v5)))) & uint32(0x7f))
	var v12 uint32 = ((uint32((uint64(a)) >> 39)) & uint32(0x1ffffff))
	var v13 uint32 = ((uint32((uint64(a)) >> 38)) & uint32(0x1ffffff))
	var v14 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x1ffffff))
	var v15 uint32 = ((uint32((uint64(b)) >> 7)) & uint32(0x1ffffff))
	var v16 uint32 = ((uint32((uint64(b)) >> 0)) & uint32(0x1ffffff))
	var v17 uint32 = ((uint32((uint32(v16)) ^ (uint32(v15)))) & uint32(0x1ffffff))
	var v18 uint32 = ((uint32((uint32(v17)) ^ (uint32(v14)))) & uint32(0x1ffffff))
	var v19 uint32 = ((uint32((uint32(v18)) ^ (uint32(v13)))) & uint32(0x1ffffff))
	var v20 uint32 = ((uint32((uint32(v19)) ^ (uint32(v12)))) & uint32(0x1ffffff))
	var v21 uint32 = ((uint32((uint64(a)) >> 63)) & uint32(0x1))
	var v22 uint32 = ((uint32((uint64(a)) >> 57)) & uint32(0x1))
	var v23 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x1))
	var v24 uint32 = ((uint32((uint64(b)) >> 25)) & uint32(0x1))
	var v25 uint32 = ((uint32((uint32(v24)) ^ (uint32(v23)))) & uint32(0x1))
	var v26 uint32 = ((uint32((uint32(v25)) ^ (uint32(v22)))) & uint32(0x1))
	var v27 uint32 = ((uint32((uint32(v26)) ^ (uint32(v21)))) & uint32(0x1))
	var v28 uint32 = ((uint32((uint64(a)) >> 58)) & uint32(0x3f))
	var v29 uint32 = ((uint32((uint64(b)) >> 33)) & uint32(0x3f))
	var v30 uint32 = ((uint32((uint64(b)) >> 26)) & uint32(0x3f))
	var v31 uint32 = ((uint32((uint32(v30)) ^ (uint32(v29)))) & uint32(0x3f))
	var v32 uint32 = ((uint32((uint32(v31)) ^ (uint32(v28)))) & uint32(0x3f))
	var v33 uint32 = ((uint32((uint64(b)) >> 39)) & uint32(0x1))
	var v34 uint32 = ((uint32((uint32(v23)) ^ (uint32(v33)))) & uint32(0x1))
	var v35 uint32 = v4
	var v36 uint32 = v11
	var v37 uint32 = v20
	var v38 uint32 = v27
	var v39 uint32 = v32
	var v40 uint32 = v34
	var v41 uint32 = ((uint32(((uint32(v40)) << 6) | (uint32(v39)))) & uint32(0x7f))
	var v42 uint32 = ((uint32(((uint32(v41)) << 1) | (uint32(v38)))) & uint32(0xff))
	var v43 uint64 = ((uint64(((uint64(v42)) << 25) | (uint64(v37)))) & uint64(0x1ffffffff))
	var v44 uint64 = ((uint64(((uint64(v43)) << 7) | (uint64(v36)))) & uint64(0xffffffffff))
	var v45 uint64 = (uint64(((uint64(v44)) << 24) | (uint64(v35))))
	return uint64(v45)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_SHA512SIG0H__one__rd__go__all_constructed(g0, g1)
	_ = sink
}
