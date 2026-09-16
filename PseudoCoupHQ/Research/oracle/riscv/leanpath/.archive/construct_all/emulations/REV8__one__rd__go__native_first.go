// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of REV8__one__rd__go__native_first.
//   
package main

//go:noinline
func emu_REV8__one__rd__go__native_first(a uint64) uint64 {
	var v0 uint32 = ((uint32((uint64(a)) >> 56)) & uint32(0xff))
	var v1 uint32 = ((uint32((uint64(a)) >> 48)) & uint32(0xff))
	var v2 uint32 = ((uint32((uint64(a)) >> 40)) & uint32(0xff))
	var v3 uint32 = ((uint32((uint64(a)) >> 32)) & uint32(0xff))
	var v4 uint32 = ((uint32((uint64(a)) >> 24)) & uint32(0xff))
	var v5 uint32 = ((uint32((uint64(a)) >> 16)) & uint32(0xff))
	var v6 uint32 = ((uint32((uint64(a)) >> 8)) & uint32(0xff))
	var v7 uint32 = ((uint32((uint64(a)) >> 0)) & uint32(0xff))
	var v8 uint64 = (uint64(((uint64(v7)) << 56) | ((uint64(v6)) << 48) | ((uint64(v5)) << 40) | ((uint64(v4)) << 32) | ((uint64(v3)) << 24) | ((uint64(v2)) << 16) | ((uint64(v1)) << 8) | (uint64(v0))))
	return uint64(v8)
}

var g0 uint64
var sink interface{}

func main() {
	sink = emu_REV8__one__rd__go__native_first(g0)
	_ = sink
}
