// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ITYPE__op_ORI__rd__go__native_first.
//   
package main

//go:noinline
func emu_ITYPE__op_ORI__rd__go__native_first(a uint64, b uint16) uint64 {
	var v0 uint64 = ((uint64((uint64(a)) >> 0)) & uint64(0x3fffffffffffffff))
	var v1 uint32 = ((uint32((uint32(b)) >> 0)) & uint32(0xfff))
	var v2 uint32 = ((uint32((uint32(b)) >> 11)) & uint32(0x1))
	var v3 uint64 = ((uint64(((uint64(v2)) << 61) | ((uint64(v2)) << 60) | ((uint64(v2)) << 59) | ((uint64(v2)) << 58) | ((uint64(v2)) << 57) | ((uint64(v2)) << 56) | ((uint64(v2)) << 55) | ((uint64(v2)) << 54) | ((uint64(v2)) << 53) | ((uint64(v2)) << 52) | ((uint64(v2)) << 51) | ((uint64(v2)) << 50) | ((uint64(v2)) << 49) | ((uint64(v2)) << 48) | ((uint64(v2)) << 47) | ((uint64(v2)) << 46) | ((uint64(v2)) << 45) | ((uint64(v2)) << 44) | ((uint64(v2)) << 43) | ((uint64(v2)) << 42) | ((uint64(v2)) << 41) | ((uint64(v2)) << 40) | ((uint64(v2)) << 39) | ((uint64(v2)) << 38) | ((uint64(v2)) << 37) | ((uint64(v2)) << 36) | ((uint64(v2)) << 35) | ((uint64(v2)) << 34) | ((uint64(v2)) << 33) | ((uint64(v2)) << 32) | ((uint64(v2)) << 31) | ((uint64(v2)) << 30) | ((uint64(v2)) << 29) | ((uint64(v2)) << 28) | ((uint64(v2)) << 27) | ((uint64(v2)) << 26) | ((uint64(v2)) << 25) | ((uint64(v2)) << 24) | ((uint64(v2)) << 23) | ((uint64(v2)) << 22) | ((uint64(v2)) << 21) | ((uint64(v2)) << 20) | ((uint64(v2)) << 19) | ((uint64(v2)) << 18) | ((uint64(v2)) << 17) | ((uint64(v2)) << 16) | ((uint64(v2)) << 15) | ((uint64(v2)) << 14) | ((uint64(v2)) << 13) | ((uint64(v2)) << 12) | (uint64(v1)))) & uint64(0x3fffffffffffffff))
	var v4 uint64 = ((uint64((uint64(v3)) | (uint64(v0)))) & uint64(0x3fffffffffffffff))
	var v5 uint32 = ((uint32((uint64(a)) >> 62)) & uint32(0x1))
	var v6 uint32 = ((uint32((uint32(v2)) | (uint32(v5)))) & uint32(0x1))
	var v7 uint32 = ((uint32((uint64(a)) >> 63)) & uint32(0x1))
	var v8 uint32 = ((uint32((uint32(v2)) | (uint32(v7)))) & uint32(0x1))
	var v9 uint64 = (uint64(((uint64(v8)) << 63) | ((uint64(v6)) << 62) | (uint64(v4))))
	return uint64(v9)
}

var g0 uint64
var g1 uint16
var sink interface{}

func main() {
	sink = emu_ITYPE__op_ORI__rd__go__native_first(g0, g1)
	_ = sink
}
