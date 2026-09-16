// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of SHA512SUM1R__one__rd__go__native_first.
//   
package main

//go:noinline
func emu_SHA512SUM1R__one__rd__go__native_first(a uint64, b uint64) uint64 {
	var v0 uint32 = ((uint32((uint64(a)) >> 18)) & uint32(0x3fff))
	var v1 uint32 = ((uint32((uint64(a)) >> 14)) & uint32(0x3fff))
	var v2 uint32 = ((uint32((uint64(b)) >> 9)) & uint32(0x3fff))
	var v3 uint32 = ((uint32((uint32(v2)) ^ (uint32(v1)) ^ (uint32(v0)))) & uint32(0x3fff))
	var v4 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0xf))
	var v5 uint32 = ((uint32((uint64(a)) >> 28)) & uint32(0xf))
	var v6 uint32 = ((uint32((uint64(b)) >> 0)) & uint32(0xf))
	var v7 uint32 = ((uint32((uint64(b)) >> 23)) & uint32(0xf))
	var v8 uint32 = ((uint32((uint32(v7)) ^ (uint32(v6)) ^ (uint32(v5)) ^ (uint32(v4)))) & uint32(0xf))
	var v9 uint32 = ((uint32((uint64(b)) >> 4)) & uint32(0x1f))
	var v10 uint32 = ((uint32((uint64(a)) >> 36)) & uint32(0x1f))
	var v11 uint32 = ((uint32((uint64(b)) >> 0)) & uint32(0x1f))
	var v12 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x1f))
	var v13 uint32 = ((uint32((uint64(b)) >> 27)) & uint32(0x1f))
	var v14 uint32 = ((uint32((uint32(v13)) ^ (uint32(v12)) ^ (uint32(v11)) ^ (uint32(v10)) ^ (uint32(v9)))) & uint32(0x1f))
	var v15 uint32 = ((uint32((uint64(a)) >> 41)) & uint32(0x7fffff))
	var v16 uint32 = ((uint32((uint64(a)) >> 37)) & uint32(0x7fffff))
	var v17 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x7fffff))
	var v18 uint32 = ((uint32((uint64(b)) >> 9)) & uint32(0x7fffff))
	var v19 uint32 = ((uint32((uint64(b)) >> 5)) & uint32(0x7fffff))
	var v20 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0x7fffff))
	var v21 uint32 = ((uint32((uint32(v20)) ^ (uint32(v19)) ^ (uint32(v18)) ^ (uint32(v17)) ^ (uint32(v16)) ^ (uint32(v15)))) & uint32(0x7fffff))
	var v22 uint32 = ((uint32((uint64(a)) >> 60)) & uint32(0xf))
	var v23 uint32 = ((uint32((uint64(b)) >> 55)) & uint32(0xf))
	var v24 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0xf))
	var v25 uint32 = ((uint32((uint64(b)) >> 28)) & uint32(0xf))
	var v26 uint32 = ((uint32((uint64(a)) >> 23)) & uint32(0xf))
	var v27 uint32 = ((uint32((uint32(v26)) ^ (uint32(v25)) ^ (uint32(v24)) ^ (uint32(v23)) ^ (uint32(v22)))) & uint32(0xf))
	var v28 uint32 = ((uint32((uint64(b)) >> 59)) & uint32(0x1f))
	var v29 uint32 = ((uint32((uint64(b)) >> 36)) & uint32(0x1f))
	var v30 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x1f))
	var v31 uint32 = ((uint32((uint64(a)) >> 27)) & uint32(0x1f))
	var v32 uint32 = ((uint32((uint32(v31)) ^ (uint32(v30)) ^ (uint32(v29)) ^ (uint32(v28)))) & uint32(0x1f))
	var v33 uint32 = ((uint32((uint64(b)) >> 41)) & uint32(0x1ff))
	var v34 uint32 = ((uint32((uint64(b)) >> 37)) & uint32(0x1ff))
	var v35 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x1ff))
	var v36 uint32 = ((uint32((uint32(v35)) ^ (uint32(v34)) ^ (uint32(v33)))) & uint32(0x1ff))
	var v37 uint64 = (uint64(((uint64(v36)) << 55) | ((uint64(v32)) << 50) | ((uint64(v27)) << 46) | ((uint64(v21)) << 23) | ((uint64(v14)) << 18) | ((uint64(v8)) << 14) | (uint64(v3))))
	return uint64(v37)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_SHA512SUM1R__one__rd__go__native_first(g0, g1)
	_ = sink
}
