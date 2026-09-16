// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ADDIW__one__rd__go__native_first.
//   
package main

//go:noinline
func emu_ADDIW__one__rd__go__native_first(a uint32, b uint16) uint64 {
	var v0 uint32 = uint32(a)
	var v1 uint32 = ((uint32((uint32(b)) >> 0)) & uint32(0xfff))
	var v2 uint32 = ((uint32((uint32(b)) >> 11)) & uint32(0x1))
	var v3 uint32 = (uint32(((uint32(v2)) << 31) | ((uint32(v2)) << 30) | ((uint32(v2)) << 29) | ((uint32(v2)) << 28) | ((uint32(v2)) << 27) | ((uint32(v2)) << 26) | ((uint32(v2)) << 25) | ((uint32(v2)) << 24) | ((uint32(v2)) << 23) | ((uint32(v2)) << 22) | ((uint32(v2)) << 21) | ((uint32(v2)) << 20) | ((uint32(v2)) << 19) | ((uint32(v2)) << 18) | ((uint32(v2)) << 17) | ((uint32(v2)) << 16) | ((uint32(v2)) << 15) | ((uint32(v2)) << 14) | ((uint32(v2)) << 13) | ((uint32(v2)) << 12) | (uint32(v1))))
	var v4 uint32 = (uint32((uint32(v3)) + (uint32(v0))))
	var v5 uint32 = ((uint32((uint32(v4)) >> 31)) & uint32(0x1))
	var v6 uint64 = (uint64(((uint64(v5)) << 63) | ((uint64(v5)) << 62) | ((uint64(v5)) << 61) | ((uint64(v5)) << 60) | ((uint64(v5)) << 59) | ((uint64(v5)) << 58) | ((uint64(v5)) << 57) | ((uint64(v5)) << 56) | ((uint64(v5)) << 55) | ((uint64(v5)) << 54) | ((uint64(v5)) << 53) | ((uint64(v5)) << 52) | ((uint64(v5)) << 51) | ((uint64(v5)) << 50) | ((uint64(v5)) << 49) | ((uint64(v5)) << 48) | ((uint64(v5)) << 47) | ((uint64(v5)) << 46) | ((uint64(v5)) << 45) | ((uint64(v5)) << 44) | ((uint64(v5)) << 43) | ((uint64(v5)) << 42) | ((uint64(v5)) << 41) | ((uint64(v5)) << 40) | ((uint64(v5)) << 39) | ((uint64(v5)) << 38) | ((uint64(v5)) << 37) | ((uint64(v5)) << 36) | ((uint64(v5)) << 35) | ((uint64(v5)) << 34) | ((uint64(v5)) << 33) | ((uint64(v5)) << 32) | (uint64(v4))))
	return uint64(v6)
}

var g0 uint32
var g1 uint16
var sink interface{}

func main() {
	sink = emu_ADDIW__one__rd__go__native_first(g0, g1)
	_ = sink
}
