// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ZBA_RTYPEUW__one__rd__go__native_first.
//   
package main

//go:noinline
func emu_ZBA_RTYPEUW__one__rd__go__native_first(a uint32, b uint8, c uint64) uint64 {
	var v0 uint32 = ((uint32((uint32(b)) >> 0)) & uint32(0x3))
	var v1 uint64 = (uint64(((uint64(uint64(0x0))) << 2) | (uint64(v0))))
	var v2 uint32 = uint32(a)
	var v3 uint64 = (uint64(((uint64(uint32(0x0))) << 32) | (uint64(v2))))
	var v4 uint64 = (uint64((uint64(v3)) << ((uint64(v1)) & uint64(0x3f))))
	var v5 uint64 = (uint64((uint64(v4)) + (uint64(uint64(c)))))
	return uint64(v5)
}

var g0 uint32
var g1 uint8
var g2 uint64
var sink interface{}

func main() {
	sink = emu_ZBA_RTYPEUW__one__rd__go__native_first(g0, g1, g2)
	_ = sink
}
