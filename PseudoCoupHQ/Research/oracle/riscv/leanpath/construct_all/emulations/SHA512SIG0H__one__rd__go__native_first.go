// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of SHA512SIG0H__one__rd__go__native_first.
//   
package main

//go:noinline
func emu_SHA512SIG0H__one__rd__go__native_first(a uint64, b uint64) uint64 {
	var v0 uint32 = ((uint32((uint64(a)) >> 8)) & uint32(0xffffff))
	var v1 uint32 = ((uint32((uint64(a)) >> 7)) & uint32(0xffffff))
	var v2 uint32 = ((uint32((uint64(a)) >> 1)) & uint32(0xffffff))
	var v3 uint32 = ((uint32((uint32(v2)) ^ (uint32(v1)) ^ (uint32(v0)))) & uint32(0xffffff))
	var v4 uint32 = ((uint32((uint64(b)) >> 0)) & uint32(0x7f))
	var v5 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x7f))
	var v6 uint32 = ((uint32((uint64(a)) >> 31)) & uint32(0x7f))
	var v7 uint32 = ((uint32((uint64(a)) >> 25)) & uint32(0x7f))
	var v8 uint32 = ((uint32((uint32(v7)) ^ (uint32(v6)) ^ (uint32(v5)) ^ (uint32(v4)))) & uint32(0x7f))
	var v9 uint32 = ((uint32((uint64(a)) >> 39)) & uint32(0x1ffffff))
	var v10 uint32 = ((uint32((uint64(a)) >> 38)) & uint32(0x1ffffff))
	var v11 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0x1ffffff))
	var v12 uint32 = ((uint32((uint64(b)) >> 7)) & uint32(0x1ffffff))
	var v13 uint32 = ((uint32((uint64(b)) >> 0)) & uint32(0x1ffffff))
	var v14 uint32 = ((uint32((uint32(v13)) ^ (uint32(v12)) ^ (uint32(v11)) ^ (uint32(v10)) ^ (uint32(v9)))) & uint32(0x1ffffff))
	var v15 uint32 = ((uint32((uint64(a)) >> 63)) & uint32(0x1))
	var v16 uint32 = ((uint32((uint64(a)) >> 57)) & uint32(0x1))
	var v17 uint32 = ((uint32((uint64(b)) >> 32)) & uint32(0x1))
	var v18 uint32 = ((uint32((uint64(b)) >> 25)) & uint32(0x1))
	var v19 uint32 = ((uint32((uint32(v18)) ^ (uint32(v17)) ^ (uint32(v16)) ^ (uint32(v15)))) & uint32(0x1))
	var v20 uint32 = ((uint32((uint64(a)) >> 58)) & uint32(0x3f))
	var v21 uint32 = ((uint32((uint64(b)) >> 33)) & uint32(0x3f))
	var v22 uint32 = ((uint32((uint64(b)) >> 26)) & uint32(0x3f))
	var v23 uint32 = ((uint32((uint32(v22)) ^ (uint32(v21)) ^ (uint32(v20)))) & uint32(0x3f))
	var v24 uint32 = ((uint32((uint64(b)) >> 39)) & uint32(0x1))
	var v25 uint32 = ((uint32((uint32(v17)) ^ (uint32(v24)))) & uint32(0x1))
	var v26 uint64 = (uint64(((uint64(v25)) << 63) | ((uint64(v23)) << 57) | ((uint64(v19)) << 56) | ((uint64(v14)) << 31) | ((uint64(v8)) << 24) | (uint64(v3))))
	return uint64(v26)
}

var g0 uint64
var g1 uint64
var sink interface{}

func main() {
	sink = emu_SHA512SIG0H__one__rd__go__native_first(g0, g1)
	_ = sink
}
