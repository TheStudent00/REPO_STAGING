// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of SHA512SIG1H__one__rd__go__native_first.
//   
package main

//go:noinline
func emu_SHA512SIG1H__one__rd__go__native_first(a uint64, b uint64) uint64 {
	var v0 uint32 = ((uint32((uint64(a)) >> 6)) & uint32(0x7))
	var v1 uint32 = ((uint32((uint64(b)) >> 29)) & uint32(0x7))
	var v2 uint32 = ((uint32((uint64(a)) >> 19)) & uint32(0x7))
	var v3 uint32 = ((uint32((uint32(v2)) ^ (uint32(v1)) ^ (uint32(v0)))) & uint32(0x7))
	var v4 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0x3ff))
	var v5 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x3ff))
	var v6 uint32 = ((uint32((uint64(a)) >> 22)) & uint32(0x3ff))
	var v7 uint32 = ((uint32((uint64(a)) >> 9)) & uint32(0x3ff))
	var v8 uint32 = ((uint32((uint32(v7)) ^ (uint32(v6)) ^ (uint32(v5)) ^ (uint32(v4)))) & uint32(0x3ff))
	var v9 uint32 = ((uint32((uint64(b)) >> 42)) & uint32(0x3fffff))
	var v10 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x3fffff))
	var v11 uint32 = ((uint32((uint64(a)) >> 19)) & uint32(0x3fffff))
	var v12 uint32 = ((uint32((uint64(a)) >> 10)) & uint32(0x3fffff))
	var v13 uint32 = ((uint32((uint64(b)) >> 0)) & uint32(0x3fffff))
	var v14 uint32 = ((uint32((uint32(v13)) ^ (uint32(v12)) ^ (uint32(v11)) ^ (uint32(v10)) ^ (uint32(v9)))) & uint32(0x3fffff))
	var v15 uint32 = ((uint32((uint64(a)) >> 54)) & uint32(0x3ff))
	var v16 uint32 = ((uint32((uint64(a)) >> 41)) & uint32(0x3ff))
	var v17 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x3ff))
	var v18 uint32 = ((uint32((uint64(b)) >> 22)) & uint32(0x3ff))
	var v19 uint32 = ((uint32((uint32(v18)) ^ (uint32(v17)) ^ (uint32(v16)) ^ (uint32(v15)))) & uint32(0x3ff))
	var v20 uint32 = ((uint32((uint64(a)) >> 51)) & uint32(0x1fff))
	var v21 uint32 = ((uint32((uint64(a)) >> 42)) & uint32(0x1fff))
	var v22 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x1fff))
	var v23 uint32 = ((uint32((uint32(v22)) ^ (uint32(v21)) ^ (uint32(v20)))) & uint32(0x1fff))
	var v24 uint32 = ((uint32((uint64(a)) >> 55)) & uint32(0x3f))
	var v25 uint32 = ((uint32((uint64(b)) >> 45)) & uint32(0x3f))
	var v26 uint32 = ((uint32((uint32(v25)) ^ (uint32(v24)))) & uint32(0x3f))
	var v27 uint64 = (uint64(((uint64(v26)) << 58) | ((uint64(v23)) << 45) | ((uint64(v19)) << 35) | ((uint64(v14)) << 13) | ((uint64(v8)) << 3) | (uint64(v3))))
	return uint64(v27)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_SHA512SIG1H__one__rd__go__native_first(g0, g1)
	_ = sink
}
