// task t4 emulation -- rendered by render_general.py, one named
// intermediate per node of the term of ZBS_RTYPE__op_BCLR__rd__go__native_first.
//   
package main

//go:noinline
func emu_ZBS_RTYPE__op_BCLR__rd__go__native_first(a uint8, b uint64) uint64 {
	var v0 uint32 = ((uint32((uint32(a)) >> 0)) & uint32(0x3f))
	var v1 uint64 = (uint64(((uint64(uint64(0x0))) << 6) | (uint64(v0))))
	var v2 uint64 = (uint64((uint64(uint64(0x1))) << ((uint64(v1)) & uint64(0x3f))))
	var v3 uint64 = (uint64(^(uint64(uint64(b)))))
	var v4 uint64 = (uint64((uint64(v3)) | (uint64(v2))))
	var v5 uint64 = (uint64(^(uint64(v4))))
	return uint64(v5)
}

var g0 uint8
var g1 uint64
var sink interface{}

func main() {
	sink = emu_ZBS_RTYPE__op_BCLR__rd__go__native_first(g0, g1)
	_ = sink
}
