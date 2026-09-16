// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of SHA512SUM0R__one__rd__go__native_first.
//   
package main

//go:noinline
func emu_SHA512SUM0R__one__rd__go__native_first(a uint64, b uint64) uint64 {
	var v0 uint32 = ((uint32((uint64(b)) >> 2)) & uint32(0xf))
	var v1 uint32 = ((uint32((uint64(a)) >> 28)) & uint32(0xf))
	var v2 uint32 = ((uint32((uint64(b)) >> 7)) & uint32(0xf))
	var v3 uint32 = ((uint32((uint32(v2)) ^ (uint32(v1)) ^ (uint32(v0)))) & uint32(0xf))
	var v4 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x1fffff))
	var v5 uint32 = ((uint32((uint64(b)) >> 11)) & uint32(0x1fffff))
	var v6 uint32 = ((uint32((uint64(b)) >> 6)) & uint32(0x1fffff))
	var v7 uint32 = ((uint32((uint64(b)) >> 0)) & uint32(0x1fffff))
	var v8 uint32 = ((uint32((uint32(v7)) ^ (uint32(v6)) ^ (uint32(v5)) ^ (uint32(v4)))) & uint32(0x1fffff))
	var v9 uint32 = ((uint32((uint64(a)) >> 53)) & uint32(0x1f))
	var v10 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0x1f))
	var v11 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x1f))
	var v12 uint32 = ((uint32((uint64(b)) >> 27)) & uint32(0x1f))
	var v13 uint32 = ((uint32((uint64(b)) >> 21)) & uint32(0x1f))
	var v14 uint32 = ((uint32((uint32(v13)) ^ (uint32(v12)) ^ (uint32(v11)) ^ (uint32(v10)) ^ (uint32(v9)))) & uint32(0x1f))
	var v15 uint32 = ((uint32((uint64(a)) >> 58)) & uint32(0x3f))
	var v16 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0x3f))
	var v17 uint32 = ((uint32((uint64(b)) >> 37)) & uint32(0x3f))
	var v18 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x3f))
	var v19 uint32 = ((uint32((uint64(b)) >> 26)) & uint32(0x3f))
	var v20 uint32 = ((uint32((uint64(a)) >> 5)) & uint32(0x3f))
	var v21 uint32 = ((uint32((uint32(v20)) ^ (uint32(v19)) ^ (uint32(v18)) ^ (uint32(v17)) ^ (uint32(v16)) ^ (uint32(v15)))) & uint32(0x3f))
	var v22 uint32 = ((uint32((uint64(b)) >> 43)) & uint32(0x1fffff))
	var v23 uint32 = ((uint32((uint64(b)) >> 38)) & uint32(0x1fffff))
	var v24 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x1fffff))
	var v25 uint32 = ((uint32((uint64(a)) >> 11)) & uint32(0x1fffff))
	var v26 uint32 = ((uint32((uint64(a)) >> 6)) & uint32(0x1fffff))
	var v27 uint32 = ((uint32((uint32(v26)) ^ (uint32(v25)) ^ (uint32(v24)) ^ (uint32(v23)) ^ (uint32(v22)))) & uint32(0x1fffff))
	var v28 uint32 = ((uint32((uint64(b)) >> 59)) & uint32(0x1f))
	var v29 uint32 = ((uint32((uint64(b)) >> 53)) & uint32(0x1f))
	var v30 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x1f))
	var v31 uint32 = ((uint32((uint64(a)) >> 27)) & uint32(0x1f))
	var v32 uint32 = ((uint32((uint32(v31)) ^ (uint32(v30)) ^ (uint32(v29)) ^ (uint32(v28)))) & uint32(0x1f))
	var v33 uint32 = ((uint32((uint64(b)) >> 58)) & uint32(0x3))
	var v34 uint32 = ((uint32((uint64(a)) >> 37)) & uint32(0x3))
	var v35 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x3))
	var v36 uint32 = ((uint32((uint32(v35)) ^ (uint32(v34)) ^ (uint32(v33)))) & uint32(0x3))
	var v37 uint64 = (uint64(((uint64(v36)) << 62) | ((uint64(v32)) << 57) | ((uint64(v27)) << 36) | ((uint64(v21)) << 30) | ((uint64(v14)) << 25) | ((uint64(v8)) << 4) | (uint64(v3))))
	return uint64(v37)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_SHA512SUM0R__one__rd__go__native_first(g0, g1)
	_ = sink
}
