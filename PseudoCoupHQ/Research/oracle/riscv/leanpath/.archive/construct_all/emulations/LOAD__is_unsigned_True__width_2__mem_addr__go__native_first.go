// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of LOAD__is_unsigned_True__width_2__mem_addr__go__native_first.
//   
package main

//go:noinline
func emu_LOAD__is_unsigned_True__width_2__mem_addr__go__native_first(a uint64, b uint16) uint64 {
	var v0 uint32 = ((uint32((uint32(b)) >> 0)) & uint32(0xfff))
	var v1 uint32 = ((uint32((uint32(b)) >> 11)) & uint32(0x1))
	var v2 uint64 = (uint64(((uint64(v1)) << 63) | ((uint64(v1)) << 62) | ((uint64(v1)) << 61) | ((uint64(v1)) << 60) | ((uint64(v1)) << 59) | ((uint64(v1)) << 58) | ((uint64(v1)) << 57) | ((uint64(v1)) << 56) | ((uint64(v1)) << 55) | ((uint64(v1)) << 54) | ((uint64(v1)) << 53) | ((uint64(v1)) << 52) | ((uint64(v1)) << 51) | ((uint64(v1)) << 50) | ((uint64(v1)) << 49) | ((uint64(v1)) << 48) | ((uint64(v1)) << 47) | ((uint64(v1)) << 46) | ((uint64(v1)) << 45) | ((uint64(v1)) << 44) | ((uint64(v1)) << 43) | ((uint64(v1)) << 42) | ((uint64(v1)) << 41) | ((uint64(v1)) << 40) | ((uint64(v1)) << 39) | ((uint64(v1)) << 38) | ((uint64(v1)) << 37) | ((uint64(v1)) << 36) | ((uint64(v1)) << 35) | ((uint64(v1)) << 34) | ((uint64(v1)) << 33) | ((uint64(v1)) << 32) | ((uint64(v1)) << 31) | ((uint64(v1)) << 30) | ((uint64(v1)) << 29) | ((uint64(v1)) << 28) | ((uint64(v1)) << 27) | ((uint64(v1)) << 26) | ((uint64(v1)) << 25) | ((uint64(v1)) << 24) | ((uint64(v1)) << 23) | ((uint64(v1)) << 22) | ((uint64(v1)) << 21) | ((uint64(v1)) << 20) | ((uint64(v1)) << 19) | ((uint64(v1)) << 18) | ((uint64(v1)) << 17) | ((uint64(v1)) << 16) | ((uint64(v1)) << 15) | ((uint64(v1)) << 14) | ((uint64(v1)) << 13) | ((uint64(v1)) << 12) | (uint64(v0))))
	var v3 uint64 = (uint64((uint64(v2)) + (uint64(uint64(a)))))
	return uint64(v3)
}

var g0 uint64
var g1 uint16
var sink interface{}

func main() {
	sink = emu_LOAD__is_unsigned_True__width_2__mem_addr__go__native_first(g0, g1)
	_ = sink
}
