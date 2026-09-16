// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of SLLIUW__one__rd__go__native_first.
//   
package main

//go:noinline
func emu_SLLIUW__one__rd__go__native_first(a uint32, b uint8) uint64 {
	var v0 uint32 = ((uint32((uint32(b)) >> 0)) & uint32(0x3f))
	var v1 uint64 = (uint64(((uint64(uint64(0x0))) << 6) | (uint64(v0))))
	var v2 uint32 = uint32(a)
	var v3 uint64 = (uint64(((uint64(uint32(0x0))) << 32) | (uint64(v2))))
	var v4 uint64 = (uint64((uint64(v3)) << ((uint64(v1)) & uint64(0x3f))))
	return uint64(v4)
}

var g0 uint32
var g1 uint8
var sink interface{}

func main() {
	sink = emu_SLLIUW__one__rd__go__native_first(g0, g1)
	_ = sink
}
