// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of SHA512SIG1L__one__rd__go__native_first.
//   
package main

//go:noinline
func emu_SHA512SIG1L__one__rd__go__native_first(a uint64, b uint64) uint64 {
	var v0 uint32 = ((uint32((uint64(a)) >> 6)) & uint32(0x7))
	var v1 uint32 = ((uint32((uint64(b)) >> 29)) & uint32(0x7))
	var v2 uint32 = ((uint32((uint64(a)) >> 19)) & uint32(0x7))
	var v3 uint32 = ((uint32((uint32(v2)) ^ (uint32(v1)) ^ (uint32(v0)))) & uint32(0x7))
	var v4 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0x3ff))
	var v5 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x3ff))
	var v6 uint32 = ((uint32((uint64(a)) >> 22)) & uint32(0x3ff))
	var v7 uint32 = ((uint32((uint64(a)) >> 9)) & uint32(0x3ff))
	var v8 uint32 = ((uint32((uint32(v7)) ^ (uint32(v6)) ^ (uint32(v5)) ^ (uint32(v4)))) & uint32(0x3ff))
	var v9 uint32 = ((uint32((uint64(b)) >> 42)) & uint32(0x1fff))
	var v10 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x1fff))
	var v11 uint32 = ((uint32((uint64(a)) >> 19)) & uint32(0x1fff))
	var v12 uint32 = ((uint32((uint64(a)) >> 10)) & uint32(0x1fff))
	var v13 uint32 = ((uint32((uint64(b)) >> 0)) & uint32(0x1fff))
	var v14 uint32 = ((uint32((uint32(v13)) ^ (uint32(v12)) ^ (uint32(v11)) ^ (uint32(v10)) ^ (uint32(v9)))) & uint32(0x1fff))
	var v15 uint32 = ((uint32((uint64(b)) >> 0)) & uint32(0x1ff))
	var v16 uint32 = ((uint32((uint64(b)) >> 55)) & uint32(0x1ff))
	var v17 uint32 = ((uint32((uint64(a)) >> 45)) & uint32(0x1ff))
	var v18 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x1ff))
	var v19 uint32 = ((uint32((uint64(a)) >> 23)) & uint32(0x1ff))
	var v20 uint32 = ((uint32((uint64(b)) >> 13)) & uint32(0x1ff))
	var v21 uint32 = ((uint32((uint32(v20)) ^ (uint32(v19)) ^ (uint32(v18)) ^ (uint32(v17)) ^ (uint32(v16)) ^ (uint32(v15)))) & uint32(0x1ff))
	var v22 uint32 = ((uint32((uint64(a)) >> 54)) & uint32(0x3ff))
	var v23 uint32 = ((uint32((uint64(a)) >> 41)) & uint32(0x3ff))
	var v24 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x3ff))
	var v25 uint32 = ((uint32((uint64(b)) >> 22)) & uint32(0x3ff))
	var v26 uint32 = ((uint32((uint64(b)) >> 9)) & uint32(0x3ff))
	var v27 uint32 = ((uint32((uint32(v26)) ^ (uint32(v25)) ^ (uint32(v24)) ^ (uint32(v23)) ^ (uint32(v22)))) & uint32(0x3ff))
	var v28 uint32 = ((uint32((uint64(a)) >> 51)) & uint32(0x1fff))
	var v29 uint32 = ((uint32((uint64(a)) >> 42)) & uint32(0x1fff))
	var v30 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x1fff))
	var v31 uint32 = ((uint32((uint64(b)) >> 19)) & uint32(0x1fff))
	var v32 uint32 = ((uint32((uint32(v31)) ^ (uint32(v30)) ^ (uint32(v29)) ^ (uint32(v28)))) & uint32(0x1fff))
	var v33 uint32 = ((uint32((uint64(a)) >> 55)) & uint32(0x3f))
	var v34 uint32 = ((uint32((uint64(b)) >> 45)) & uint32(0x3f))
	var v35 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x3f))
	var v36 uint32 = ((uint32((uint32(v35)) ^ (uint32(v34)) ^ (uint32(v33)))) & uint32(0x3f))
	var v37 uint64 = (uint64(((uint64(v36)) << 58) | ((uint64(v32)) << 45) | ((uint64(v27)) << 35) | ((uint64(v21)) << 26) | ((uint64(v14)) << 13) | ((uint64(v8)) << 3) | (uint64(v3))))
	return uint64(v37)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_SHA512SIG1L__one__rd__go__native_first(g0, g1)
	_ = sink
}
