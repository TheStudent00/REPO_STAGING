// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ITYPE__op_ANDI__rd__go__native_first.
//   
package main

//go:noinline
func emu_ITYPE__op_ANDI__rd__go__native_first(a uint64, b uint16) uint64 {
	var v0 uint32 = ((uint32((uint32(b)) >> 0)) & uint32(0xfff))
	var v1 uint32 = ((uint32(^(uint32(v0)))) & uint32(0xfff))
	var v2 uint32 = ((uint32((uint32(b)) >> 11)) & uint32(0x1))
	var v3 uint32 = ((uint32(^(uint32(v2)))) & uint32(0x1))
	var v4 uint64 = ((uint64(((uint64(v3)) << 62) | ((uint64(v3)) << 61) | ((uint64(v3)) << 60) | ((uint64(v3)) << 59) | ((uint64(v3)) << 58) | ((uint64(v3)) << 57) | ((uint64(v3)) << 56) | ((uint64(v3)) << 55) | ((uint64(v3)) << 54) | ((uint64(v3)) << 53) | ((uint64(v3)) << 52) | ((uint64(v3)) << 51) | ((uint64(v3)) << 50) | ((uint64(v3)) << 49) | ((uint64(v3)) << 48) | ((uint64(v3)) << 47) | ((uint64(v3)) << 46) | ((uint64(v3)) << 45) | ((uint64(v3)) << 44) | ((uint64(v3)) << 43) | ((uint64(v3)) << 42) | ((uint64(v3)) << 41) | ((uint64(v3)) << 40) | ((uint64(v3)) << 39) | ((uint64(v3)) << 38) | ((uint64(v3)) << 37) | ((uint64(v3)) << 36) | ((uint64(v3)) << 35) | ((uint64(v3)) << 34) | ((uint64(v3)) << 33) | ((uint64(v3)) << 32) | ((uint64(v3)) << 31) | ((uint64(v3)) << 30) | ((uint64(v3)) << 29) | ((uint64(v3)) << 28) | ((uint64(v3)) << 27) | ((uint64(v3)) << 26) | ((uint64(v3)) << 25) | ((uint64(v3)) << 24) | ((uint64(v3)) << 23) | ((uint64(v3)) << 22) | ((uint64(v3)) << 21) | ((uint64(v3)) << 20) | ((uint64(v3)) << 19) | ((uint64(v3)) << 18) | ((uint64(v3)) << 17) | ((uint64(v3)) << 16) | ((uint64(v3)) << 15) | ((uint64(v3)) << 14) | ((uint64(v3)) << 13) | ((uint64(v3)) << 12) | (uint64(v1)))) & uint64(0x7fffffffffffffff))
	var v5 uint64 = ((uint64((uint64(a)) >> 0)) & uint64(0x7fffffffffffffff))
	var v6 uint64 = ((uint64(^(uint64(v5)))) & uint64(0x7fffffffffffffff))
	var v7 uint64 = ((uint64((uint64(v6)) | (uint64(v4)))) & uint64(0x7fffffffffffffff))
	var v8 uint64 = ((uint64(^(uint64(v7)))) & uint64(0x7fffffffffffffff))
	var v9 uint32 = ((uint32((uint64(a)) >> 63)) & uint32(0x1))
	var v10 uint32 = ((uint32(^(uint32(v9)))) & uint32(0x1))
	var v11 uint32 = ((uint32((uint32(v3)) | (uint32(v10)))) & uint32(0x1))
	var v12 uint32 = ((uint32(^(uint32(v11)))) & uint32(0x1))
	var v13 uint64 = (uint64(((uint64(v12)) << 63) | (uint64(v8))))
	return uint64(v13)
}

var g0 uint64
var g1 uint16
var sink interface{}

func main() {
	sink = emu_ITYPE__op_ANDI__rd__go__native_first(g0, g1)
	_ = sink
}
